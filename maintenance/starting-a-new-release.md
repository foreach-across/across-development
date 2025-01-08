---
title: Starting a new release
weight: 30
toc: true
---

This page describes the various steps that are usually required to
start a new Across X.Y version.

<!--more-->

These instructions assume Across 6.x, where framework, platform and
all modules all have the same version. For 5.x you'll have a much
harder time.

The example here is for 6.0 -> 6.1, but adapt as needed of course.


## Read the Spring Boot release notes

Read the release notes in the [Spring Boot
Wiki](https://github.com/spring-projects/spring-boot/wiki). These are
pretty good, without being too long (considering the scope of Spring
Boot!). They also come with a list of dependency upgrades, usually
with a link to the corresponding release notes. You obviously can't
and shouldn't read all of those, but if you encounter problems with a
specific dependency during the next steps, you can easily find a
high-quality source there.


## Create a new branch


1. Make sure your repositories are clean: no uncommitted files and no
   unpushed commits etc.

2. Make sure all your repositories are up to date:

        ax-exec.sh git fetch -p

   In fact, an even better option is to clone a fresh top-level
   `across-development` repo (and locally name it `6.1` in this
   example), and the child repositories, as explained in [Getting
   started]({{<relref getting-started.md >}}):

3. Then create a 6.1 branch starting from the latest commit on the
   remote 6.0 branch, for each repository:

		ax-exec.sh git checkout -b 6.1 origin/6.0

4. In IntelliJ, search and replace `6.0-SNAPSHOT` with
   `6.1-SNAPSHOT`. This should in principle only occur in the
   `.gitlab-ci.yml` files, but you better check. Obviously do not
   update it in this file, or you will mess up this documentation.

5. Commit and push the 6.1 branch for the `across-framework`
   directory:

		cd across-framework
		git push -u origin HEAD --dry-run
		git push -u origin HEAD

6. Next, commit and push each of the following repositories, but ONLY
   AFTER the build of the previous one was successful (otherwise there
   will be no `6.1-SNAPSHOT` artifacts on the Nexus server to download
   as dependencies).


## Upgrade using OpenRewrite

The first option to try is
[OpenRewrite](https://docs.openrewrite.org/). For the example of
Across 6.1, we want to upgrade to Spring Boot 3.3, so use the [Spring
Boot 3.3
recipe](https://docs.openrewrite.org/recipes/java/spring/boot3/upgradespringboot_3_3). I
always use the "Maven Command Line" option to run an OpenRewrite
recipe.

Try to use OpenRewrite first from the top-level repositories,
e.g. apply it over all repositories in one. If that does not work, it
might work by applying it on each repository one-by-one, in the right
order.

Even when running the OpenRewrite recipe works, it doesn't do
miracles. You may still have to fix compilation errors by hand, and
it's not magically going to fix the tests. In fact, the changes it
does, might also break stuff, and the easiest (and probably best)
solution is to revert a specific change ... That has one big
disadvantage: OpenRewrite will probably do the same thing on the next
upgrade cycle:

- Add a comment near the specific code that OpenRewrite messes up, to
  remind the next person doing the upgrade.

- The OpenRewrite Maven Plugin also has an [`<exclusions>` option to
  skip entire
  files/directories](https://docs.openrewrite.org/reference/rewrite-maven-plugin#plugin-configuration). That
  might be too coarse-grained, so use your best judgement.


## Upgrade the Spring Boot version number

In fact, my experience is that OpenRewrite is usually able to update
the code, but does not upgrade the Spring Boot version in the
`pom.xml` file, possibly due to the relatively specific Maven modules
organization of Across. You have to check the Spring Boot version
number in the `<parent>` section in these two `pom.xml` files:

	across-framework/across-core-dependencies/pom.xml
	across-platform/across-application-parent/pom.xml

and if necessary, manually set that to the right version. The parent
POM is `spring-boot-dependencies` for `across-core-dependencies` and
`spring-boot-starter-parent` for `across-application-parent`, but
these two always have the same version. You can find all possible
versions numbers at:

https://central.sonatype.com/artifact/org.springframework.boot/spring-boot-dependencies/versions


## Fixing compilations errors

This is obviously the first step after running OpenRewrite and/or
manually upgrading the version numbers. Most of the time these are
small things (especially in X.Y+1 upgrades). Use common sense, Google,
StackOverflow whatever to fix these.

Once `across-framework` compiles, you have two options:

1. Either first fix the tests of `across-framework`.

2. Make all the other repositories compile first.

Of course, it depends on the situation, but I usually go for the
second option to detect ASAP if there's any big breaking compilation
issues in the rest of Across. As soon as you have everything
compiling, you can immediately try to run one of the test applications
in Across (without first having to fix all tests). Two of the most
important ones are:

- `EntityModuleTestApplication` (of course you can try this as soon as
  `entity-module` compiles).

- `PlatformTestApplication`: This one is important because it tests
  the combination of `entity-module` and associates, with
  `user-module`.

If these work (or at least start up) you know already a lot. Whereas
fixing the tests repository by repository, module by module, can be
quite a bit of work, with relatively little real-world feedback.

But most importantly, at this point, you can [skip the step of fixing
the tests]({{<relref "#fixing-the-tests">}}) (for now obviously), and
already [give a *real* application a try]({{<relref
"#tryout-with-an-application">}}), so we'll keep that order in this
documentation. But first we need to explain the
`dependencies.list/.tree.txt` files.


## dependencies.list.txt / dependencies.tree.txt

The Across git repositories (and at least one application repository)
have the following files next to each `pom.xml` file:

	dependency.list.txt
	dependency.tree.txt

These are generated using the `generate-dependencies.sh` script in the
`bin` directory of the `across-development` repository, which is put
in your `PATH` when you source the `env.sh` script (See [Getting
started]({{<relref "getting-started.md#initial-maven-build" >}}). This
script is a wrapper around the following Maven goals:

- [`maven-dependency-plugin:list`](https://maven.apache.org/plugins/maven-dependency-plugin/list-mojo.html)
- [`maven-dependency-plugin:tree`](https://maven.apache.org/plugins/maven-dependency-plugin/tree-mojo.html)

The `dependency.list.txt` file contains an alphabetically sorted list
of artifacts that the Maven module depends on, directly or indirectly,
as chosen by the [Maven dependency selection
algorithm](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
(Mathematically speaking, this is the [transitive
closure](https://en.wikipedia.org/wiki/Transitive_closure) of the
dependency graph). This file is easy to diff against previous
versions, so that you can clearly see all updates that have been done,
and which dependency versions are actually used (which is sometimes
non-trivial). This is also the reason why we commit these files to
version control.

The `dependency.tree.txt` file shows the dependency graph of the
module, but reduced to a tree structure, according to the algorithm
that Maven uses to select artifact versions. So if you are wondering
where a specific dependency (or version of that dependency) comes
from, you can find it here.

Unfortunately, there is no easy way to ensure these two files are kept
in sync with changes to the `pom.xml` files, so that burden is on
you. At least the script can simply be run from the top-level
directory (e.g. in the `across-development` repository):

    generate-dependencies.sh

The script also checks that there are no dependencies with more than
one version, in all of Across. Unfortunately there is one artifact (in
`across-autoconfigure`, also see the note about that in further) for
which that is not the case:

    ERROR: There are 1 dependencies with multiple versions:
      2 org.springframework.plugin:spring-plugin-core

But so far that has not caused any issues, so you can safely ignore
it.

Finally, the rule to remember is simple: Whenever you make any change
to a `pom.xml` file, and once `mciwt` over all repositories compiles
everything OK, you should re-run `generate-dependencies.sh`. And make
sure to commit that together with the `pom.xml` versions.

Here are a few more tips about visualizing dependencies:

- The `dependency:tree` goal can also generate a `.dot` file, which
  can be graphically plotted using
  [GraphViz](https://graphviz.org/). Note that dependency graphs can
  be enormous, and because of that, you usually want to plot the
  dependency graph with all redundant dependencies removed
  (mathematically called [the transitive
  reduction](https://en.wikipedia.org/wiki/Transitive_reduction))

        tred graph.dot | dot -Tsvg > graph.svg

  But even then it will still be big. The `tree` goal also have
  options to include/exclude specific dependencies to help with that.
  
  I usually use SVG as the output format, because when you open that
  in a browser, you can actually *search* for any text in the graph,
  which is very useful in a large graph.

- There is also an `ax-dependencies.py` script (which is not based on
  the `maven-dependency-plugin`), but whose output is a `.dot` file as
  well. Run the script with `--help` for more info. This script was
  used to generate the dependency plot at the bottom of the [Modules
  page]({{<ref "/modules.md#module-dependency-graph">}}).


## Tryout with an application

Of course, you can only try this with an application that is already
up-to-date with Across / Spring Boot upgrades (or at least pretty up
to date).

There is also a practical issue now: if the tests are still failing in
CI at this moment, then there are also no X.Y-SNAPSHOT (6.1-SNAPSHOT
in this example) jar files being published to the internal Nexus
server. So you can't compile the application against those
snapshots. This can also be considered a blessing in desguise, because
working against snapshots downloaded from a repository isn't easy
either, due to Maven caching in your local repository. This command
will quickly become your friend:

    rm -rf ~/.m2/repository/com/foreach

(which is also still useful with the alternative I'll present).

Also: Make sure you do *not* accidentally hit `enter` after the `~/`:
you'll wipe out your entire home directory :-(. Which is why you
better do this:

    rm ~/.m2/repository/com/foreach -rf

The solution for the missing X.Y-SNAPSHOT jars is:

1. Compile all of Across (from the top-level directory) with the
   `mciwt` alias (`wt` = without tests because you want to iterate
   fast). This installs (the `i` in `mciwt`) the Across maven
   artifacts in your local Maven repository with version
   `dev-SNAPSHOT`. There are never artifacts with version
   `dev-SNAPSHOT` published to the Nexus server (unless somebody
   changes the CI/CD setup), so you know this is always whatever the
   last code is that you have built locally.

2. Change Across version property/properties in your application to
   `dev-SNAPSHOT` to pick up those artifacts.

When you have to go back and forth between making a change in Across,
and testing it with the application, this is definitely a much better
developer experience, with a much faster edit-compile-debug cycle.


## Fixing the tests

I like to run all tests using Maven on my laptop: it's a much faster
feedback loop than CI, and using the `--fail-at-end` option, I can get
feedback over multiple repositories in one go. Also: if there are many
failures, there's a good chance there are just a few root causes
behind the majority of the failures, and this can give a better
overview of the issues.

See [Getting started]({{<relref
"getting-started.md#running-tests-with-maven" >}}) for the right
commands and configuration.

The most annoying thing that can happen here is that you have to
continuously go back and forth between fixing tests and making changes
in a low-level repository (e.g. `across-framework`) and a high-level
repository (e.g. `across-entity-admin-modules`), and possibly even the
real application that you have chosen. This is another reason why I
like to give a real application a try before attempting to fix all the
failing tests. And using `dev-SNAPSHOT` in the application results in
a faster edit-compile-debug cycle.

If you upgraded any dependencies in this step, or even changed any
`pom.xml` file, make sure to re-run the `generate-dependencies.sh`
script.


## Upgrade other dependencies

Across also uses a number of dependencies whose version is not managed
by
[`spring-boot-dependencies`](https://central.sonatype.com/artifact/org.springframework.boot/spring-boot-dependencies/versions). This
includes for example:

- testcontainers
- guava
- httpclient4
- ...

You can find these in the two `pom.xml` files that were also mentioned
earlier:

	across-framework/across-core-dependencies/pom.xml
	across-platform/across-application-parent/pom.xml

And in the top-level `pom.xml` files of all repositories.

You may have had to upgrade some of these dependencies to fix
compilation or to fix the tests in one of the previous steps. Now that
all tests are working, it is a good time to go through all other
version dependencies, and upgrade them if sensible. Ensure that the
versions are in sync in all repositories (`generate-dependencies.sh`
helps with that).

There is one exception: Do not try to upgrade the dependencies in
`across-autoconfigure`, unless absolutely necessary. Experience is
that that just creates more trouble than it's worth, and many of these
dependencies just shouldn't be upgraded. In fact, when there are
problems with some of the test modules of `across-autoconfigure`, I
have often just disabled such a test module, because it tests an
integration with something that no active project uses anymore (such
as Cassandra, MongoDB, ...).

Important: The two `pom.xml` files from above contain a set of
(version) properties that have to kept in sync *exactly* (this wasn't
always the case in the past, leading to some surprises).

These are marked by the comments (in the different files):

    <!-- Keep in sync with across-application-parent -->
	<!-- Keep in sync with across-core-dependencies -->

respectively. Use for example `kdiff3` to verify this:

	kdiff3 across-framework/across-core-dependencies/pom.xml across-platform/across-application-parent/pom.xml

I recommend that you only push these upgrades in all the repositories,
once the tests all pass on your laptop. Otherwise you risk have to go
back and forth with upgrading in one repository, which breaks the next
one, and then you have to go back to the previous one, etc etc.

Alternatively, use a feature branch for these upgrades, and a `git
merge --squash` to merge it to the `X.Y` branch.

Again, you likely changed some `pom.xml` files in this step, so make
sure to re-run the `generate-dependencies.sh` script before pushing
your changes.


## Re-test the application

You've made some more changes to Across in the mean time (fix tests,
upgraded other dependencies), so you should definitely re-test your
application at this point.

Now is also a good time to have another colleague do some functional
testing as well.

You should also deploy the application to a test environment at this
point, to ensure it works there as well (we have seen cases where
there was a startup issue at this point, possibly requiring some
configuration or IaC changes).


## Next steps

Ideally, you should upgrade and test another application at this
point, but that may not always be realistic.

By the time you get to this point, there may already have been a new
maintenance release of Spring Boot (.Z in X.Y.Z, these are monthly),
for the major version that you are upgrading to. So make sure you are
on the latest maintenance release and that you re-run
`generate-dependencies.sh` afterwards.

In principle, you are now ready [to make a release build]({{<relref
release-procedure.md>}}).

Once the release build is finished, don't forget to update the
applications, and replace the -SNAPSHOT versions in the `pom.xml`
file(s) with the released version.
