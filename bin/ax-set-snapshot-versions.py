#!/usr/bin/env python3
import sys

import typer
from across.config import AcrossConfig
from across.git import GitRepositoryCollection
from across.maven import maven_clean_install_without_tests
from across.util import eprint

app = typer.Typer()


@app.command()
def start():
    directory, config = AcrossConfig.load()
    repo_collection = GitRepositoryCollection(directory, config)
    repo_collection.check_dirty()  # otherwise you cannot easily roll back
    snapshot_versions = repo_collection.determine_snapshot_versions()
    print("versions.properties to be fed to versions-maven-plugin:")
    snapshot_versions.write_versions_properties(sys.stdout, revision=None, prefix="   ")
    _ask_user_confirmation()
    print()
    for repository in repo_collection.repositories:
        revision = snapshot_versions.versions[repository.name]
        repository.update_gitlab_ci_variables(snapshot_versions, revision)
        maven_clean_install_without_tests()
        repository.generate_dependencies()
    repo_collection.execute_for_each("git status; git diff")
    print("Changed versions: OK")
    print("Maven build w/o tests: OK")
    print("You can always rollback using: ax-exec.sh git reset --hard")


def _ask_user_confirmation():
    confirmed = typer.confirm(
        f"Are you sure you want to set the above -SNAPSHOT versions?"
    )
    if not confirmed:
        eprint("Not setting snapshot versions!")
        raise typer.Abort()
    print("Setting snapshot versions:")


if __name__ == "__main__":
    app()
