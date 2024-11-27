---
title: Starting a new release
weight: 30
toc: true
---

This page describes the various steps that are usually required to
start a new X.Y version.

<!--more-->

## Create a new branch

These instrucctions assume 6.x, where framework, platform and all
modules all have the same version. For 5.x you'll have a much harder
time.

The example here is for 6.0 -> 6.1, but adapt as needed of course.

1. Make sure your repositories are clean: no uncommitted files and no
   unpushed commits etc.

2. Make sure all your repositories are up to date (or actually better,
   clone a fresh top-level `across-development` repo, and the child
   repos, as explained in [Getting started](getting-started.md)):

        ax-exec.sh git fetch -p

3. For example for starting 6.1 from the latest commit on the 6.0 branch:

		ax-exec.sh git checkout -b 6.1 origin/6.0

4. In IntelliJ, search and replace `6.0-SNAPSHOT` with
   `6.1-SNAPSHOT`. This should in principle only occur in the
   `.gitlab-ci.yml` files, but you better check.

5. Commit and push the 6.1 branch for the `across-framework`
   directory:

		cd across-framework
		git push -u origin HEAD --dry-run
		git push -u origin HEAD

6. Next, commit and push each of the following repositories, but ONLY
   AFTER the build of the previous one was successful (otherwise there
   will be no `6.1-SNAPSHOT` artifacts on the Nexus server to download
   as dependencies).


## Upgrade Spring Boot

TODO: where to search&replace

TODO: how to use https://docs.openrewrite.org/
