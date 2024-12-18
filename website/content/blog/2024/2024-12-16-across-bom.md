---
title: "Replacing the Across Application Parent POM with the Across Platform BOM"
date: 2024-12-17T12:00:00+01:00
author: Davy
toc: true
---

This blog introduces the `across-platform-bom`, and explains why it
should be used instead of the `across-application-parent`.

<!--more-->

## Current situation

Currently, Across 5 applications typically use the Across
`across-application-parent` POM like this:

	<parent>
        <groupId>com.foreach.across</groupId>
        <artifactId>across-application-parent</artifactId>
        <version>5.5.1</version>
     </parent>

This has some advantages, but also a very big drawback: an application
cannot by itself upgrade to a new Spring Boot release: this would
require a new release of Across first. That is not the days-long
procedure it was before, but it's still too heavy to do every month.
(which is the cycle of maintenance releases of Spring Boot).  If you
want to support the previous minor release as well (which is what
Spring Boot does), it's two Across release per month. Clearly this is
not sustainable.

Also keep in mind critical security issues could come at any
moment. As an example,
[Log4Shell](https://en.wikipedia.org/wiki/Log4Shell) could still be
handled, because you can update the `log4j2.version` property, and
more or less be done. But you *cannot do that* for Spring Boot itself.

Note also that Across is [deprecated]({{< relref
2024-01-15-deprecation.md >}}), and the only maintenance that it
receives are Spring Boot upgrades.


## Goal

We want to move to a situation where:

- We minimize the number of Across releases.

- But still upgrade on a regular basis (e.g. each minor release of
  Spring Boot).

- And allow applications to upgrade to the latest patch release (the
  `z` in `x.y.z`) of Spring Boot by themselves. In fact this might
  even work with minor Spring Boot upgrade (where the `y` in `x.y.z`
  goes up), and that has in fact been done in Project C.


## Solution

The best solution for this, is to treat Across as just another
library, not as a platform that prevents even patch upgrades.

This is widely done by many projects using a [Bill-of-Materials
POM](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#Bill_of_Materials_.28BOM.29_POMs),
for instance:

- [JUnit BOM](https://junit.org/junit5/docs/current/user-guide/#running-tests-build-maven-bom).
- [Jackson BOM](https://github.com/FasterXML/jackson-bom)
- [Spring Framework BOM](https://central.sonatype.com/artifact/org.springframework/spring-framework-bom)
- [Spring Security BOM](https://central.sonatype.com/artifact/org.springframework.security/spring-security-bom)
- [Spring Data BOM](https://central.sonatype.com/artifact/org.springframework.data/spring-data-bom)
- ...


## Across Release Schedule Proposal

A concrete proposal for an Across release schedule could be as
follows:

- One `x.y.0` release, as soon as a minor new version of Spring Boot
  is released.
- One `x.y.1` release, when the last maintenance release of the
  corresponding Spring Boot is released.

If necessary, there could be maintenance releases in between of
course, but that should be rare.

Applications can then upgrade every month to the latest patch release
of Spring Boot, by themselves, without the need for an Across
release. This is as simple as incrementing the version number in the
`parent` of the root `pom.xml` of the application.

Doing this every month means:

- That the delta is always small.
- You are always ready for a sudden out-of-band fix for an important
  vulnerability.


## Migrating

First run:

	mvn org.apache.maven.plugins:maven-dependency-plugin:3.8.1:list -DoutputFile=dependency-old.list.txt
	mvn org.apache.maven.plugins:maven-dependency-plugin:3.8.1:tree -DoutputFile=dependency-old.tree.txt

You could for instance also commit those files Git (but without the
`-old` suffix then).

Replace the parent in your root `pom.xml`:

	<parent>
		<groupId>com.foreach.across</groupId>
		<artifactId>across-application-parent</artifactId>
		<version>5.5.1</version>
	</parent>

with:

	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.7.18</version>
	</parent>

Add the following properties:

    <foreach-common-bom.version>2.0.0</foreach-common-bom.version>
    <across-framework.version>5.5.1</across-framework.version>
    <across-platform.version>5.5.1</across-platform.version>

And under `dependencyManagement/dependencies` add:

	<dependency>
		<groupId>com.foreach.across</groupId>
		<artifactId>across-platform-bom</artifactId>
		<version>${across-platform.version}</version>
		<type>pom</type>
		<scope>import</scope>
	</dependency>
    <dependency>
		<groupId>com.foreach.libs</groupId>
		<artifactId>common-bom</artifactId>
		<version>${foreach-common-bom.version}</version>
		<type>pom</type>
		<scope>import</scope>
    </dependency>

Now build everything again: in principle this should not give any issues.

You should now check if there are any dependencies whose version have
changed. Run these commands again, but with a `-new` suffix:

	mvn org.apache.maven.plugins:maven-dependency-plugin:3.8.1:list -DoutputFile=dependency-new.list.txt
	mvn org.apache.maven.plugins:maven-dependency-plugin:3.8.1:tree -DoutputFile=dependency-new.tree.txt

Then diff them using your preferred diff tool (`kdiff3`, `meld`,
WinMerge, ...), for instance:

	kdiff3 dependency-old.list.txt dependency-new.list.txt

*Study those differences carefully*: there will likely be differences,
and it's now your responsibility to manage that. You will likely need
to upgrade at least Spring Framework 5.3 and Spring Security 5.8,
because they still had important releases (up to August 2024) after
the last Spring Boot 2.7 release (November 2023). Add the following
properties:

    <spring-framework.version>5.3.39</spring-framework.version>
    <spring-security.version>5.8.14</spring-security.version>

You may also want to take particular care of Liquibase, since upgrades
or downgrades of Liquibase may have quite a bit of impact.


## Disadvantages

Note this has disadvantages too: the tradeoff is: you are in control,
but you will have more work. It's analogous to the tradeoff between
inheriting from `spring-boot-starter-parent` vs importing
`spring-boot-dependencies`, which is discussed succinctly here:

https://www.baeldung.com/spring-boot-dependency-management-custom-parent


## 5.2.2

Note: The `across-platform-bom` was introduced in the [5.2.2
Release notes]({{<ref
"/release-notes/5.2.2.md#using-522-with-spring-boot-25-or-26" >}}),
but it was still somewhat experimental then. It's been in use in a
very active project for over a year now, so it's definitely stable.


