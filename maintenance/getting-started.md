---
title: Getting started with development on Across
weight: 10
toc: true
sidebar:
    open: true
---

These instructions are for setting up your development environment on
your laptop, in order to efficiently work on the Across framework,
modules and platform.

<!--more-->

## Use the CLI, not IntelliJ

Title says it all, the initial instructions here *MUST* be done in a
terminal, preferably using the `bash` shell (`zsh` might work, but I
make no guarantees).


## Prerequisites

On macOS, most of these can be installed using Homebrew. On Windows,
you can often use Chocolatey.

- `bash`

- Python: minimum 3.10

- Java: 8 for Across 5.x, 17 for Across 6.x, see further for the
  specific installation instructions that are *required* to make the
  scripts work. Do *NOT* skip this step.

- Maven: Latest 3.9

- [GraphViz](https://graphviz.org/download/)

- [Hugo](https://gohugo.io/) static site generator: use the extended
  version.

- Go (if using a Hugo theme which requires Go modules)

IntelliJ: install the [Hugo
plugin](https://plugins.jetbrains.com/plugin/13215-hugo-integration)


## JDK installation instructions

Install both a JDK 1.8 and a JDK 17 in `~/.jdks`. The easiest way to
do this is:

- Download the latest Eclipse Temurin 1.8 and 17 JDK using the Project
  Structure dialog in IntelliJ, which will put this in the `~/.jdks`
  directory.

- Then create symlinks so the `~/.jdks/1.8` and `~/.jdks/17` point to
  the latest 1.8 and 17 in the `~/.jdks` directory.


## Clone the repositories

### Clone the across-development repository:

First of all, make a directory where you will work on Across:

	mkdir -p ~/git/across
	cd ~/git/across

And then clone the across-development repository:

	git clone https://gitlab.eindhoven.io-internal.dev/antwerpen/across/across-development.git

The (default) `main` branch is for Across 6.x. Switch to the `5.x`
branch for maintenance on older releases, but hopefully that will not
be needed. I highly recommend using separate local repositories for
5.x and 6.x development. At the time of writing, 6.0 is the version in
development, so you probably want to do something like this:

	mv across-development 6.0


### Setup the Python virtualenv

`across-development` comes with a lot of `bash` and `python` scripts
for automation. There is also an `across.yml` file in the top-level
directory, that is used by the python scripts, but also by the
[Hugo](https://gohugo.io/)-based Across website.

We need to set up a Python
[`virtualenv`](https://docs.python.org/3/library/venv.html) to make
these scripts work. Personally, I prefer to keep my virtualenvs
outside the git repository, otherwise it sometimes causes trouble with
IntelliJ:

	python3 -m venv ../venv-6

Next you have to activate the `venv-6` environment in your current
shell (and any other terminal that you open), by sourcing the
`activate` script, which should work for both `bash` and `zsh` (there
is a separate `activate.fish` script if you like `fish`):

	source ../venv-6/bin/activate

Or, more idiomatically:

	. ../venv-6/bin/activate

If you now run:

	which python3

you should see that your shell picks up `python3` from the
`../venv-6/bin` directory.

Next we need to install the required Python packages into your
`virtualenv`:

	pip install -r requirements.txt

Now source the `env.sh` to add the local `bin` with the Across scripts
to your `PATH`:

	. env.sh

Try the following commands:

	ax-list.py modules
	ax-list.py modules --with-repo
	ax-list.py repositories

These commands should list the modules and repositories, in the order
that they are build (and are [listed on the website]({{<ref
modules.md>}})).

The order of the repositories is something you need to know by heart,
if you want to efficiently work on Across. It's not a long list, and
the order is pretty logical, so this shouldn't be a problem.


### Clone the Framework, modules and Platform repositories

Next, we will use the `ax-list.py` script in combination with `xargs`
to clone all the repositories:

	ax-list.py repositories | xargs -I '{}' git clone https://gitlab.eindhoven.io-internal.dev/antwerpen/across/{}.git

The initial branch in each of those repositories will be whatever
happens to be the current default branch, so lets check what branch
this is, using, you guessed it, yet another script:

	ax-exec.sh git status

This simply executes `git status` in each of the child repositories.

Tip: If you want to run a command with `ax-exec.sh`, first start
typing that command itself, using standard shell completion. Then use
`ctrl-a` to go to the beginning of the command, and add `ax-exec.sh`
followed by a space, and `enter`.

Since we want to work on 6.0, and the 6.0 branches already exist, you
can now do:

	ax-exec.sh git checkout 6.0


### Clone the website repository

The [Across website](https://foreach-across.github.io) is actually
just a [GitHub
repository](https://github.com/foreach-across/foreach-across.github.io)):
which contains the HTML/CSS/... files of the website. That repository
must be cloned in a specific directory:

	cd website
	git clone git@github.com:foreach-across/foreach-across.github.io.git public

Publishing the website is one of the last steps of the [Release
procedure]({{< relref release-procedure >}}), so that's documented there.


## Initial Maven build

Assuming you followed the specific JDK installation instructions, you
can now source the `env.sh` file:

	. env.sh

Then use the alias `mciwt` (use `alias mciwt` to see what it does)
from the top-level directory:

	mciwt

This will likely fail with an error about some missing artifacts with
version `dev-SNAPSHOT`. This is due to the very specific structure of
the (parent) modules in Across, for which there is no easy
solution. The workaround is to first build in `across-framework`, and
then build everything:

	cd across-framework
	mciwt
	cd -
	mciwt

Remember this, because you will likely run into this more than once.

Tip: If you ever run into trouble with Across snapshots and Maven
and/or IntelliJ, then check out the [Tips and tricks]({{<relref
tips-and-tricks >}}).


## IntelliJ

Now that you have build everything using Maven, you can open the
top-level `pom.xml` in the `across-development` repository. This opens
*all* of Across in one single IntelliJ project, which any modern
laptop can easily handle. This is the only way to be able to work
efficiently on Across, allowing you to easily follow all references,
open call/class hierarchy, etc.

This is in fact the reason why the `dev-SNAPSHOT` version exists: the
IntelliJ support for Maven cannot handle different versions in the
various child projects, or at least not when they are defined using
the [`revision`](https://maven.apache.org/maven-ci-friendly.html)
property. And in Across 5.x, the various modules (or, since 5.3, the
repositories) have different versions. This obviously meant quite a
bit of work for GitLab CI/CD, and for the release procedure.

In Across 6.x, we have lined up all versions of Across Framework, all
modules/repository and Across Platform to 6.x. This is one of the
reasons why the `across-media-modules` repository (with {{<module-ref
file-manager-module>}}, {{<module-ref imageserver-core>}} and
{{<module-ref web-cms-module>}}) *had* to be removed from Across
{{<release-note-ref 6.0.0>}}: they were already at 6.x in Across
5.x. And I did not want to jump to Across 7, because it's nice to have
Across 6 with Spring 6, Spring Security 6 and Hibernate 6, and easier
to remember especially.

We could simplify the build process for Across 6.x, but I would not
recommend that for the CI process, until 5.x is really end of life
(meaning no applications left to upgrade).


## Running tests with Maven

### Setup ~/dev-configs for Across development

This allows you to easily run integration tests from both Maven and
IntelliJ.

Symlink the `across-test.properties`. From the top-level directory, run:

	mkdir -p ~/dev-configs
	(cd ~/dev-configs/ && ln -s $OLDPWD/across-test.properties across-test.properties)

Note that the only difference with the `across-test.properties` from
the `across-framework` repository should be the hostnames: they are
all `127.0.0.1`, as opposed to the GitLab service `alias`.


### docker-compose for databases

The instructions here do not use `testcontainers` for the relational
databases, because:

- The tests in GitLab CI/CD don't use `testcontainers` either for
  relational databases.

- It is much faster to start a database server once in the background,
  and then reuse it all the time, than to start one for each test case
  (or at least every time there is a `@DirtiesContext`, and there are
  a lot of those!)

Other `testcontainers` are still used, since they are used only very
occasionally.

To start all database servers, simply run:

	docker-compose up

Or each one individually:

	docker-compose up mssql
	docker-compose up mysql
	docker-compose up oracle
	docker-compose up postgres


### Maven integration tests

To run the integration tests locally, run either of:

	axitest -DacrossTest.datasource=h2
	axitest -DacrossTest.datasource=mssql
	axitest -DacrossTest.datasource=mysql
	axitest -DacrossTest.datasource=oracle
	axitest -DacrossTest.datasource=postgres


# Running tests in IntelliJ

Many Across repositories have an IntelliJ run configuration for each
database to run all integration tests. Obviously you need to have the
database(s) running using `docker-compose` (see above).

