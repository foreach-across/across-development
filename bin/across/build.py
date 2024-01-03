import os
from time import sleep

import gitlab
from gitlab.v4.objects import ProjectPipeline


def poll(repo_name: str) -> ProjectPipeline:
    # directory, config = AcrossConfig.load()

    pat = os.environ["GITLAB_PAT"]
    # print(len(pat))
    gl = gitlab.Gitlab(
        url="https://gitlab.isaac.nl",
        private_token=pat,
        user_agent="antwerpen/across.py",
    )
    # print(gl.url)
    # TODO: will shown credentials so disable again:
    gl.enable_debug()
    gl.auth()

    project = gl.projects.get("antwerpen/across/across-framework")
    # print(project.to_json())
    # We should know the commit sha of the commit we just created/pushed:
    pipelines = project.pipelines.list(
        sha="414d5e4f2312d964533d49a3f68f764c40d52b75", order_by="id"
    )
    pipeline = list(pipelines)[-1]
    id = pipeline.id
    # and now we have to poll until it's finished
    pipeline = project.pipelines.get(id)
    print(pipeline.to_json())
    while pipeline.status not in {"success", "failed", "canceled", "skipped"}:
        print("status: %s", pipeline.status)
        sleep(10)
        pipeline = project.pipelines.get(id)
    return pipeline
