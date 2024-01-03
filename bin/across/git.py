from pathlib import Path
from typing import Dict, List, Sequence

from git import Repo


def create_repos(
    directory: Path = Path().absolute(), repo_names: Sequence[str] = None
) -> Dict[Path, Repo]:
    kv_pairs = [
        (Path(repo_path).absolute(), Repo(repo_path))
        for repo_path in find_repo_paths(directory, repo_names)
    ]
    return dict(kv_pairs)
    # return dict([(os.path.basename(repo.git_dir), repo) for repo in repos])


def find_repo_paths(directory: Path, repo_names: Sequence[str] = None) -> List[Path]:
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
