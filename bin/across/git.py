from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Sequence, Optional, Union, TextIO

import yaml
from git import Repo
from semver import Version

from .config import RepositoryConfig, AcrossConfig


class GitRepository:
    config: RepositoryConfig
    path: Path
    name: str
    repo: Repo

    def __init__(self, config: RepositoryConfig, path: Path):
        self.config = config
        self.path = path
        self.name = config.name
        self.repo = Repo(path)

    @property
    def branch(self) -> str:
        return str(self.repo.active_branch)

    @property
    def branch_names(self) -> List[str]:
        return [b.name for b in self.repo.branches]  # type: ignore[attr-defined]

    @property
    def tag_names(self) -> List[str]:
        return [t.name for t in self.repo.tags]

    def determine_latest_version(self) -> Optional[Version]:
        tags = [str(tag) for tag in self.repo.tags]
        branch_tags = filter(lambda t: t.startswith(f"v{self.branch}."), tags)
        branch_versions = sorted([Version.parse(tag[1:]) for tag in branch_tags])
        if branch_versions:
            return branch_versions[-1]
        else:
            return None

    def determine_next_version(self) -> Version:
        tags = [str(tag) for tag in self.repo.tags]
        branch_tags = sorted(filter(lambda t: t.startswith(f"v{self.branch}."), tags))
        if branch_tags:
            last_tag = branch_tags[-1]
            last_version = Version.parse(last_tag[1:])
            return Version(
                last_version.major,
                last_version.minor,
                last_version.patch + 1,
                "M1",  # TODO
            )
        else:
            return Version.parse(f"{self.branch}.0-M1")  # TODO

    def fetch(self):
        for remote in self.repo.remotes:
            remote.fetch()


class GitRepositoryCollection:
    directory: Path
    config: AcrossConfig
    repositories_by_name: Dict[str, GitRepository] = dict()
    repositories: List[GitRepository] = list()  # Same order as in AcrossConfig

    def __init__(self, directory: Path, config: AcrossConfig):
        self.directory = directory
        self.config = config
        for repository_config in config.repositories:
            repository = GitRepository(
                repository_config, Path(directory, repository_config.name)
            )
            self.repositories_by_name[repository.name] = repository
            self.repositories.append(repository)

    def fetch_all(self):
        for repository in self.repositories:
            print(f"Fetching from {repository.name}")
            repository.fetch()

    def find_repositories_before(self, repository_name: str) -> List[GitRepository]:
        result: List[GitRepository] = list()
        for repository in self.repositories:
            if repository.name == repository_name:
                return result
            result.append(repository)
        return result

    def check_release_plan(
        self, release_plan: "RepositoryVersions", repo_name: str
    ) -> GitRepository:
        repository = self.repositories_by_name[repo_name]
        self._check_tag_does_not_exist(repository, release_plan.versions[repo_name])
        self._check_branches_exist(release_plan)
        return repository

    @staticmethod
    def _check_tag_does_not_exist(repository: GitRepository, version: Version):
        tag = f"v{version}"
        if tag in repository.tag_names:
            raise Exception(f"Tag {tag} already exists in {repository.name}")

    def _check_branches_exist(self, release_plan):
        for repo_name, version in release_plan.versions.items():
            branch_name = f"{version.major}.{version.minor}"
            repository = self.repositories_by_name[repo_name]
            if branch_name not in repository.branch_names:
                raise Exception(f"Branch {branch_name} does not exist in {repo_name}")


@dataclass
class RepositoryVersions:
    # path: Path
    versions: dict[str, Version]

    def print(self, explanation):
        if not self.versions:
            print(explanation, "None found!")
            return
        print(explanation)
        for repo_name, version in self.versions.items():
            print("  ", repo_name, ":", version)

    @staticmethod
    def parse(config: AcrossConfig, path: Path) -> "RepositoryVersions":
        with open(path) as ins:
            tmp = yaml.load(ins, Loader=yaml.CLoader)
        releases = dict()
        wrong_repo_names = list()
        for repo_name, version in tmp.items():
            if repo_name not in config.repository_names:
                wrong_repo_names.append(repo_name)
            releases[repo_name] = Version.parse(version)
        if wrong_repo_names:
            raise Exception(f"Wrong repository names in {path}: {wrong_repo_names}")
        return RepositoryVersions(releases)

    @staticmethod
    def latest_versions(repositories: List[GitRepository]) -> "RepositoryVersions":
        errored_repo_names = list()
        result = dict()
        for repository in repositories:
            latest_version = repository.determine_latest_version()
            if latest_version:
                result[repository.name] = latest_version
            else:
                errored_repo_names.append(repository.name)
        print(f"Versions: {result}")
        if errored_repo_names:
            raise Exception(
                f"Could not determine latest version for: {errored_repo_names}"
            )
        return RepositoryVersions(result)

    def determine_subset(
        self, dependency_repos: List[GitRepository]
    ) -> "RepositoryVersions":
        result = dict()
        for dependency_repo in dependency_repos:
            if dependency_repo.name in self.versions:
                result[dependency_repo.name] = self.versions[dependency_repo.name]
        return RepositoryVersions(result)

    def write_versions_properties(
        self,
        output_or_path: Union[Path, TextIO],
        repo_version: Version,
        prefix="",
    ):
        if isinstance(output_or_path, Path):
            directory: Path = output_or_path
            path = Path(directory, "versions.properties")
            print(f"Writing {path}")
            with open(path, "w") as output1:
                self.write_versions_properties(output1, repo_version, prefix)
        elif isinstance(output_or_path, TextIOWrapper):
            output2: TextIO = output_or_path
            output2.write(f"{prefix}revision={repo_version}\n")
            for name, version in self.versions.items():
                output2.write(f"{prefix}{name}.version={version}\n")
        else:
            raise Exception(f"Cannot write to {output_or_path.__class__}")


def create_repos(
    directory: Path = Path().absolute(), repo_names: Sequence[str] = []
) -> Dict[Path, Repo]:
    kv_pairs = [
        (Path(repo_path).absolute(), Repo(repo_path))
        for repo_path in find_repo_paths(directory, repo_names)
    ]
    return dict(kv_pairs)
    # return dict([(os.path.basename(repo.git_dir), repo) for repo in repos])


def find_repo_paths(directory: Path, repo_names: Sequence[str] = []) -> List[Path]:
    # return [os.path.dirname(git) for git in glob.glob("*/*/.git")]
    # The directory structure deliberately designed to have git repos only at depth 2:
    # - faster than a full recursive search, especially on Windows
    # - also easy in shell scripts:
    # cwd = Path.cwd() # gives an absolute path everywhere
    # cwd = Path()
    # eprint(cwd)
    if repo_names:
        result = [Path(directory, name) for name in repo_names]
        for path in result:
            if not Path(path, ".git").exists():
                raise (
                    Exception(
                        f"{path}: is not a git repository (.git subdirectory missing)"
                    )
                )
    else:
        result = [p.parent for p in directory.glob("*/.git")]
    return sorted(result)


def repo_path(repo: Repo) -> Path:
    return Path(repo.git_dir).absolute().parent


def repo_name(repo: Repo) -> str:
    return repo_path(repo).name
