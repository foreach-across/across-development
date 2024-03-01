#!/usr/bin/env python3
import os
import pprint

import gitlab
import typer

from across.build import GITLAB_PAT
from across.config import AcrossConfig

GITHUB_PAT = "GITHUB_PAT"

app = typer.Typer(
    help="List repository or module names, for use in shell scripts such as ax-exec.sh"
)


@app.command(help="Configure mirroring to the public GitHub repositories")
def configure(gh_user_name: str):
    pat = os.environ.get(GITLAB_PAT)
    if not pat:
        raise Exception(
            f"Environment variable {GITLAB_PAT} (personal access token) is not set."
        )
    gh_pat = os.environ.get(GITHUB_PAT)
    if not gh_pat:
        raise Exception(
            f"Environment variable {GITHUB_PAT} (personal access token) is not set."
        )
    _, config = AcrossConfig.load()
    gl = gitlab.Gitlab(
        url="https://gitlab.isaac.nl",  # TODO remove hardcoded URL
        private_token=pat,
        user_agent="antwerpen/across.py",
    )
    gl.auth()
    for repo_config in config.repositories:
        print(repo_config.id)
        repo_name = repo_config.id
        _update_repo(gl, repo_name, gh_pat, gh_user_name)
    _update_repo(gl, "across-development", gh_pat, gh_user_name)


def _update_repo(gl, repo_name, gh_pat, gh_user_name):
    project = gl.projects.get(f"antwerpen/across/{repo_name}")
    mirror_mgr = project.remote_mirrors
    gh_url = (
        f"https://{gh_user_name}:{gh_pat}@github.com/foreach-across/{repo_name}.git"
    )
    result = None
    for m in mirror_mgr.list():
        if "/foreach-across/" in m.url:
            result = mirror_mgr.update(m.id, url=gh_url)
        else:
            print(m.url)
    if not result:
        result = mirror_mgr.create(
            {
                "url": gh_url,
                "enabled": True,
                "auth_method": "password",
            }
        )
    pprint.pp(result)


if __name__ == "__main__":
    app()
