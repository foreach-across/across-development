from pathlib import Path
from typing import Dict, Sequence

import typer

from .config import AcrossConfig
from .repository import Repository

app = typer.Typer()


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
    # TODO this should not have to read maven, except perhaps if we want do determine the repository dependencies
    repositories = Repository.read_all(directory)
    repos_by_name = {repo.name: repo for repo in repositories}
    repository = repos_by_name[repo_name]
    versions_by_repo_name = determine_versions(repositories)
    print(versions_by_repo_name)

    _write_versions_properties(repository.path, config)

    # We'll need to execute two maven commands:
    # mvn versions:2.16.2:update-parent -DskipResolution=true -DparentVersion=5.3.0-alpha-1
    # mvn versions:2.16.2:set-property -DpropertiesVersionsFile=versions.properties
    # Take care of the particular structure in across-autoconfigure with the test-projects
    # We should just include all those test-projects in the top-level pom


def determine_versions(repositories: Sequence[Repository]) -> Dict[str, str]:  # repo-name -> version
    for repository in repositories:
        print(f"Fetching from {repository.name}")
        for remote in repository.repo.remotes:
            remote.fetch()
    result = dict()
    for repository in repositories:
        tags = [str(tag) for tag in repository.repo.tags]
        print(tags)
        branch_tags = sorted(filter(lambda t: t.startswith(f"v{repository.branch}"), tags))
        print(branch_tags)
        if branch_tags:
            last_tag = branch_tags[-1]
            result[repository.name] = "TODO:" + last_tag  # TODO
        else:
            result[repository.name] = f"v{repository.branch}.0"
    return result


def _write_versions_properties(repo_path: Path, config: AcrossConfig):
    new_version = "0.0.1"
    path = Path(repo_path, "versions.properties")
    print(f"Writing {path}")
    with open(path, "w") as output:
        for repo_config in config.repositories:
            output.write(f"{repo_config.name}.version={new_version}\n")


@app.command()
def finish():
    print(f"TODO: Finish release")


if __name__ == "__main__":
    app()
