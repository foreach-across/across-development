from pathlib import Path
from typing import List

from . model import DEPENDENCY_TREE_TXT, Project, ProjectArtifact, UsedArtifact, POM_XML


def read_projects(repository_dir: Path) -> List[Project]:
    dep_tree_paths = list(repository_dir.rglob(DEPENDENCY_TREE_TXT))
    # assert len(dep_tree_paths) > 0
    return [_parse_dependency_tree(repository_dir, path) for path in dep_tree_paths]


def _parse_dependency_tree(repository_path: Path, dep_tree_path: Path) -> Project:
    project_path = dep_tree_path.parent
    pom_path = project_path / POM_XML
    please_run_dtree = "Please run: ax-make-dependency-tree.sh (from the top-level dir)"
    if not dep_tree_path.exists():
        raise Exception(
            f"{project_path}: could not find {DEPENDENCY_TREE_TXT}: {please_run_dtree}"
        )
    if dep_tree_path.stat().st_mtime < pom_path.stat().st_mtime:
        raise Exception(
            f"{project_path}: {POM_XML} is newer than {DEPENDENCY_TREE_TXT}: {please_run_dtree}"
        )
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
