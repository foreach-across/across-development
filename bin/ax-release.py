#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import typer
from semver import Version

from across.build import AcrossGitLab
from across.config import AcrossConfig
from across.git import GitRepositoryCollection, RepositoryVersions, GitRepository
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
    # repo_version = orig_repository.determine_next_version()
    repo_version = release_plan.versions[repo_name]
    print("Going to release:", repo_name + ":" + str(repo_version))
    repo_collection.fetch_all()
    repo_collection.check_release_plan(release_plan, repo_name)
    orig_repository = repo_collection.repositories_by_name[repo_name]
    if orig_repository.repo.is_dirty():
        raise Exception(f"{repo_name} is dirty")
    ci = AcrossGitLab(repo_name)  # init early to check the GITLAB_PAT
    dependency_repos = repo_collection.find_repositories_before(repo_name)
    # dirty_dependency_repos = list(filter(lambda r: r.repo.is_dirty(), dependency_repos))
    # if dirty_dependency_repos:
    #     raise Exception(f"{[ddr.name for ddr in dirty_dependency_repos]} is dirty.")
    # TODO: if the release plan is a partial plan, then we still need this:
    # latest_versions = RepositoryVersions.latest_versions(dependency_repos)
    # latest_versions.print("Latest versions of dependencies:")
    dependency_versions = release_plan.determine_subset(dependency_repos)
    dependency_versions.print("Dependency versions:")
    print(f"New version of {repo_name} to be released: {repo_version}")
    print("versions.properties to be fed to versions-maven-plugin:")
    dependency_versions.write_versions_properties(
        sys.stdout, repo_version, prefix="   "
    )
    print()
    new_repository = orig_repository.clone(stash_clone)
    _update_pom_files(new_repository, dependency_versions, repo_version)
    _ask_user_confirmation(repo_name, repo_version)
    _quick_local_build()
    _commit_and_build(ci, new_repository, repo_version)
    _tag_and_build(ci, new_repository, repo_version)
    print(
        "Remember to close, release and drop the staging repository at https://oss.sonatype.org/#stagingRepositories"
    )
    print(
        "But keep in mind that can be done for all releases together at the end as well."
    )
    orig_repository.fetch()


def _update_pom_files(
    repository: GitRepository, dependency_versions: RepositoryVersions, new_version
):
    version_properties_path = dependency_versions.write_versions_properties(
        repository.path.parent, new_version
    )
    across_framework_version = dependency_versions.versions["across-framework"]
    if repository.name == "across-platform":
        os.chdir(Path(repository.path, "across-platform-dependencies"))
        _update_parent(across_framework_version)
        os.chdir(repository.path)
    elif repository.name != "across-framework":
        # The parent pom of across-framework is Spring Boot, so nothing to do in that case.
        # For all other repositories, the parent pom is across-framework:
        _update_parent(across_framework_version)
    _update_version_properties(version_properties_path)


def _update_parent(across_framework_version: Version):
    cmd = [
        "mvn",
        f"versions:{MAVEN_VERSIONS_PLUGIN_VERSION}:update-parent",
        "-DskipResolution=true",
        f"-DparentVersion={across_framework_version}",
    ]
    system(" ".join(cmd))


def _update_version_properties(path: Path):
    cmd = [
        "mvn",
        f"versions:{MAVEN_VERSIONS_PLUGIN_VERSION}:set-property",
        f"-DpropertiesVersionsFile={path}",
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


def _commit_and_build(ci, new_repository, repo_version):
    commit = new_repository.commit_and_push(repo_version)
    print("Commit:", commit.hexsha)
    commit_pipeline = ci.poll_commit_pipeline(commit)
    print("Commit pipeline:", commit_pipeline.status)
    if commit_pipeline.status != "success":
        raise Exception(f"Commit pipeline ended with status: {commit_pipeline.status}")


def _tag_and_build(ci, new_repository, repo_version):
    tag = new_repository.tag_and_push(repo_version)
    print("Tag:", tag.name)
    tag_pipeline = ci.poll_tag_pipeline(tag)
    print("Tag pipeline:", tag_pipeline.status)
    if tag_pipeline.status != "success":
        raise Exception(f"Tag pipeline ended with status: {tag_pipeline.status}")


# @app.command()
# def poll(repo_name: str):
#     build.poll_gitlab_pipeline(
#         repo_name.strip("/"), "fb1757a257ce469c63ee29efb9f90c062cbcc94c"
#     )


@app.command()
def finish():
    print(f"TODO: Finish release")


if __name__ == "__main__":
    app()
