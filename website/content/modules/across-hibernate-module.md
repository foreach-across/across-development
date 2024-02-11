---
weight: 301
title: Hibernate JPA module
aliases:
  - AcrossHibernateJpaModule

repo-id: across-base-modules
module-name: AcrossHibernateJpaModule
---

The `AcrossHibernateJpaModule` activates JPA support for an entire
Across application. It allows other modules to subscribe their entities
to the shared JPA `EntityManager` represented by the
`AcrossHibernateJpaModule`. The JPA implementation is built on top of
Hibernate.

<!--more-->

This module also activates support for Spring
Data `JpaRepository` implementations and comes with a set
of [helpers](https://across-docs.foreach.be/across-standard-modules/AcrossHibernateModule/3.0.0.RELEASE/reference/#base-classes) to
facilitate repository and entity implementations.

The `AcrossHibernateJpaModule` is compatible with regular Spring Boot
JPA starter. If you have an Across application using JPA in your
application module, you can add this module to your application, and it
will transparently take over the `EntityManager` creation.

### Artifacts

The Hibernate JPA module dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>across-hibernate-module</artifactId>
    </dependency>
