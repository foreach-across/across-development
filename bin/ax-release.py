#!/usr/bin/env python3

import os
import sys
import tempfile
from pathlib import Path

import typer
from git import Repo
from git.objects import Commit
from semver import Version

from across import build
from across.build import poll_gitlab_pipeline
from across.config import AcrossConfig
from across.git import GitRepositoryCollection, GitRepository, RepositoryVersions
from across.util import system, eprint

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
    release_plan_path: str,
    repo_name: str,
    stash_clone: bool = False,
):
    repo_name = repo_name.strip("/")  # using shell completion will often add a /
    directory, config = AcrossConfig.load()
    release_plan = RepositoryVersions.parse(config, Path(release_plan_path))
    release_plan.print("Release plan is:")
    repo_collection = GitRepositoryCollection(directory, config)
    repo_collection.check_release_plan(release_plan, repo_name)
    orig_repository = repo_collection.repositories_by_name[repo_name]
    if orig_repository.repo.is_dirty():
        raise Exception(f"{repo_name} is dirty")
    dependency_repos = repo_collection.find_repositories_before(repo_name)
    dirty_dependency_repos = list(filter(lambda r: r.repo.is_dirty(), dependency_repos))
    if dirty_dependency_repos:
        raise Exception(f"{[ddr.name for ddr in dirty_dependency_repos]} is dirty.")
    repo_collection.fetch_all()
    # TODO: if the release plan is a partial plan, then we still need this:
    # latest_versions = RepositoryVersions.latest_versions(dependency_repos)
    # latest_versions.print("Latest versions of dependencies:")
    dependency_versions = release_plan.determine_subset(dependency_repos)
    dependency_versions.print("Dependency versions:")
    # repo_version = orig_repository.determine_next_version()
    repo_version = release_plan.versions[repo_name]
    print(f"New version of {repo_name} to be released: {repo_version}")
    print("versions.properties to be fed to versions-maven-plugin:")
    dependency_versions.write_versions_properties(
        sys.stdout, repo_version, prefix="   "
    )
    print()
    new_repository = _clone(orig_repository, stash_clone)
    dependency_versions.write_versions_properties(new_repository.path, repo_version)
    if repo_name != "across-framework":
        # The parent pom of across-framework is Spring Boot, so nothing to do in that case.
        # For all other repositories, the parent pom is across-framework:
        _update_parent(dependency_versions.versions["across-framework"])
    _update_version_properties()
    _ask_user_confirmation(repo_name, repo_version)
    _quick_local_build()
    msg = f"Release {repo_version} by across.py release"
    commit = _commit_and_push(new_repository.repo, msg)
    print("commit: ", commit.hexsha)
    pipeline = poll_gitlab_pipeline(repo_name, commit.hexsha)
    print(f"pipeline: {pipeline.status}")
    # TODO: when the build is successful: create and push tag
    # TODO: tag-triggered pipeline in GitLab will run frontend jobs + deploy to Sonatype OSS (but no other jobs)


def _clone(orig_repository: GitRepository, stash_clone: bool) -> GitRepository:
    tmp_repo_dir = Path(tempfile.gettempdir(), "across-releases").absolute()
    if not tmp_repo_dir.exists():
        tmp_repo_dir.mkdir()
    clone_dir = Path(tmp_repo_dir, orig_repository.name)
    if clone_dir.exists():
        repository = GitRepository(orig_repository.config, clone_dir)
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
        eprint("Not releasing!")
        raise typer.Abort()
    print("Releasing it!")


def _quick_local_build():
    system("mvn clean package -DskipTests")


def _commit_and_push(repo: Repo, msg: str) -> Commit:
    repo.git.add(update=True)  # git add -u
    commit = repo.index.commit(msg)
    repo.remote("origin").push()
    return commit


@app.command()
def poll(repo_name: str):
    build.poll_gitlab_pipeline(
        repo_name.strip("/"), "fb1757a257ce469c63ee29efb9f90c062cbcc94c"
    )


@app.command()
def finish():
    print(f"TODO: Finish release")


if __name__ == "__main__":
    app()
