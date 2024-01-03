from pathlib import Path
from typing import Dict, List, Sequence, Optional

from git import Repo
from semver import Version

from across.config import RepositoryConfig, AcrossConfig


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

    def determine_latest_version(self) -> Optional[Version]:
        tags = [str(tag) for tag in self.repo.tags]
        # print(tags)
        branch_tags = sorted(filter(lambda t: t.startswith(f"v{self.branch}."), tags))
        # print(branch_tags)
        if branch_tags:
            last_tag = branch_tags[-1]
            return Version.parse(last_tag[1:])
        else:
            return None

    def determine_next_version(self) -> Version:
        tags = [str(tag) for tag in self.repo.tags]
        # print(tags)
        branch_tags = sorted(filter(lambda t: t.startswith(f"v{self.branch}."), tags))
        # print(branch_tags)
        if branch_tags:
            last_tag = branch_tags[-1]
            last_version = Version.parse(last_tag[1:])
            return Version(
                last_version.major, last_version.minor, last_version.patch + 1
            )
        else:
            return Version.parse(f"{self.branch}.0")

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
