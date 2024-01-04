#!/usr/bin/env python3

import typer
from across.config import AcrossConfig

app = typer.Typer(
    help="List repository or module names, for use in shell scripts such as ax-exec.sh"
)


@app.command(help="List git repository names")
def repositories():
    _, config = AcrossConfig.load()
    for repo_config in config.repositories:
        print(repo_config.name)


@app.command(help="List modules names")
def modules(with_repo: bool = False):
    _, config = AcrossConfig.load()
    for repo_config in config.repositories:
        for module_name in repo_config.modules:
            if with_repo:
                line = f"{repo_config.name}/{module_name}"
            else:
                line = module_name
            print(line)


if __name__ == "__main__":
    app()
