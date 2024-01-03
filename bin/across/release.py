import os
import sys
import tempfile
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, TextIO, Union, Text

import typer
from semver import Version

from across import build
from .config import AcrossConfig
from .git import GitRepositoryCollection, GitRepository
from .util import system

app = typer.Typer()

MAVEN_VERSIONS_PLUGIN_VERSION = "2.16.2"


# @app.command()
# def start():
#     directory, config = AcrossConfig.load()
#     # TODO this should not have to read maven, except perhaps if we want do determine the repository dependencies
#     repositories = Repository.read_all(directory)
#     # for repository in repositories:
#     #     print(f"Fetching from {repository.name}")
#     #     for remote in repository.repo.remotes:
#     #         remote.fetch()
#     for repository in repositories:
#         print(f"{repository.name}: {repository.branch}")
#     # TODO: ask for confirmation that these are the right branches
#     # TODO: clone in a separate repo, and do a quick/unit-test build there
#
#     new_version = "0.0.1"
#     for repository in repositories:
#         #path = Path(repository.path, "versions.properties")
#         _write_versions_properties(repository.path, config)


@app.command()
def start(
    repo_name: str,
    stash_clone: bool = False,
):
    repo_name = repo_name.strip("/")  # using shell completion will often add a /
    directory, config = AcrossConfig.load()
    repo_collection = GitRepositoryCollection(directory, config)
    orig_repository = repo_collection.repositories_by_name[repo_name]
    if orig_repository.repo.is_dirty():
        raise Exception(f"{repo_name} is dirty")
    dependency_repos = repo_collection.find_repositories_before(repo_name)
    dirty_dependency_repos = list(filter(lambda r: r.repo.is_dirty(), dependency_repos))
    if dirty_dependency_repos:
        raise Exception(f"{[ddr.name for ddr in dirty_dependency_repos]} is dirty.")
    repo_collection.fetch_all()
    repo_versions = _determine_latest_versions(dependency_repos)
    print(repo_versions)
    repo_version = orig_repository.determine_next_version()
    _write_versions_properties(sys.stdout, repo_versions, repo_version)
    new_repository = _clone(orig_repository, stash_clone)
    _write_versions_properties(new_repository.path, repo_versions, repo_version)
    if repo_name != "across-framework":
        _update_parent(repo_versions["across-framework"])
    _update_version_properties()
    _ask_user_confirmation(repo_name, repo_version)
    _quick_local_build()
    # TODO: commit and push; this will trigger the regular build in GitLab
    # TODO: monitor the build in GitLab
    # TODO: when the build is successful: create and push tag
    # TODO: tag-triggered pipeline in GitLab will run frontend jobs + deploy to Sonatype OSS (but no other jobs)


def _determine_latest_versions(
    repositories: List[GitRepository],
) -> Dict[str, Version]:  # repo-name -> version
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
        raise Exception(f"Could not determine latest version for: {errored_repo_names}")
    return result


def _write_versions_properties(
    output_or_path: Union[Path, TextIO],
    repo_versions: Dict[str, Version],
    repo_version: Version,
):
    if isinstance(output_or_path, Path):
        directory: Path = output_or_path
        path = Path(directory, "versions.properties")
        print(f"Writing {path}")
        with open(path, "w") as output1:
            _write_versions_properties(output1, repo_versions, repo_version)
    elif isinstance(output_or_path, TextIOWrapper):
        output2: TextIO = output_or_path
        output2.write(f"revision={repo_version}\n")
        for name, version in repo_versions.items():
            output2.write(f"{name}.version={version}\n")
    else:
        raise Exception(f"Cannot write to {output_or_path.__class__}")


def _clone(orig_repository: GitRepository, stash_clone: bool) -> GitRepository:
    tmp_repo_dir = Path(tempfile.gettempdir(), "across-releases").absolute()
    if not tmp_repo_dir.exists():
        tmp_repo_dir.mkdir()
    clone_dir = Path(tmp_repo_dir, orig_repository.name)
    if clone_dir.exists():
        repository = GitRepository(orig_repository.config, clone_dir)
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
        url = orig_repository.repo.remote("origin").url
        system(f"git clone {url}")
        repository = GitRepository(orig_repository.config, clone_dir)
    os.chdir(repository.path)
    if repository.branch != orig_repository.branch:
        system(f"git checkout {orig_repository.branch}")
    system(f"git pull --ff-only")  # we don't want git pull to do a merge!
    return repository


def _update_parent(across_framework_version: Version):
    cmd = [
        "mvn",
        f"versions:{MAVEN_VERSIONS_PLUGIN_VERSION}:update-parent",
        "-DskipResolution=true",
        f"-DparentVersion={across_framework_version}",
    ]
    system(" ".join(cmd))


def _update_version_properties():
    cmd = [
        "mvn",
        f"versions:{MAVEN_VERSIONS_PLUGIN_VERSION}:set-property",
        "-DpropertiesVersionsFile=versions.properties",
    ]
    system(" ".join(cmd))


def _ask_user_confirmation(repo_name, repo_version):
    system("git status")
    system("git diff")
    confirmed = typer.confirm(
        f"Are you sure you want to release {repo_name}:{repo_version}?"
    )
    if not confirmed:
        print("Not releasing!")
        raise typer.Abort()
    print("Releasing it!")


def _quick_local_build():
    system("mvn clean package -DskipTests")


@app.command()
def poll(repo_name: str):
    build.poll(repo_name)


@app.command()
def finish():
    print(f"TODO: Finish release")


if __name__ == "__main__":
    app()
