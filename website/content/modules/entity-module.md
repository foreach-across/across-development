---
weight: 405
title: Entity Module

repo-id: across-entity-admin-modules
module-name: EntityModule
---

`EntityModule` provides the developer with infrastructure for building
user interfaces to manage the entities of an application.

<!--more-->

At the heart is the `EntityRegistry`, which contains a map of all
available entities in the application. An entity is backed by an
`EntityConfiguration`, which is a full metamodel of what makes up the
entity and possibly how it can be identified, fetched and persisted.
Based on the available entity model, default administration screens in
[Admin Web]({{< relref "admin-web-module.md" >}}) can be
generated. These can also be fully customized and extended using
configuration classes and custom components.

EntityModule has built-in support for Spring Data repositories. All
Spring Data repositories in an application will be detected and
registered. A CRUD UI for those entities will be available with
sorting and searching capabilities where possible.

### Artifacts

The EntityModule dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>entity-module</artifactId>
    </dependency>
