#!/usr/bin/env python3
import sys
from pathlib import Path

import typer

from across.build import AcrossGitLab
from across.config import AcrossConfig
from across.git import GitRepositoryCollection, RepositoryVersions, ReleasePlan
from across.maven import maven_clean_install_without_tests
from across.util import system, eprint
from across.javadoc import JavadocPublisher

app = typer.Typer()


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
    repo_collection.fetch_all()  # To make sure we have all branches and tags
    repo_collection.check_release_plan(release_plan, repo_name)
    orig_repository = repo_collection.repositories_by_name[repo_name]
    ci = AcrossGitLab(repo_name)  # init early to check the GITLAB_PAT
    dependency_repos = repo_collection.find_repositories_before(repo_name)
    dependency_versions = release_plan.determine_subset(dependency_repos)
    dependency_versions.print("Dependency versions:")
    print(f"New version of {repo_name} to be released: {repo_version}")
    print("versions.properties to be fed to versions-maven-plugin:")
    dependency_versions.write_versions_properties(
        sys.stdout, repo_version, prefix="   "
    )
    print()
    new_repository = orig_repository.clone(stash_clone)
    new_repository.update_pom_files(dependency_versions, repo_version)
    _ask_user_confirmation(repo_name, repo_version)
    maven_clean_install_without_tests()
    _commit_and_build(ci, new_repository, repo_version)
    _tag_and_build(ci, new_repository, repo_version)
    print(
        "Remember to close, release and drop the staging repository at https://oss.sonatype.org/#stagingRepositories"
    )
    print(
        "But keep in mind that can be done for all releases together at the end as well."
    )
    orig_repository.fetch()


def _ask_user_confirmation(repo_name, repo_version):
    system("git status")
    system("git diff")
    confirmed = typer.confirm(
        f"Are you sure you want to release {repo_name}:{repo_version}?"
    )
    if not confirmed:
        eprint("Not releasing!")
        raise typer.Abort()
    print(f"Releasing {repo_name}:{repo_version}")


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


@app.command()
def javadoc(release_plan_path: str, push: bool = True):
    directory, config = AcrossConfig.load()
    release_plan = ReleasePlan.parse(config, Path(release_plan_path))
    release_plan.repository_versions.print("Release plan is:")
    javadoc = JavadocPublisher(config, release_plan, push)
    javadoc.publish()
    if push:
        print("Check the deploy progress at: https://github.com/foreach-across/api-docs-5/settings/pages")


if __name__ == "__main__":
    app()
