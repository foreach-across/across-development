---
title: Regular maintenance
weight: 90
toc: true
---

## GitHub sync token rotation

The internal GitLab repositories are automatically synched to
GitHub. The GitHub personal access token for that sync is valid for
maximum 1 year, so it needs be rolled over regularly.

For documentation to configure the sync, see:

- https://docs.gitlab.com/ee/user/project/repository/mirror/
- https://docs.gitlab.com/ee/user/project/repository/mirror/push.html
- https://docs.gitlab.com/ee/user/project/repository/mirror/push.html#set-up-a-push-mirror-from-gitlab-to-github


## GPG key rotation

The current Across GPG key will expire on 2025-06-06.
