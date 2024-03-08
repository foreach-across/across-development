---
title: Tips and tricks
weight: 40
toc: true
---

Some tips and tricks for maintaining Across.

<!--more-->


## ax-exec.sh

You can use this script to run a command in each of the 7
repositories, for instance:

	ax-exec.sh git status
	ax-exec.sh git fetch -p
	ax-exec.sh git pull --ff-only

Danger zone: If you want to "undo" everything in all 7 repositories:

	ax-exec.sh git reset --hard


## ax-set-snapshot-versions.py

This script looks at the current branch of each of the 7 repositories,
and updates the `pom.xml` files of each repository to use the right
snapshot version for that repository, and its dependencies. E.g. if
your current branches are:

    across-framework.version:            5.4
    across-autoconfigure.version:        2.4
    across-base-modules.version:         4.4
    across-entity-admin-modules.version: 4.4
    across-user-auth-modules.version:    4.4
    across-media-modules.version:        6.4
    across-platform.version:             5.4

Then the script will propose this:

    across-framework.version=5.4-SNAPSHOT
    across-autoconfigure.version=2.4-SNAPSHOT
    across-base-modules.version=4.4-SNAPSHOT
    across-entity-admin-modules.version=4.4-SNAPSHOT
    across-user-auth-modules.version=4.4-SNAPSHOT
    across-media-modules.version=6.4-SNAPSHOT
    across-platform.version=5.4-SNAPSHOT
    Are you sure you want to set the above -SNAPSHOT versions? [y/N]:

There are two use cases for this:

- You've started a new branch.

- You've finished a release, and now need to [reset the revision back
  to --SNAPSHOT]({{< ref
  "release-procedure#reset-versions-to---snapshot" >}}).
