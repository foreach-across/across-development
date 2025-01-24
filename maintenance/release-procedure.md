---
title: Release procedure
weight: 70
toc: true
---

The release procedure consists of:

- Making a release plan file.

- Running a script for each repository you are releasing.

- And a few post-release steps.


<!--more-->

## Create a release plan file

On the `main` branch of the `across-development` repository, go to the
`release-plans` directory. This will look something like:

	5.3.0-M1.yml
	5.3.0-M2.yml
	5.3.0.yml
	5.4.0.yml

In this example, we'll release `5.4.1`, so the easiest option is to
start from the `5.4.0.yml` file:

	cp 5.4.0.yml 5.4.1.yml
	git add 5.4.1.yml

Edit the content of the new release plan file with the repositories
and their corresponding new versions. For the `5.4.1` example, this
will look like:

	across-framework: 5.4.1
	across-autoconfigure: 2.4.1
	across-base-modules: 4.4.1
	across-entity-admin-modules: 4.4.1
	across-user-auth-modules: 4.4.1
	across-media-modules: 6.4.1
	across-platform: 5.4.1

Note that the order is important: it should follow the dependencies,
and the order in which the repositories are to be released.


## Run the release script for each repository

Warning: This is a procedure that takes a fairly long time (think 1.5
to 2 hours), so the recommendation is *NOT* use the terminal in
IntelliJ, but an OS-native terminal ("Terminal" in macOS, Gnome
terminal, Windows Terminal etc).

First of all, make sure you have sourced the right Python virtual
environments, and your `JAVA_HOME` and `PATH` environment variables
point to the right JDK (1.8 for Across 5, 17 for Across 6). For my
setup, this is:

	. ../../venv/across/bin/activate
	. env.sh

Verify this:

- `which python` should show the path to the `python` executable in
  the `across` virtualenv:

        $ which python
	    /home/dvsp/git/venv/across/bin/python

- `mvn --version` should print the right JDK version:

		$ mvn --version
		Apache Maven 3.9.6 (bc0240f3c744dd6b6ec2920b3cd08dcc295161ae)
		Maven home: /home/dvsp/tools/maven
		Java version: 1.8.0_332, vendor: Temurin, runtime: /home/dvsp/.jdks/temurin-1.8.0_332/jre
		Default locale: en_US, platform encoding: UTF-8
		OS name: "linux", version: "6.5.0-21-generic", arch: "amd64", family: "unix"

In the example, we are making a new release for each repository, so we
start with `across-framework`. From your `across-development`
repository (where you have cloned all the other repositories), run:

	ax-release.py start release-plans/5.4.1.yml across-framework

This will perform a few basic checks, edit the required `pom.xml`
files to change the version numbers, and show you the diff of those
changes. It will then ask for your confirmation. If you're OK with the
changes, type `y` + enter to continue.

From here onwards, everything will be done automatically (for the
current repository):

- A `mvn` build will be run locally, without any tests, to ensure that
  the modified `pom.xml` files will actually build.

- The changes will be committed and pushed to GitLab.

- This will trigger a regular pipeline in GitLab, with one small
  variation, because the `revision` is now no longer a `-SNAPSHOT`: in
  the final job (`deploy:foreach`), `mvn` will deploy the artifacts to
  the `across-releases` repository on the Foreach Nexus server
  (instead of the `across-snapshots` repository).

- When that pipeline is finished successfully, the script will create
  a git tag (`v5.4.1` in this example) and push that to GitLab.

- Pushing that tag will trigger another pipeline in GitLab, but with
  just a single job: `deploy:sonatype` (a job that is never run in a
  "regular" branch or merge-request pipeline). This job will perform
  all of the steps documented at:

  https://central.sonatype.org/publish/publish-guide/

  FYI: Across is on the "legacy" host: https://oss.sonatype.org/, not
  on the newer https://s01.oss.sonatype.org/.

Once that last pipeline is finished successfully, the script will end
with the following message:

> Remember to close, release and drop the staging repository at
> https://oss.sonatype.org/#stagingRepositories But keep in mind that
> can be done for all releases together at the end as well.

We'll take the last option, and release everything together at the
very end.

For now, perform the above procedure again, for each of the remaining
repositories. Once all of those are done successfully, go to the next
step.


## Deploy to Maven Central

In this step, we follow this procedure from Maven Central:

https://central.sonatype.org/publish/release/

In short: go to:

