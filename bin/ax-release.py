#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Optional, Annotated

import typer

from across.build import AcrossGitLab
from across.config import AcrossConfig
from across.git import GitRepositoryCollection, RepositoryVersions, ReleasePlan
from across.maven import maven_clean_install_without_tests
from across.util import system, eprint
from across.javadoc import JavadocPublisher
from across.util import Version

app = typer.Typer()


@app.command()
def start(
    release_plan_path: str,
    repo_name: Annotated[Optional[str], typer.Argument()] = None,
    all: bool = False,
    from_repo: Optional[str] = None,
    stash_clone: bool = False,
):
    _check_options(all, from_repo, repo_name)
    directory, config = AcrossConfig.load()
    release_plan = RepositoryVersions.parse(config, Path(release_plan_path))
    release_plan.print("Release plan is:")
    repo_collection = GitRepositoryCollection(directory, config)
    repo_collection.fetch_all()  # To make sure we have all branches and tags
    releasers = _releasers(
        release_plan, repo_collection, repo_name, from_repo, stash_clone
    )
    # We want to perform each step for all repositories, then ask for confirmation for all repositories,
    # and only then start the actual release procedure for the first repository and the next, ...!
    for r in releasers:
        r.check()
    for r in releasers:
        r.prepare()
    for r in releasers:
        if not r.ask_confirmation():
            eprint("Not releasing!")
            raise typer.Exit(3)
    for r in releasers:
        r.execute()
    print(
        "Remember to close, release and drop the staging repository at https://oss.sonatype.org/#stagingRepositories"
    )
    print(
        "But keep in mind that can be done for all releases together at the end as well."
    )


def _check_options(all, from_repo, repo_name):
    if not repo_name and not from_repo and not all:
        sys.stderr.write(
            "You must either pass a repository name, or --all to release all repositories, or --from-repo to (re)start from a repo in the middle.\n"
        )
        raise typer.Exit(1)
    if repo_name and all:
        sys.stderr.write("--all cannot be combined with a specific repository\n")
        raise typer.Exit(2)
    if from_repo and all:
        sys.stderr.write("--all cannot be combined with --from-repo\n")
        raise typer.Exit(3)


def _releasers(
    release_plan: RepositoryVersions,
    repo_collection: GitRepositoryCollection,
    repo_name: Optional[str],
    from_repo: Optional[str],
    stash_clone,
):
    if repo_name:
        repo_name = repo_name.strip("/")  # using shell completion will often add a /
        releasers = [
            RepoReleaser(release_plan, repo_collection, repo_name, stash_clone)
        ]
    elif from_repo:
        from_repo = from_repo.strip("/")  # using shell completion will often add a /
        releasers = [
            RepoReleaser(release_plan, repo_collection, repo_name, stash_clone)
            for repo_name in release_plan.repo_names
            if release_plan.repo_names.index(repo_name)
            >= release_plan.repo_names.index(from_repo)
        ]
        # print([rel.repo_name for rel in releasers])
    else:
        releasers = [
            RepoReleaser(release_plan, repo_collection, repo_name, stash_clone)
            for repo_name in release_plan.repo_names
        ]
    return releasers


