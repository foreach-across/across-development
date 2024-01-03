import os
import sys
from time import sleep

import gitlab
from gitlab.v4.objects import ProjectPipeline


def poll_gitlab_pipeline(repo_name: str, commit_sha: str) -> ProjectPipeline:
    # directory, config = AcrossConfig.load()
    sleep(10)

    pat = os.environ["GITLAB_PAT"]
    # print(len(pat))
    gl = gitlab.Gitlab(
        url="https://gitlab.isaac.nl",
        private_token=pat,
        user_agent="antwerpen/across.py",
    )
    # print(gl.url)
    # Will shown credentials so disable again:
    # gl.enable_debug()
    gl.auth()

    project = gl.projects.get(f"antwerpen/across/{repo_name}")
    # print(project.to_json())
    pipelines = list(project.pipelines.list(sha=commit_sha, order_by="id"))
    while not pipelines:
        sys.stderr.write(f"No pipeline yet for {commit_sha}\n")
        sleep(10)

    pipeline = pipelines[-1]
    id = pipeline.id
    # and now we have to poll until it's finished
    pipeline = project.pipelines.get(id)
    sys.stderr.write(f"You can follow the build at: {pipeline.web_url}\n")
    while pipeline.status not in {"success", "failed", "canceled", "skipped"}:
        sys.stderr.write(f"status: {pipeline.status}\n")
        sleep(10)
        pipeline = project.pipelines.get(id)
    print(pipeline.to_json())
    return pipeline
