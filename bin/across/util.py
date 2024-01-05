import os
import sys
from pathlib import Path


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# The assumption is that all repository are cloned with the same name as on the git server:
def repository_name(repo_dir: Path) -> str:
    git_dir = repo_dir / ".git"
    assert git_dir.is_dir()
    return repo_dir.name


def system(cmd):
    exit_code = os.system(cmd)
    if exit_code != 0:
        raise Exception(f"Command exited with {exit_code}: {cmd}")