class RepoReleaser:
    def __init__(
        self,
        release_plan: RepositoryVersions,
        repo_collection: GitRepositoryCollection,
        repo_name: str,
        stash_clone: bool,
    ):
        self.release_plan: RepositoryVersions = release_plan
        self.repo_collection: GitRepositoryCollection = repo_collection
        self.repo_name: str = repo_name
        self.repo_version: Version = release_plan.versions[repo_name]
        self.stash_clone: bool = stash_clone
        self.orig_repository = repo_collection.repositories_by_name[repo_name]
        self.ci = AcrossGitLab(repo_name)  # init early to check the GITLAB_PAT
        self.new_repository = None

    def __str__(self):
        return f"RepoReleaser[{self.repo_name}:{self.repo_version}]"

    def check(self):
        self.repo_collection.check_release_plan(self.release_plan, self.repo_name)

    def prepare(self):
        print("Preparing to release:", self.repo_name + ":" + str(self.repo_version))
        dependency_repos = self.repo_collection.find_repositories_before(self.repo_name)
        dependency_versions = self.release_plan.determine_subset(dependency_repos)
        dependency_versions.print("Dependency versions:")
        print()
        self.new_repository = self.orig_repository.clone(self.stash_clone)
        variables = self.new_repository.update_gitlab_ci_variables(
            dependency_versions, self.repo_version
        )
        self.new_repository.run_ci_before(variables)
        # must be before generate_dependencies(), otherwise the release version doesn't exist yet:
        maven_clean_install_without_tests()
        self.new_repository.generate_dependencies()
        self.new_repository.undo_pom_changes()  # because we don't want to commit these

    def ask_confirmation(self) -> bool:
        self._chdir()
        print()
        print(f"git status: {self.repo_name}:")
        system("git status")
        # Exclude the dependency.list|tree.txt files, because:
        # - They make the diff too big to quickly and confidently make the yes/no decision.
        # - And I'm confident enough that those dependency.*.txt work correctly.
        print(f"git diff (excluding dependency.*.txt): {self.repo_name}:")
        system("git diff ':^dependency.*.txt' ':^*/dependency.*.txt'")
        return typer.confirm(
            f"Are you sure you want to release {self.repo_name}:{self.repo_version}?"
        )

    def execute(self):
        self._chdir()
        print(f"Releasing {self.repo_name}:{self.repo_version}")
        self._commit_and_build()
        self._tag_and_build()
        self.orig_repository.fetch()

    def set_to_snapshot(self):
        self._chdir()
        print(f"Setting to snapshot {self.repo_name}:{self.repo_version}")
        self._commit_and_build()
        self.orig_repository.fetch()

    def _commit_and_build(self):
        commit = self.new_repository.commit_and_push(self.repo_version)
        print("Commit:", commit.hexsha)
        commit_pipeline = self.ci.poll_commit_pipeline(commit)
        print("Commit pipeline:", commit_pipeline.status)
        if commit_pipeline.status != "success":
            raise Exception(
                f"Commit pipeline ended with status: {commit_pipeline.status}"
            )

    def _tag_and_build(self):
        tag = self.new_repository.tag_and_push(self.repo_version)
        print("Tag:", tag.name)
        tag_pipeline = self.ci.poll_tag_pipeline(tag)
        print("Tag pipeline:", tag_pipeline.status)
        if tag_pipeline.status != "success":
            raise Exception(f"Tag pipeline ended with status: {tag_pipeline.status}")

    def _chdir(self):
        os.chdir(self.new_repository.path)


# @app.command()
# def poll(repo_name: str):
#     build.poll_gitlab_pipeline(
#         repo_name.strip("/"), "fb1757a257ce469c63ee29efb9f90c062cbcc94c"
#     )


@app.command()
def finish(
    release_plan_path: str,
    repo_name: Annotated[Optional[str], typer.Argument()] = None,
    all: bool = False,
    from_repo: Optional[str] = None,
    stash_clone: bool = False,
):
    _check_options(all, from_repo, repo_name)
    directory, config = AcrossConfig.load()
    # release_plan = RepositoryVersions.parse(config, Path(release_plan_path))
    # release_plan.print("Release plan is:")
    repo_collection = GitRepositoryCollection(directory, config)
    repo_collection.fetch_all()  # To make sure we have all branches and tags
    repo_collection.check_dirty()  # otherwise you cannot easily roll back
    snapshot_versions = repo_collection.determine_snapshot_versions()
    releasers = _releasers(
        snapshot_versions, repo_collection, repo_name, from_repo, stash_clone
    )
    # We want to perform each step for all repositories, then ask for confirmation for all repositories,
    # and only then start the actual procedure for the first repository and the next, ...!
    for r in releasers:
        r.check()
    for r in releasers:
        r.prepare()
    for r in releasers:
        if not r.ask_confirmation():
            eprint("Not setting snapshot!")
            raise typer.Exit(3)
    for r in releasers:
        r.set_to_snapshot()


@app.command()
def javadoc(release_plan_path: str, push: bool = True):
    directory, config = AcrossConfig.load()
    release_plan = ReleasePlan.parse(config, Path(release_plan_path))
    release_plan.repository_versions.print("Release plan is:")
    javadoc = JavadocPublisher(config, release_plan, push)
    javadoc.publish()
    if push:
        print(
            "Check the deploy progress at: https://github.com/foreach-across/api-docs-5/settings/pages"
        )


if __name__ == "__main__":
    app()
