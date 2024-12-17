#!/usr/bin/env python3

import typer
from across.config import AcrossConfig

app = typer.Typer(
    help="List repository or module names, for use in shell scripts such as ax-exec.sh"
)


@app.command(help="List git repository names")
def repositories(deleted: bool = False):
    _, config = AcrossConfig.load()
    for repo_config in config.repositories:
        if not repo_config.deleted or deleted:
            print(repo_config.id, end='\n')


@app.command(help="List modules names")
def modules(with_repo: bool = False, deleted: bool = False):
    _, config = AcrossConfig.load()
    for repo_config in config.repositories:
        if not repo_config.deleted or deleted:
            for module in repo_config.modules:
                if with_repo:
                    line = f"{repo_config.id}/{module.id}"
                else:
                    line = module.id
                print(line, end='\n')


if __name__ == "__main__":
    app()
