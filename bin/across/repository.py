import itertools
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from git import Repo

from .util import eprint

from .maven import Project, LOCAL_SNAPSHOT, UsedArtifact


class Repository:
    repo: Repo
    path: Path
    name: str
    projects: Dict[str, Project]

    def __init__(self, path: Path, name: str, projects: Sequence[Project]):
        self.repo = Repo(path)
        self.path = path
        self.name = name
        self.branch = str(self.repo.head)
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
    def read_all(directory: Path = Path().absolute()) -> List["Repository"]:
        result = list()
        for repo_path in _find_repo_paths(directory):
            # eprint(repo_path)
            projects = Project.read_all(repo_path)
            result.append(Repository.create(repo_path, projects))
        return result

    @staticmethod
    def create(repo_path: Path, projects: List[Project]) -> "Repository":
        repository = Repository(repo_path, repo_path.name, projects)
        eprint(repository)
        return repository


def _find_repo_paths(directory: Path) -> List[Path]:
    # return [os.path.dirname(git) for git in glob.glob("*/*/.git")]
    # The directory structure deliberately designed to have git repos only at depth 2:
    # - faster than a full recursive search, especially on Windows
    # - also easy in shell scripts:
    # cwd = Path.cwd() # gives an absolute path everywhere
    # cwd = Path()
    # eprint(cwd)
    result = [p.parent for p in directory.glob("*/.git")]
    return sorted(result)
