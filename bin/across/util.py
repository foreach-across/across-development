import os
import sys
from pathlib import Path
from typing import List

import semver


# Wrapper around semver.Version that allows X.Y for X.Y-SNAPSHOT
class Version(semver.Version):
    @staticmethod
    def parse(s: str) -> "Version":  # type: ignore[override]
        if s.count(".") == 1:
            # assuming it's X.Y:
            s += ".999"
        sv = semver.Version.parse(s)
        return Version(sv.major, sv.minor, sv.patch, sv.prerelease, sv.build)

    def __str__(self):
        result = super().__str__()
        if self.patch == 999:
            return result.replace(".999", "")
        return result

    @property
    def is_snapshot(self):
        return self.prerelease == "SNAPSHOT"


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
        system_error(cmd, exit_code)


def system_error(cmd, exit_code):
    raise Exception(f"Command exited with {exit_code}: {cmd}")


def write_index_html(directory: Path, name: str, entries=None) -> Path:
    index_file = Path(directory, "index.html")
    if not entries:
        entries = get_index_entries(directory)
    lines = [f'<li><a href="{entry}/">{entry}</a></li>' for entry in entries]
    lines_txt = "\n   ".join(lines)
    content = f"""<html>
 <head>
  <title>Index of {name}</title>
 </head>
 <body>
  <h1>Index of {name}</h1>
  <ul>
   <li><a href="..">..</a></li>
   {lines_txt}
  </ul>
 </body>
</html>
"""
    with open(index_file, "w") as index:
        index.write(content)
    return index_file


def get_index_entries(directory: Path) -> List[str]:
    result = []
    for entry in os.listdir(directory):
        if entry != "index.html" and not entry.startswith("."):
            result.append(entry)
    return list(sorted(result))


def get_index_versions(directory: Path) -> List[Version]:
    result = []
    for entry in os.listdir(directory):
        if entry not in {"index.html", "current"} and not entry.startswith("."):
            result.append(entry)
    versions = [Version.parse(entry) for entry in result]
    return list(sorted(versions))
