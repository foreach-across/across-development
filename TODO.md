# Integrate admin-web-bootstrap-4

Into the `across-entity-admin-modules` repository.


# End-to-end tests

Also: are we running the frontend unit tests? Not that there are a lot
of those.

End-to-end tests are at least in:

	across-entity-admin-modules/bootstrap-ui-module/src/main/frontend/tests/e2e
	across-entity-admin-modules/entity-module-test-application/src/test/e2e


# Maven configuration

`across-autoconfigure` also has widely varying build times, and an
occasional random failure. Plus it starts several Java-based
testcontainers, which again might all be using 1/4 of the memory ...

- `-Xmx256m` for the Maven JVM should be sufficient for all
  repositories and a safe option.

- Use `-Xmx512m` also for `maven-surefire-plugin`?

- Use `-Xmx512m` for all repositories/modules, or keep it to
  `across-media-modules`?

OTOH, we don't want to slow down the tests by arbitrarily reducing the
JVM heap size: after all, we should be using those 4 GiB when we can.

There could be lot to be gained by explicitly configuring the memory
of the Java testcontainers:
https://java.testcontainers.org/features/advanced_options/

Does `testcontainers` configure a JVM exit hook to stop a container
when the JVM exits? Or does it rely on `ryuk` even in this case? That
would mean that the next part of the build might not have enough
memory, because an old container hasn't been stopped yet.


# Build optimization

## Configure testcontainers to use the GitLab Dependency Proxy

	TESTCONTAINERS_HUB_IMAGE_NAME_PREFIX: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}


## Custom build image

Might reduce the pain of `testcontainers`, and allow for better
caching in the GitLab Dependency Proxy.

This would be based on `maven:3.8-eclipse-temurin-8` (which in turn is
based on Ubuntu 22.04), and need at least the following packages:

- `gpg`: signing maven artifacts

- `graphicsmagick`: for ImageServer

- `ghostscript`: also for ImageServer, because it can effectively
  execute `ghostscript` commands

- `docker.io`: when using `testcontainers` through the GitLab
  Dependency Proxy.


# Sync to GitHub

https://docs.gitlab.com/ee/user/project/repository/mirror/

https://docs.gitlab.com/ee/user/project/repository/mirror/push.html


# Release build

We need a new release build procedure/script/tool, hopefully not as
elaborate as AXRT.

Maven has much more modern feature for release build than the old
`maven-release-plugin`, e.g.:

https://maven.apache.org/maven-ci-friendly.html

And we already have that `revision` property, it's just not used for
what it's intended.

GitLab can do different things depending on whether a branch or a tag
was pushed. Ideally, the value for `revision` can be derived from
that:

- Push to `5.3` branch => `5.3-SNAPSHOT`
- Push `v5.3.0` tag => `5.3.0`

(Yes, we'll drop the `.RELEASE`, which Spring (since 5.3) and Spring
Boot (since 2.4) have also done.

The question is: how easily can this be done, preferably in the
`variables` section of the `.gitlab-ci.yml`

See the `artifact-version.sh` script for an attempt to do this with a
one-liner. While that works in `bash`, a `.gitlab-ci.yml` variable
value isn't evaluated in a shell. See the `gitlab-ci-cd-tryout` for a
solution that uses a different job for tags and branches.


# Website

Store the old website in a Git repository.

See the various TODO's in the `website` directory.

Use GitLab CI/CD to publish the website on each push to main: draft
articles won't be published anyway.

Figure out where to store the Antora docs and the Javadocs (Cloudflare
R2 maybe?).

Point DNS to GitHub.


# Frontend upgrades

Manually verify that all frontend result files are the same as in
5.1.0 / 5.2.1.

Bootstrap 4 is EOL since 2023-01-01 (last version = 4.6.2):

- https://endoflife.date/bootstrap
- https://blog.getbootstrap.com/2022/07/19/bootstrap-4-6-2/

`cypress/browsers:chrome65-ff57` is obviously rather out of date.

`yarn` in the various frontend builds complains that the
`package-lock.json` file is from `npm`, not `yarn`.


# Reproducible builds

Why: https://reproducible-builds.org/
How: https://maven.apache.org/guides/mini/guide-reproducible-builds.html

Might require upgrading maven plugins.

`project.build.outputTimestamp` should be defined in the parent pom of
each repository, otherwise `mvn clean verify artifact:compare` logs an
error (but does consider the result passed).

Frontend build outputs will likely be the biggest hurdle for
this. I've manually verified that it works for the frontend builds in
`across-entity-admin-modules`.

A quick tryout indicated that this works: Spring Boot 2.4 defines the
right Maven plugin versions for reproducible builds except for
`maven-javadoc-plugin`: while it has the right minimal version, that
version would have to be configured with `notimestamp`. Instead I
choose to upgrade the plugin to the latest version, which does that
automatically when the `project.build.outputTimestamp` is set.

TODO: publish the `buildinfo` file, which is apparently intended to be
run from the CLI:
https://maven.apache.org/plugins/maven-artifact-plugin/usage.html

To be relatively sure the build is reproducible, we probably need to
run it twice, during the `deploy` job. Or alternatively, do that in a
separate job. This actually fails at the moment:

https://gitlab.isaac.nl/antwerpen/across/across/-/jobs/476201
