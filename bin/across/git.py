import os
import tempfile
from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Sequence, Optional, Union, TextIO

import yaml
from git import Repo, Tag
from git.objects import Commit

from .config import RepositoryConfig, AcrossConfig
from .maven import (
    Version,
    update_parent,
    update_version_properties,
)
from .util import system, system_error


class GitRepository:
    config: RepositoryConfig
    path: Path
    name: str
    repo: Repo

    def __init__(self, config: RepositoryConfig, path: Path):
        self.config = config
        self.path = path
        self.name = config.id
        self.repo = Repo(path)

    @property
    def active_branch_name(self) -> str:
        return str(self.repo.active_branch)

    @property
    def branch_names(self) -> List[str]:
        return [b.name for b in self.repo.branches]  # type: ignore[attr-defined]

    @property
    def tag_names(self) -> List[str]:
        return [t.name for t in self.repo.tags]

    def determine_latest_version(self) -> Optional[Version]:
        tags = [str(tag) for tag in self.repo.tags]
        branch_tags = filter(
            lambda t: t.startswith(f"v{self.active_branch_name}."), tags
        )
        branch_versions = sorted([Version.parse(tag[1:]) for tag in branch_tags])
        if branch_versions:
            return branch_versions[-1]
        else:
            return None

    def determine_next_version(self) -> Version:
        tags = [str(tag) for tag in self.repo.tags]
        branch_tags = sorted(
            filter(lambda t: t.startswith(f"v{self.active_branch_name}."), tags)
        )
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
            return Version.parse(f"{self.active_branch_name}.0-M1")  # TODO

    def fetch(self):
        for remote in self.repo.remotes:
            remote.fetch()

    def clone(self, stash_clone: bool) -> "GitRepository":
        tmp_repo_dir = Path(tempfile.gettempdir(), "across-releases").absolute()
        if not tmp_repo_dir.exists():
            tmp_repo_dir.mkdir()
        clone_dir = Path(tmp_repo_dir, self.name)
        if clone_dir.exists():
            repository = GitRepository(self.config, clone_dir)
            # TODO: also check for unpushed commits!
            if repository.repo.is_dirty():
                if stash_clone:
                    os.chdir(clone_dir)
                    print(f"Stashing dirty context in {clone_dir}")
                    system("git stash")
                else:
                    raise Exception(f"Clone dir is dirty: {clone_dir}")
            repository.fetch()
        else:
            os.chdir(tmp_repo_dir)
            url = self.repo.remote("origin").url
            system(f"git clone {url}")
            repository = GitRepository(self.config, clone_dir)
        repository.chdir()
        if repository.active_branch_name != self.active_branch_name:
            system(f"git checkout {self.active_branch_name}")
        system(f"git pull --ff-only")  # we don't want git pull to do a merge!
        return repository

    def chdir(self):
        os.chdir(self.path)

    def update_pom_files(self, dependency_versions: "RepositoryVersions", revision):
        self.chdir()
        version_properties_path = dependency_versions.write_versions_properties(
            self.path, revision
        )
        if self.name == "across-platform":
            os.chdir(Path(self.path, "across-platform-dependencies"))
            update_parent(dependency_versions.versions["across-framework"])
        elif self.name != "across-framework":
            # The parent pom of across-framework is Spring Boot, so nothing to do in that case.
            # For all other repositories, the parent pom is across-framework:
            update_parent(dependency_versions.versions["across-framework"])
        self.chdir()
        update_version_properties(version_properties_path)

    def commit_and_push(self, version: Version) -> Commit:
        self.repo.git.add(update=True)  # git add -u
        commit = self.repo.index.commit(_message(version))
        self.repo.remote("origin").push()
        return commit

    def tag_and_push(self, version: Version) -> Tag:
        tag = self.repo.create_tag(f"v{version}", message=_message(version))
        self.repo.remote("origin").push(tag.name)
        return tag

    def generate_dependencies(self):
        self.chdir()
        cmd = "generate-dependencies.sh"
        exit_code = os.system(cmd)
        if exit_code != 0:
            if self.name == "across-autoconfigure":
                print(
                    "generate-dependencies.sh failed in across-autoconfigure, but that's OK"
                )
            else:
                system_error(cmd, exit_code)


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
                repository_config, Path(directory, repository_config.id)
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

    def check_dirty(self):
        dirty_repos = list()
        for repository in self.repositories:
            if repository.repo.is_dirty():
                dirty_repos.append(repository.name)
        if dirty_repos:
            raise Exception(f"{dirty_repos} are dirty (uncommitted changes)!")

    def determine_snapshot_versions(self) -> "RepositoryVersions":
        result = dict()
        for repository in self.repositories:
            # This assumes the branch is named something like X.Y:
            bv = Version.parse(repository.active_branch_name)
            result[repository.name] = Version(bv.major, bv.minor, bv.patch, "SNAPSHOT")
        return RepositoryVersions(result)

    def execute_for_each(self, cmd):
        old_wd = os.getcwd()
        for repository in self.repositories:
            os.chdir(repository.path)
            system(cmd)
        os.chdir(old_wd)


@dataclass
class RepositoryVersions:
    versions: dict[str, Version]

    @property
    def repo_names(self) -> List[str]:
        return list(self.versions.keys())

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
            if repo_name not in config.repository_ids:
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
        revision: Version | None,
        prefix="",
    ):
        if isinstance(output_or_path, Path):
            directory: Path = output_or_path
            path = Path(directory, "versions.properties")
            print(f"Writing {path}")
            with open(path, "w") as output1:
                self.write_versions_properties(output1, revision, prefix)
            return path
        elif isinstance(output_or_path, TextIOWrapper):
            output2: TextIO = output_or_path
            if revision:
                output2.write(f"{prefix}revision={revision}\n")
            for name, version in self.versions.items():
                output2.write(f"{prefix}{name}.version={version}\n")
        else:
            raise Exception(f"Cannot write to {output_or_path.__class__}")


@dataclass
class ReleasePlan:
    path: Path
    repository_versions: RepositoryVersions

    @property
    def name(self) -> str:
        return os.path.basename(self.path.stem)

    @property
    def versions(self) -> dict[str, Version]:
        return self.repository_versions.versions

    @staticmethod
    def parse(config: AcrossConfig, path: Path) -> "ReleasePlan":
        return ReleasePlan(path, RepositoryVersions.parse(config, path))


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


def _message(version: Version) -> str:
    return f"Release {version} by ax-release.py"
