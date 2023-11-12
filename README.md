# Across local development

You can use the instructions, scripts and configuration files in this
repository to do local development on Across on your
laptop/desktop/workstation.

The instructions here do not use `testcontainers`, because:

- The tests in GitLab CI/CD don't use `testcontainers` either.

- It is much faster to start a database server once in the background,
  and then reuse it all the time, than to start one for each test case
  (or at least every time there is a `@DirtiesContext`, and there are
  a lot of those!)


# Setup ~/dev-configs for Across development

This allows you to easily run integration tests from both Maven and
IntelliJ.

Symlink the `across-test.properties`. From this directory, run:

	mkdir -p ~/dev-configs
	(cd ~/dev-configs/ && ln -s $OLDPWD/across-test.properties across-test.properties)

Note that the only difference with the `across-test.properties` from
the `across-framework` repository should be the hostnames: they are
all `127.0.0.1`, as opposed to the GitLab service `alias`.


# docker-compose for databases

To start all database servers, simply run:

	docker-compose up

Or each one individually:

	docker-compose up mssql
	docker-compose up mysql
	docker-compose up oracle
	docker-compose up postgres


# Maven integration tests

Pre-requisites:

- Install a JDK 1.8 in `~/.jdks`. The easiest way to do this is to
  download the latest Eclipse Temurin 1.8 JDK using IntelliJ, which
  will put this in the `~/.jdks` directory.

- Install Maven (see the `env.sh` file for the version) in `~/tools`.

And then source the `env.sh` file:

	. env.sh

Alternatively, make sure your `JAVA_HOME` and `MAVEN_HOME` are set
correctly.

To run the integration tests locally, run either of:

	axitest -DacrossTest.datasource=h2
	axitest -DacrossTest.datasource=mssql
	axitest -DacrossTest.datasource=mysql
	axitest -DacrossTest.datasource=oracle
	axitest -DacrossTest.datasource=postgres


# IntelliJ

Most Across repositories have an IntelliJ run configuration for each
database to run all integration tests. Obviously you need to have the
database(s) running using `docker-compose` (see above).
