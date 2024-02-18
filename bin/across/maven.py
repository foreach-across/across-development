from dataclasses import dataclass
from pathlib import Path
from typing import List

import semver

from . import util
from .config import RepositoryConfig, ModuleConfig
from .util import system

POM_XML = "pom.xml"
# EFFECTIVE_POM_XML = ".effective-pom.xml"
DEPENDENCY_TREE_TXT = "dependency.tree.txt"
LOCAL_SNAPSHOT = "local-SNAPSHOT"

MAVEN_VERSIONS_PLUGIN_VERSION = "2.16.2"

MAVEN_CENTRAL_URL = "https://repo1.maven.org/maven2"


# Wrapper around semver.Version that allows X.Y for X.Y-SNAPSHOT
class Version(semver.Version):
    @staticmethod
    def parse(s: str) -> "Version":  # type: ignore[override]
        if s.count(".") == 1:
            # assuming it's X.Y:
            s += ".666"
        sv = semver.Version.parse(s)
        return Version(sv.major, sv.minor, sv.patch, sv.prerelease, sv.build)

    def __str__(self):
        result = super().__str__()
        if self.patch == 666:
            return result.replace(".666", "")
        return result


@dataclass
class Artifact(object):
    group_id: str
    artifact_id: str
    version: str

    @property
    def short_id(self):
        return self.group_id + ":" + self.artifact_id

    @property
    def long_id(self):
        return f"{self.group_id}:{self.artifact_id}:{self.version}"

    def is_foreach(self):
        return self.group_id.startswith("com.foreach.")

    @property
    def dir_path(self) -> str:
        return (
            self.group_id.replace(".", "/")
            + "/"
            + self.artifact_id
            + "/"
            + str(self.version)
        )

    def file_name(self, extension="jar", suffix=None, check_sum=None):
        real_suffix = f"-{suffix}" if suffix else ""
        real_check_sum = f".{check_sum}" if check_sum else ""
        return f"{self.artifact_id}-{self.version}{real_suffix}.{extension}{real_check_sum}"

    def file_path(self, extension="jar", suffix=None, check_sum=None):
        return f"{self.dir_path}/{self.file_name(extension, suffix, check_sum)}"

    @property
    def javadoc_jar_name(self):
        return self.file_name(suffix="javadoc", extension="jar")

    @property
    def javadoc_jar_url(self):
        return f"{MAVEN_CENTRAL_URL}/{self.dir_path}/{self.javadoc_jar_name}"

    @property
    def is_pom(self) -> bool:
        return (
            self.artifact_id.endswith("-bom")
            or self.artifact_id.endswith("-dependencies")
            or self.artifact_id.endswith("-parent")
        )

    def __str__(self):
        return self.long_id

    @staticmethod
    def of(
        repository_config: RepositoryConfig, module_config: ModuleConfig, version: str
    ) -> "Artifact":
        return Artifact(repository_config.group_id, module_config.artifact_id, version)


@dataclass
class ProjectArtifact(Artifact):
    # project: "Project"
    packaging: str  # TODO enum?

    def __str__(self):
        return f"{super()}:{self.packaging}"


@dataclass
class UsedArtifact(Artifact):
    # using_project: "Project"
    type: str
    scope: str  # TODO enum?
    is_optional: bool
    is_direct_dependency: bool

    def __str__(self):
        optional = "optional" if self.is_optional else "required"
        direct = "direct" if self.is_direct_dependency else "indirect"
        return f"{super()}:{self.type}:{optional}:{direct}"


class Project(object):
    def __init__(
        self,
        repository_path: Path,
        project_dir: Path,
        project_artifact: ProjectArtifact,
        all_dependencies: List[UsedArtifact],
    ):
        self.repository_path = repository_path
        self.repository_name = util.repository_name(repository_path)
        self.project_path = project_dir
        self.pom_file = project_dir / POM_XML
        assert self.pom_file.is_file()
        self.artifact = project_artifact
        self.all_dependencies = all_dependencies
        self.direct_dependencies = filter(
            lambda a: a.is_direct_dependency, all_dependencies
        )

    def __str__(self):
        return f"Project({self.long_id})"

    @property
    def short_id(self):
        return self.artifact.short_id

    @property
    def long_id(self):
        return self.artifact.short_id

    @property
    def group_id(self):
        return self.artifact.group_id

    @property
    def artifact_id(self):
        return self.artifact.artifact_id

    @property
    def version(self):
        return self.artifact.version

    @staticmethod
    def read_all(repository_dir: Path) -> List["Project"]:
        dep_tree_paths = list(repository_dir.rglob(DEPENDENCY_TREE_TXT))
        # assert len(dep_tree_paths) > 0
        return [_parse_dependency_tree(repository_dir, path) for path in dep_tree_paths]


def update_parent(across_framework_version: Version):
    cmd = [
        "mvn",
        f"versions:{MAVEN_VERSIONS_PLUGIN_VERSION}:update-parent",
        "-DskipResolution=true",
        f"-DparentVersion={across_framework_version}",
    ]
    system(" ".join(cmd))


def update_version_properties(version_properties_path: Path):
    cmd = [
        "mvn",
        f"versions:{MAVEN_VERSIONS_PLUGIN_VERSION}:set-property",
        f"-DpropertiesVersionsFile={version_properties_path}",
    ]
    system(" ".join(cmd))


def maven_clean_install_without_tests():
    system("mvn clean install -DskipTests")


def _parse_dependency_tree(repository_path: Path, dep_tree_path: Path) -> Project:
    project_path = dep_tree_path.parent
    pom_path = project_path / POM_XML
    please_run_dtree = "Please run: ax-make-dependency-tree.sh (from the top-level dir)"
    if not dep_tree_path.exists():
        raise Exception(
            f"{project_path}: could not find {DEPENDENCY_TREE_TXT}: {please_run_dtree}"
        )
    # if dep_tree_path.stat().st_mtime < pom_path.stat().st_mtime:
    #     raise Exception(
    #         f"{project_path}: {POM_XML} is newer than {DEPENDENCY_TREE_TXT}: {please_run_dtree}"
    #     )
    lines = dep_tree_path.read_text().splitlines()
    project_line = lines[0]
    dependency_lines = filter(lambda line: len(line.strip()) > 0, lines[1:])
    (group_id, artifact_id, packaging, version) = project_line.split(":")
    project_artifact = ProjectArtifact(group_id, artifact_id, version, packaging)
    artifacts = [_parse_dependency_line(line) for line in dependency_lines]
    return Project(repository_path, project_path, project_artifact, artifacts)


def _parse_dependency_line(line: str) -> UsedArtifact:
    # print(f"'{line}'")
    line_parts = line.split()
    is_optional = line_parts[-1] == "(optional)"
    if is_optional:
        line_parts = line_parts[:-1]
    is_selected_from_constraint = {
        "(version",
        "selected",
        "from",
        "constraint",
    }.issubset(line_parts)
    if is_selected_from_constraint:
        # |  |  \- org.webjars.bower:bootstrap:jar:5.1.3:compile (version selected from constraint [3.3.7,))
        line_parts = line_parts[:-5]
    is_direct_dependency = len(line_parts) == 2
    dep_parts = line_parts[-1].split(":")
    if len(dep_parts) == 6:
        # io.netty:netty-resolver-dns-native-macos:jar:osx-x86_64:4.1.70.Final:provided
        (group_id, artifact_id, type_, _, version, scope) = dep_parts
    else:
        (group_id, artifact_id, type_, version, scope) = dep_parts
    return UsedArtifact(
        group_id, artifact_id, version, type_, scope, is_optional, is_direct_dependency
    )
