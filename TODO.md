# direnv

Switch to `direnv`: https://direnv.net/ and document it in the getting
started.


# Verify number of tests

Against Bamboo, before making the 5.3 release build.

Keep in mind that Bamboo will likely run integration tests during the
unit tests as well (against H2).


# Frontend unit tests

I don't think they were run on Bamboo either ...


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

## Per-job type caches

e.g. maven caches for maven jobs, nodejs caches for node jobs


## Configure testcontainers to use the GitLab Dependency Proxy

	TESTCONTAINERS_HUB_IMAGE_NAME_PREFIX: ${CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX}


## End-to-end tests in across-entity-admin-modules

These install Cypress from the website on each and every run. See
`e2e-tests.docker`. We should be able to use the docker image with
Cypress and the browsers in [one
image](https://hub.docker.com/r/cypress/included), but that requires a
big Cypress upgrade.


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

`docker-compose` is a single, statically linked binary that can be
installed using a single `https` request:

https://docs.docker.com/compose/install/standalone/

Docker Engine is also available as a tarball with statically linked
binaries for `docker` and other tools (including the docker daemon,
don't need that):

https://docs.docker.com/engine/install/binaries/


# Website

Store the old website in a Git repository.

See the various TODO's in the `website` directory.

Use GitLab CI/CD to publish the website on each push to main: draft
articles won't be published anyway.

Figure out where to store the Antora docs and the Javadocs (Cloudflare
R2 maybe?).

Point DNS to GitHub.

Add a pointer to the Across School presentation (Dutch). p.22 is
broken though:

https://foreachos.github.io/ax-school

Perhaps add a `.github` repository to `ForeachOS` with a README.md
that is shown for organization; see for example:

https://github.com/containers/.github/tree/main/profile

That is shown before the pinned repositories, which should be:

	across-framework
	across-platform
	across-development
	ax-docs-across-site

Although perhaps we should integrate the Antora playbook into
`across-development`?


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
version would have to be configured with `notimestamp`. Instead, I
choose to upgrade the plugin to the latest version, which does that
automatically when the `project.build.outputTimestamp` is set.

TODO: publish the `buildinfo` file, which is apparently intended to be
run from the CLI:
https://maven.apache.org/plugins/maven-artifact-plugin/usage.html

To be relatively sure the build is reproducible, we probably need to
run it twice, during the `deploy` job. Or alternatively, do that in a
separate job. This actually fails at the moment:

https://gitlab.eindhoven.io-internal.dev/antwerpen/across/across/-/jobs/476201


# dev-SNAPSHOT

I would like to open all projects in a single IntelliJ project,
probably with `across-development` at the top. The problem with this
is: IntelliJ cannot handle the `revision` properties having different
values. It just gets hopelessly confused.

The cheap solution is obviously: just use the same version
everywhere. Problem is that image server already used 6.x, which
forced `across-media-modules` to use that as well. And I really want
to use 6.x for Spring Boot 3.x, with Spring Framework 6, Spring
Security 6 and Hibernate 6. Workaround for that is to just switch to
5.10 now, and start from 6.10 for 6.x.

There might be another option: use `dev-SNAPSHOT` for `revision` and
all `.version` properties, and then use search and replace:

`<revision>dev-SNAPSHOT</revision>`: Always the version of the current
repository.

`<version>dev-SNAPSHOT</version>` -> always the version of
`across-framework`, because it's only used in `<parent>` sections, and
in `across-autoconfigure/test-projects/pom.xml` to define the version
of `across-test`, but that's still `across-framework`. Ideally there
should be an `across-framework.version` property in
`across-autoconfigure`.

`<across-xyz-modules.version>dev-SNAPSHOT</...>` -> always the version
of that repository.

So it's real easy with Python or even `sed` to automatically search
and replace these values. It's almost possible in the other direction
as well, except that you can't just replace
`<version>whatever</version>`.

This solves the "the `parent` `version` cannot use a property" problem
that more or less forces us to commit modified `pom.xml` files to Git,
which I prefer to avoid. Counter point: in the current release build
procedure, pushing that commit is what triggers the tests (although
they've already run, but against snapshots, so not entirely
reliable). Update: there will still be a commit, but with the version
numbers changing in the environment variables in the `.gitlab-ci.yml`
file.

Not committing the changed `pom.xml` files to Git is key for this.

So the question becomes: can be easily do this in an init step for
each GitLab CI job?

- We don't need this in the front-end jobs.

- We do use `before_script:` in 4 places, which is always at the job
  level. Could we use `before_script` at the top-level, without it
  being overwritten by the job-level ones? Nope, that's not how it
  works:
  https://docs.gitlab.com/ee/ci/yaml/script.html#set-a-default-before_script-or-after_script-for-all-jobs

- If it's a simple line, say just execute a script, we can live with
  the duplication.

- Getting that script is typically the problem, but we can write it
  once, and just copy it to each of the seven repo's. Or `curl|bash`
  it, but the job token will only have access to the project being
  built, not to `across-development`. A [Group access
  token|https://docs.gitlab.com/ee/user/group/settings/group_access_tokens.html]
  is probably an option. Downloading the script from Nexus is an
  option too.

- Or finally do switch to `submodules` (shudder) to get scripts etc in
  the build?

- The script could be written in Python if the maven image contains
  `python` or `python3`: as expected, that's not the case for
  `maven:3.9.6-eclipse-temurin-8`, but it does have `sed`. Or we could
  define our own build image, also clean up some apt installs
  (graphicsmagick, gpg), but that would be yet another skill an Across
  maintainer would need to have.

- All options to download the script from somewhere will be annoying
  to duplicate in the job-level `before_script`.

`sed` seems like the winner here, with (a variant of) the script
duplicated in each repo, and the versions declared as environment
variables in the per-project `.gitlab-ci.yml` file. The script could
be called `ci-before.sh` or something like that, and conditionally
executed if it exists or not. Easy to duplicate in the per-job
`before_script` as well.

One thing to watch out for is the release build procedure: the
"pre-build" must also run the script, and commit the changes to
`.gitlab-ci.yml`, but not those to the `pom.xml` files.

Or switch to Gradle, but since we have little in-house Gradle
experience, it doesn't seem like a sustainable option.

Timing for a top level build on an i7 13800H (6Px2T+8E cores) laptop:

	mciwt      00:57
	mciwt -1TC 00:30
	mci        09:38
	mci -T1C   06:07

Integration tests:

	axitest                                    06:02
	axitest -T1C                               03:10
	axitest -DacrossTest.datasource=mysql      05:02
	axitest -DacrossTest.datasource=mysql -T1C 02:23 FAIL

Parallel integration tests only work with H2, because that's in memory
and can easily use a separate "database" or "server" for each Maven
module. As expected, with a real database, all parallel tests using
the same server/schema/database will just hopelessly mess up that
database.


# Spring Boot applications not starting in the top-level project

`PlatformTestApplication` doesn't start from the overall 5.5 IntelliJ
project:

	Caused by: java.lang.IllegalAccessError:
	tried to access class
	org.springframework.data.repository.config.RepositoryBeanDefinitionBuilder
	from class
	org.springframework.data.repository.config.AcrossRepositoryConfigurationDelegate

And yes, that's an Across class in a Spring Data package!

The weird things are:

- It does start in an IntelliJ project opened from the
  `across-platform/pom.xml`, and the Java and Java command line
  arguments are exactly the same (haven't checked the entire classpath
  though).

- It does work in `ITPlatformTestApplication`, which runs the exact
  same line without a problem.

- We're running with JDK8, so this shouldn't be a JDK9 modules thing.

The problem is probably: in the global project, the
`AcrossRepositoryConfigurationDelegate` class is loaded by the
`RestartClassLoader`, while the rest of that package is loaded from
the `spring-data-jpa.jar` using a different class loader. It makes
sense that the tests work, because those are unlikely to run in a
restarting class loader. And indeed: when removing
`spring-boot-devtools` from the classpath of `platform-bom-test`, it
starts just fine.


# 5.5

Not a priority at all: Is now possible to use the
`spring-boot-security-starter`? Without adding it to
`across-autoconfigure`? Perhaps only at the application level (check
with Cama first)?

Migrate to the non-legacy option, as explained in [the migration blog]
(https://spring.io/blog/2022/02/21/spring-security-without-the-websecurityconfigureradapter):

    public void configureGlobal( AuthenticationManagerBuilder auth ) throws Exception {

Move the `dev-SNAPSHOT` discussion out of this TODO, and into the maintenance
documentation.


# 6.0

Undo java.locale.providers=COMPAT and use CLDR by default


# Version numbers

Align all repositories on version 6.0.0?

This makes it possible to get rid of `dev-SNAPSHOT`, but that in turn
might not make the release procedure simpler ...


# Migration guides

Write docs about how to migrate to the `across-platform-bom` + update
old release notes. Also explain the reasoning.

Use `common-file-manager` instead of `file-manager-module`.
