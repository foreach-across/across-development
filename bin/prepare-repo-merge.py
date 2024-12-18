#!/usr/bin/env python3
import os.path
import sys

from git import Repo

TMP_DIR = "/tmp/repo-merge"

GROUP_MODULES = {
    "across-base-modules": [
        "across-hibernate-module",
        "spring-security-module",
        "debug-web-module",
        "logging-module",
        "ehcache-module",
        # "spring-batch-module",
        # "spring-mobile-module",
    ],
    "across-entity-admin-modules": [
        "admin-web-bootstrap-4",  # The dependency on file-manager-module should be easy to break
        "bootstrap-ui-module",
        "admin-web-module",
        "entity-ui-module",
        "properties-module",
        "application-info-module",
    ],
    "across-user-auth-modules": [
        "spring-security-acl-module",
        "user-module",
        "ldap-module",
        "oauth2-module",
    ],
}


def main(group_repo_name: str):
    module_repo_names = GROUP_MODULES[group_repo_name]
    print(f"{group_repo_name}: {module_repo_names}")
    # if os.path.exists(TMP_DIR):
    #     shutil.rmtree(TMP_DIR)
    group_repo_url = f"https://gitlab.eindhoven.io-internal.dev/antwerpen/across/{group_repo_name}.git"
    os.makedirs(TMP_DIR, exist_ok=True)
    for module_repo_name in module_repo_names:
        handle_module_repo(group_repo_name, group_repo_url, module_repo_name)


def handle_module_repo(group_repo_name, group_repo_url, module_repo_name):
    print(f"Handling {module_repo_name}:")
    os.chdir(TMP_DIR)
    module_repo_dir = os.path.join(TMP_DIR, module_repo_name + ".git")
    module_repo_url = f"https://bitbucket.org/beforeach/{module_repo_name}.git"
    if not os.path.exists(module_repo_dir):
        _system(f"git clone --bare {module_repo_url}")
    # os.chdir(module_repo_dir)
    # _system("git branch")
    # _system("git tag")
    repo = Repo(module_repo_dir)
    try:
        remote = repo.remote(group_repo_name)
    except Exception:
        remote = repo.create_remote(group_repo_name, group_repo_url)
    for tag in repo.tags:
        if tag.name.startswith("across-standard-modules-"):
            print(f"  Skipping tag: {tag}")
        else:
            print(f"  Pushing tag {tag} to {group_repo_url}")
            remote.push(tag.name)
    for head in repo.heads:
        new_branch_name = f"{module_repo_name}-{head.name}"
        ref_spec = f"{head.name}:{new_branch_name}"
        print(f"  Pushing {ref_spec} to {group_repo_url}")
        remote.push(ref_spec)


def _system(cmd):
    code = os.system(cmd)
    if code != 0:
        raise (Exception(f"{cmd}: exit code: {code}"))


if __name__ == "__main__":
    main(sys.argv[1])
