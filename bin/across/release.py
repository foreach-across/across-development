import os
from pathlib import Path
from typing import Dict

import typer
from git import Repo

from .git import create_repos, repo_path
from .config import AcrossConfig
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
def start(repo_name: str):
    repo_name = repo_name.strip("/")  # using shell completion will often add a /
    directory, config = AcrossConfig.load()
    # TODO check for uncommitted changes in the local repo
    # TODO this should not have to read maven, except perhaps if we want to determine the repository dependencies
    # repositories = Repository.read_all(directory)
    # repos_by_name = {repo.name: repo for repo in repositories}
    repos_by_path = create_repos(directory, config.repository_names)
    repos_by_name = dict([(path.name, repo) for path, repo in repos_by_path.items()])
    repo = repos_by_name[repo_name]
    repo_versions = _determine_versions(repos_by_name)
    repo_version = repo_versions[repo_name]
    print(repo_versions)
    _write_versions_properties(repo_path(repo), config, repo_versions, repo_version)
    # TODO perform the changes in a separate repo clone
    os.chdir(repo_path(repo))
    if repo_name != "across-framework":
        _update_parent(repo_versions["across-framework"])
    _update_version_properties()
    system("git status")
    system("git diff")
    confirmed = typer.confirm(
        f"Are you sure you want to release {repo_name}:{repo_version}?"
    )
    if not confirmed:
        print("Not releasing!")
        raise typer.Abort()
    print("Releasing it!")
    # TODO: build locally
    # TODO: commit and push; this will trigger the regular build in GitLab
    # TODO: monitor the build in GitLab
    # TODO: when the build is successful: create and push tag
    # TODO: tag-triggered pipeline in GitLab will run frontend jobs + deploy to Sonatype OSS (but no other jobs)


# TODO: This is not correct: the algorithm is different for the to-be-released repository,
# and the ones that the to-be-released repository depends on.
# TODO: Perhaps a better option is to do the release with a config file, mapping each repo to a version:
# It's more explicit, less heuristics, and allows you to work in the repositories on the next branch ...
def _determine_versions(
    repos: Dict[str, Repo],
) -> Dict[str, str]:  # repo-name -> version
    for repo_name, repo in repos.items():
        print(f"Fetching from {repo_name}")
        for remote in repo.remotes:
            remote.fetch()
    result = dict()
    for repo_name, repo in repos.items():
        tags = [str(tag) for tag in repo.tags]
        print(tags)
        branch_tags = sorted(
            filter(lambda t: t.startswith(f"v{repo.active_branch}"), tags)
        )
        print(branch_tags)
        if branch_tags:
            last_tag = branch_tags[-1]
            result[repo_name] = "TODO:" + last_tag  # TODO
        else:
            result[repo_name] = f"{repo.active_branch}.0"
    print(f"Versions: {result}")
    return result


def _write_versions_properties(
    repo_path: Path,
    config: AcrossConfig,
    repo_versions: Dict[str, str],
    repo_version: str,
):
    path = Path(repo_path, "versions.properties")
    print(f"Writing {path}")
    with open(path, "w") as output:
        output.write(f"revision={repo_version}\n")
        for repo_config in config.repositories:
            new_version = repo_versions[repo_config.name]
            output.write(f"{repo_config.name}.version={new_version}\n")


def _update_parent(across_framework_version: str):
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


@app.command()
def finish():
    print(f"TODO: Finish release")


if __name__ == "__main__":
    app()
