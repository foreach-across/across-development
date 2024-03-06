---
title: Regular maintenance
weight: 90
toc: true
---

This page describes regular maintenance that needs to be performed,
such as rotating tokens and keys.

<!--more-->


## GitHub sync token rotation

The internal GitLab repositories are automatically synched to
GitHub. The GitHub personal access token for that sync is valid for
maximum 1 year, so it needs be rolled over regularly.

For documentation to configure the sync, see:

- https://docs.gitlab.com/ee/user/project/repository/mirror/
- https://docs.gitlab.com/ee/user/project/repository/mirror/push.html
- https://docs.gitlab.com/ee/user/project/repository/mirror/push.html#set-up-a-push-mirror-from-gitlab-to-github

The current token will expire on 2025-03-01.

The `ax-github-mirror.py` script can be used to configure/update the
mirroring.


## GPG key rotation

The current Across GPG key will expire on 2025-06-06.
