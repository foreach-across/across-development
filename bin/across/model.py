import itertools
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import util
from util import eprint

# from maven_dtree import read_projects
# import maven_dtree

POM_XML = "pom.xml"
EFFECTIVE_POM_XML = ".effective-pom.xml"
DEPENDENCY_TREE_TXT = ".dependency-tree.txt"
LOCAL_SNAPSHOT = "local-SNAPSHOT"


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
        return self.group_id + ":" + self.artifact_id + ":" + self.version

    def is_foreach(self):
        return self.group_id.startswith("com.foreach.")

    def __str__(self):
        return self.long_id


@dataclass()
class ProjectArtifact(Artifact):
    # project: "Project"
    packaging: str  # TODO enum?

    def __str__(self):
        return f"{super()}:{self.packaging}"


@dataclass()
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


class Repository:
    path: Path
    name: str
    projects: Dict[str, Project]

    def __init__(self, path: Path, name: str, branch: str, projects: Sequence[Project]):
        self.path = path
        self.name = name
        self.branch = branch
        self.projects = {p.artifact.artifact_id: p for p in projects}

    def __str__(self):
        lines = [str(self.path.anchor), str(self.path)] + [
            f"  {p.artifact.artifact_id}: {p.artifact.version}"
            for p in self.projects.values()
        ]
        return "\n".join(lines)

    @property
    def version(self) -> str:
        projects_by_version = self.projects_by_version
        if len(projects_by_version) == 1:
            version = list(projects_by_version.keys())[0]
            if version == LOCAL_SNAPSHOT:
                return self.branch + "-SNAPSHOT"
            return version
        projects_by_version_str = {
            k: [str(p) for p in v] for k, v in projects_by_version.items()
        }
        raise Exception(
            f"{self.name}: Unexpected nr of versions in the projects: {projects_by_version_str}"
        )

    @property
    def projects_by_version(self) -> Dict[str, Sequence[Project]]:
        result = itertools.groupby(self.projects.values(), lambda p: p.artifact.version)
        return {k: list(v) for k, v in result}

    @property
    def versioned_deps(self) -> Dict[str, str]:  # artifactId -> version
        used_artifacts: Dict[str, Tuple[UsedArtifact, Project]] = dict()
        errors = list()
        for project in self.projects.values():
            for artifact in project.direct_dependencies:
                if artifact.is_foreach():
                    prev_used_artifact_tuple = used_artifacts.get(artifact.artifact_id)
                    if prev_used_artifact_tuple:
                        (existing_artifact, from_project) = prev_used_artifact_tuple
                        if existing_artifact.version != artifact.version:
                            current_pom_file = project.pom_file.relative_to(Path.cwd())
                            first_pom_file = from_project.pom_file.relative_to()
                            msg = f"{current_pom_file} depends on {artifact.version} for {artifact.short_id},"
                            msg += f"but {first_pom_file} already depends on {existing_artifact.version}"
                            errors.append(msg)
                    else:
                        used_artifacts[artifact.artifact_id] = (artifact, project)
        if errors:
            msg = "\n".join(errors)
            msg += "\nThis is likely a dependency-management problem: either something is missing there,"
            msg += "\nor another version is declared in on of the child projects"
        return {
            artifactId: artifact.version
            for artifactId, (artifact, _) in used_artifacts.items()
        }

    @staticmethod
    def read_all() -> List["Repository"]:
        import maven_dtree

        result = list()
        for repo_path in find_repo_paths():
            # eprint(repo_path)
            projects = maven_dtree.read_projects(repo_path)
            result.append(Repository.create(repo_path, projects))
        return result

    @staticmethod
    def create(repo_path: Path, projects: List[Project]) -> "Repository":
        branch = Repository.determine_branch(repo_path)
        repository = Repository(repo_path, repo_path.name, branch, projects)
        eprint(repository)
        return repository

    @staticmethod
    def determine_branch(repo_path: Path) -> str:
        # TODO: this is easier with: git rev-parse --abbrev-ref HEAD
        process = subprocess.run(
            ["git", "branch", "-a"], capture_output=True, text=True, cwd=repo_path
        )
        text = process.stdout
        lines: List[str] = text.splitlines(keepends=False)
        for line in lines:
            if line.startswith("* "):
                branch = line[2:].strip()
                if branch.startswith("(HEAD"):
                    # Example: * (HEAD detached at v4.1.5)
                    return "HEAD"
                return branch
        raise Exception(f"{repo_path}: Could not determine branch from: \n{text}")


def find_repo_paths() -> List[Path]:
    # return [os.path.dirname(git) for git in glob.glob("*/*/.git")]
    # The directory structure deliberately designed to have git repos only at depth 2:
    # - faster than a full recursive search, especially on Windows
    # - also easy in shell scripts:
    # cwd = Path.cwd() # gives an absolute path everywhere
    cwd = Path()
    eprint(cwd)
    result = sorted([p.parent for p in cwd.glob("*/*/*/.git")])
    # so we can still use the script in lower directories as well, useful in public/modules:
    if not result:
        result = sorted([p.parent for p in cwd.glob("*/*/.git")])
        if not result:
            result = sorted([p.parent for p in cwd.glob("*/.git")])
    return result
