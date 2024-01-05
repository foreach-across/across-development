import os
import sys
from time import sleep

from git import Tag
from git.objects import Commit

import gitlab
from gitlab.v4.objects import ProjectPipeline

from across.util import eprint

GITLAB_PAT = "GITLAB_PAT"


class AcrossGitLab:
    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        pat = os.environ.get(GITLAB_PAT)
        if not pat:
            raise Exception(
                f"Environment variable {GITLAB_PAT} (personal access token) is not set."
            )
        self.gitlab = gitlab.Gitlab(
            url="https://gitlab.isaac.nl",  # TODO remove hardcoded URL
            private_token=pat,
            user_agent="antwerpen/across.py",
        )
        # print(gl.url)
        # Will shown credentials so disable again:
        # gl.enable_debug()
        self.gitlab.auth()
        # TODO remove hardcoded group name:
        self.project = self.gitlab.projects.get(f"antwerpen/across/{self.repo_name}")
        # print(project.to_json(indent="  "))

    def poll_commit_pipeline(self, commit: Commit) -> ProjectPipeline:
        id = self._find_pipeline_id(sha=commit.hexsha)
        return self._poll_pipeline(id)

    def poll_tag_pipeline(self, tag: Tag) -> ProjectPipeline:
        id = self._find_pipeline_id(ref=tag.name)
        return self._poll_pipeline(id)

    def _find_pipeline_id(self, sha=None, ref=None):
        if not sha and not ref:
            raise Exception("Must specify at least sha or ref")
        sleep(10)
        while True:
            pipelines = list(
                self.project.pipelines.list(sha=sha, ref=ref, order_by="id")
            )
            if pipelines:
                # We assume the pipeline with the highest id is the one we need.
                # Note that the GitLab API order_by is descending by default:
                return pipelines[0].id
            print("No pipeline yet for:", sha if sha else ref)
            sleep(10)

    def _poll_pipeline(self, id) -> ProjectPipeline:
        # and now we have to poll until it's finished
        pipeline = self.project.pipelines.get(id)
        print("You can follow the build at:", pipeline.web_url)
        while pipeline.status not in {"success", "failed", "canceled", "skipped"}:
            print("status:", pipeline.status)
            sleep(10)
            pipeline = self.project.pipelines.get(id)
        print(pipeline.to_json(indent="  "))
        return pipeline
