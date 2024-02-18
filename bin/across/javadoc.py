import os
import tempfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

from git import Repo

from .config import AcrossConfig
from .git import ReleasePlan
from .maven import Artifact
from .util import system

API_DOCS_GIT_URL = "git@github.com:foreach-across/api-docs-5.git"


class JavadocPublisher:
    def __init__(self, config: AcrossConfig, release_plan: ReleasePlan):
        self.config = config
        self.release_plan = release_plan
        self.tmp_dir = Path(tempfile.gettempdir(), "across-api-docs").absolute()
        if not self.tmp_dir.exists():
            self.tmp_dir.mkdir()
        self.cache_dir = Path(self.tmp_dir, "cache")
        if not self.cache_dir.exists():
            self.cache_dir.mkdir()
        self.repo_dir = Path(self.tmp_dir, "api-docs-5")

    def publish(self):
        repo = self.clone()
        release_name = self.release_plan.name
        print(release_name)
        commit_msg = f"Javadocs from release plan: {release_name}:\n"
        for repo_name, version in self.release_plan.versions.items():
            repo_config = self.config[repo_name]
            for module in repo_config.modules:
                artifact = Artifact.of(repo_config, module, version)
                if (
                    artifact.artifact_id == "ax-bootstrap-4-utilities"
                    or artifact.is_pom
                ):
                    print(f"{artifact}: Skipping because it does not have javadocs")
                else:
                    print(artifact)
                    self._publish_artifact(artifact, repo)
                    commit_msg += f"\n{artifact}"
        for group_id in self.config.group_ids:
            index_file = _write_index_html(Path(group_id), f"/{group_id}")
            repo.git.add(index_file)
        index_file = _write_index_html(Path(), f"/")
        repo.git.add(index_file)
        # print(comment)
        repo.git.commit("-m", commit_msg)
        repo.git.gc("--aggressive", "--keep-largest-pack")
        repo.remote("origin").push()
        tag_msg = f"Release plan {release_name} by ax-release.py"
        tag = repo.create_tag(f"v{release_name}", message=tag_msg)
        repo.remote("origin").push(tag.name)

    def clone(self) -> Repo:
        clone_dir = self.repo_dir
        if clone_dir.exists():
            repo = Repo(clone_dir)
            # TODO: also check for unpushed commits!
            if repo.is_dirty():
                repo.git.stash()
                # raise Exception(f"Clone dir is dirty: {clone_dir}")
            for remote in repo.remotes:
                remote.fetch()
        else:
            os.chdir(self.tmp_dir)
            system(f"git clone {API_DOCS_GIT_URL}")
            repo = Repo(clone_dir)
        os.chdir(clone_dir)
        system("git config gc.autoDetach false")
        if repo.active_branch.name != "main":
            system(f"git checkout main")
        system(f"git pull --ff-only")  # we don't want git pull to do a merge!
        return repo

    def _cache_javadoc_jar(self, artifact: Artifact) -> Path:
        path = Path(self.cache_dir, artifact.javadoc_jar_name)
        if path.exists():  # TODO should check checksum
            print(f"{path}: up to date")
        else:
            url = artifact.javadoc_jar_url
            urlretrieve(url, path)
            print(f"{path}: downloaded from {url}")
        return path

    def _publish_artifact(self, artifact: Artifact, repo: Repo):
        jar_file = self._cache_javadoc_jar(artifact)
        artifact_dir = Path(
            self.repo_dir,
            artifact.group_id,
            artifact.artifact_id,
        )
        version_dir = Path(
            artifact_dir,
            str(artifact.version),
        )
        with zipfile.ZipFile(jar_file, "r") as zip:
            zip.extractall(version_dir)
        repo.git.add(version_dir)
        index_file = _write_index_html(
            artifact_dir, f"/{artifact.group_id}/{artifact.artifact_id}"
        )
        repo.git.add(index_file)


def _write_index_html(directory: Path, name: str) -> Path:
    index_file = Path(directory, "index.html")
    lines = []
    for entry in os.listdir(directory):
        if entry != "index.html" and not entry.startswith("."):
            lines.append(f'<li><a href="{entry}">{entry}</a></li>')
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
