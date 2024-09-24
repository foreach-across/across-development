---
title: "Foreach Common Java Libraries 2.0 / 3.0 Release notes"
date: 2024-09-12
author: Davy
toc: true
---

The [Foreach Common Java Libraries
(FCJL)](https://github.com/ForeachOS/foreach-common-java-libraries)
are a set of small libraries, with limited dependencies and limited
scope. Some of these libraries are used by Across, and had to be
updated for Jakarta EE (a requirement for Spring Boot 3 and thus for
Across 6). We made 2.0 and 3.0 releases, and a new module
`common-file-manager` was added.

<!--more-->

## Overview

The last (public) release of these libraries was
[1.1](https://bitbucket.org/beforeach/common-java-libraries/src/common-projects-1.1/). There
was also an internal-only
[1.2](https://bitbucket.org/beforeach/common-java-libraries/src/common-projects-1.2/)
release (for MF), that was not published to Maven Central. The 1.x
branch was still based on Spring Framework 4 and Hibernate 4, but was
compatible with Across 5 (Spring Boot 2, with Spring Framework 5 and
Hibernate 5).

We made a 2.0 branch where all dependencies are aligned with Spring
Boot 2.7.18 (the last (public) Spring Boot 2 release) and a 3.0 branch
where all dependencies are aligned with Spring Boot 3.2. Note that
FCJL itself does *not* depend on Spring Boot: the
`spring-boot-starter-parent` is simply and only used to get a
consistent set of dependency versions.

In both the 2.0 and 3.0 branches, a new module is introduced:
`common-file-manager`: This is an evolution of the Across
`file-manager-module`, where all dependencies on Across have been
removed.

Across 5.5.1 will update the dependencies on FCJL from 1.1 to 2.0.0,
but that should have zero impact.

Lastly, a [Bill-of-Materials (BOM)
`pom.xml`](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#bill-of-materials-bom-poms)
was introduced, so that consuming libraries and applications can
easily import a consist set of libraries.

Releases can be found on Maven Central:

https://central.sonatype.com/search?q=g:com.foreach.libs


## Using FCJL as dependencies in Maven

You will need to add a version property in the `<properties>` of your
root `pom.xml` (typically in the top-level directory). If you are
using Spring Boot 2 (Across 5):
                
	<foreach-common-bom.version>2.0.0</foreach-common-bom.version>

or for Spring Boot 3 (Across 6):

	<foreach-common-bom.version>3.0.0</foreach-common-bom.version>

Then in the `<dependencyManagement>` section under `<dependencies>`,
add:

	<dependency>
		<groupId>com.foreach.libs</groupId>
		<artifactId>common-bom</artifactId>
		<version>${foreach-common-bom.version}</version>
		<type>pom</type>
		<scope>import</scope>
	</dependency>

Adding a dependency is then as simple as adding:

	<dependency>
		<groupId>com.foreach.libs</groupId>
		<artifactId>common-file-manager</artifactId>
	</dependency>


## Removed modules

The `common-test` module was removed in 2.0.0: It provides only one
class and that did not compile with the version of Mockito from Spring
Boot 2.7.18. Across 5.5.0 had a dependency on this module, but it was
not actually used. If it turns out that somebody still needs this, we
can take another look at what the best option forward is.


## common-file-manager

The Across {{< module-ref file-manager-module >}} actually consisted
of three layers:

1. `FileManager` and `FileRepository` and all the implementations
   (local files, (S)FTP, Amazon S3 and Azure Blob storage).

2. `FileReference`, which is a JPA entity. Unfortunately, it is hard
   to factor out because of all the dependencies on the {{< module-ref
   across-hibernate-module >}} and the {{< module-ref
   properties-module >}}. This isn't used by projects C nor G, but it
   is used by project MI. `FileReferenceProperties` does not appear to
   be used anywhere.

3. The admin UI, based on `entity-module` and `admin-web-module`,
   which allows for browsing the file repositories. Obviously we won't
   migrate this as is, but we won't provide a web UI at all. You can
   just use the native tools (such as the [Azure Storage
   Exporer](https://azure.microsoft.com/en-us/products/storage/storage-explorer))
   or use the [IntelliJ Remote File Systems
   plugin](https://plugins.jetbrains.com/plugin/21706-remote-file-systems),
   which supports local files, SFTP, and object storage for all major
   providers. It does not appear to support plain FTP, but there are
   many browsers for that, such as
   [FileZilla](https://filezilla-project.org/) (which supports FTP,
   FTP over TLS (FTPS) and SFTP)

So for now, we factored out only layer 1, into the
`common-file-manager` module. Layer 2 could become
`common-file-manager-jpa`, and as mentioned before, layer 3 will not
be migrated.

Why are we keeping this? 

- This module provides a nice abstraction over file-systems, with some
  fairly specific semantics, such as the caching repository that
  delegates to an actual repository.

- It is needed for some projects, when they remove their dependency on
  Across.

Migration steps:

1. Start by configuring maven with the right dependencies as above,
   and don't forget to remove the dependency on the old
   {{< module-ref file-manager-module >}}.

2. The Java package name for the classes has been changed, so replace:

		com.foreach.across.modules.filemanager

   with:

		com.foreach.common.filemanager
	
   You obviously need to do this in all `.java` files, but there might
   be configuration files that might contain this package name, and
   that need to be adapted as well.

3. {{< module-ref file-manager-module >}} created a `FileManager` bean
   automatically, but now you will need to create your own instance of
   `FileManager(Impl)` and add your repositories to that. Or you might
   use the `FileRepository`s directly if you don't need the
   `FileManager/FileRepositoryRegistry` functionality.

4. Remove the `fileManagerModule` entry from your `application.yml`
   files (and/or `-dev` variants etc), as it will not be picked up
   anymore. You will need to replace this with your own configuration.


## Git repository is moved

The legacy repository is at Bitbucket:
https://bitbucket.org/beforeach/common-java-libraries. This will not
be updated anymore.

The internal repository where development happens is at:
https://gitlab.eindhoven.io-internal.dev/antwerpen/common/foreach-common-java-libraries

And that is mirrored to the public GitHub repository at:
https://github.com/ForeachOS/foreach-common-java-libraries

There is also an old Jira project, but that is not used anymore:
https://foreach.atlassian.net/browse/FJCL