https://oss.sonatype.org/#stagingRepositories

and login with your account that gives you access to Across (check
with the lead Across maintainer for access).  If you don't see any
repository, click the "Refresh" button.

Before we release (*There is no undo!*), we will do a brief check of the
content of the staging repository:

- Click on the staging repository

- At the bottom, select the "Content" tab.

- Open the tree, and check that all the expected maven artifacts are
  there. For instance:

- `across-core`, `across-test` and `across-web`, with the right
    versions, if you made a new release for the `across-framework`
    repository.

  - `across-autoconfigure` if you released the corresponding
    repository.

  - Check that all the modules you released are under
    `com.foreach.across.modules`, with the right versions.

Once you are certain that the staging repository contains the right
artifacts:

- Select the staging repository.

- Click the "Close" button: this takes a while, because it checks
  whether all artifacts comply with the [Maven Central
  requirements](https://central.sonatype.org/publish/requirements/),
  such as `sources` jar files, GPG signatures, ... Unless those
  requirements have changes, the build procedure should have taken
  care of them all.

- Once the repository is closed, the "Release" button becomes
  available. Once you click that, there is no way back: the artifacts
  will be deployed to Maven Central, and can never be removed or
  modified again. So, be very sure of the contents, before you click
  that button!

After (in principle) maximum 10 minutes, the new artifacts should be
available at Maven Central:

https://repo1.maven.org/maven2/


## Deploy Javadocs to the website

The API Javadocs are hosted using GitHub Pages, using this repository:

https://github.com/foreach-across/api-docs-6

Run the equivalent of:

	ax-release.py javadoc release-plans/5.4.1.yml

This will:

- Clone the GitHub repository.

- Download the `javadoc` jar files from Maven Central (so they must
  have deployed before you can do this) and unzip them in the right
  directory.

- Regenerate the `index.html` files with the new entries.

- Update the `current` symlinks to point to the latest release, but
  only if needed. For instance, if you release `5.4.2`, but `5.5.0`
  was already released, the "current" version will still be `5.5.0`.

- Commit and push the changes to GitHub (unless you used the
  `--no-push` option).

When the changes are pushed, GitHub Pages will automatically
re-deploy the site to:

https://foreach-across.github.io/api-docs-6/

This may take a minute or two. With the right permissions, you can
check when the site was last deployed at:

https://github.com/foreach-across/api-docs-6/actions


## Write and deploy release notes

Create the release notes under the `releases-notes` directory, for
instance by starting from an older release note:

	cd release-notes/
	cp 5.4.0.md 5.4.1.md
	git add 5.4.1.md

Change the title, date and author (if necessary) in the header of the
new document.

Second, if this is an X.Y.0 release (e.g. a new minor release of
Across), then you also have to update the overview table at the start
of `release-notes/_index.md` (which is rendered at the top of the
[Release notes page]({{<relref release-notes.md>}}). You need to add a
new column for the new Across version, with the corresponding versions
of Spring Boot, Spring Framework, etc.

Start the [Hugo static site generator](https://gohugo.io) in
development mode:

	cd website
	make start

Open [http://localhost:1313/](http://localhost:1313/) in your browser
and navigate to your new release notes. Whenever you edit the Markdown
file (in your editor), it will immediately be rerendered in the
browser.

Once your release notes are finished you can deploy the changes to
the website (you will need write access to the [website
repository](https://github.com/foreach-across/foreach-across.github.io)):

	cd website
	./deploy.sh "Release notes for 5.4.1"

Since this is very small, deployment will be fast, but you can follow
the progress here:

https://github.com/foreach-across/foreach-across.github.io/actions


## Reset versions to --SNAPSHOT

Warning: This is a procedure that takes a fairly long time (think 1.5
to 2 hours), so the recommendation is *NOT* use the terminal in
IntelliJ, but an OS-native terminal ("Terminal" in macOS, Gnome
terminal, Windows Terminal etc).

1. Make sure you are still in the same `across-development` repository
   as the one where you performed the release, and that the 7
   repositories are still on the same branch as used for the release.

2. Ensure you have the latest commit for the release branch of each
   repository (See the [Tips and tricks]({{< ref "tips-and-tricks"
   >}}) for details about these commands):

		ax-exec.sh git fetch -p
		ax-exec.sh git pull --ff-only

3. Next:

		ax-set-snapshot-versions.py

4. Lastly, you'll need to commit and push each repository separately
   again (TODO: Automate this).
