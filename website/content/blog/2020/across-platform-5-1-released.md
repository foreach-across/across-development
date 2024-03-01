---
title: Across platform 5.1 released
date: 2020-12-07
author: The Across Team
toc: true
---

This release updates a number of standard modules with new features and
a few bugfixes.

### Upgrading

Upgrading from 5.0 should be seamless and we advise developers to do so
when possible. Upgrading only individual modules might result in
breaking changes and is not advised.

<!--more-->

## What's new

This section lists some of the more notable changes included in this
release. Full details can be found in the [release
notes](across-platform-5-1-released.html#whats-new-sections) of the
corresponding modules.

### Across Platform and all Standard Modules

- All unit tests have been migrated from Junit 4 to Junit 5.
- All tests that use docker containers (cross database tests, solr,
  ...) have been migrated to use testcontainers.

### Across Core & Web 5.1.0

- Updated to Spring Boot 2.3.5. ([Spring Boot 2.3 release
  notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.3-Release-Notes))
- Dependencies have been removed/updated where they were outdated.
- Added support to make Lazy autowire candidate resolver work.

### Across Auto Configure 2.1.0

- Several downstream dependency updates for cassandra, elasticsearch,
  spring boot admin, graphql

### Across Hibernate Module 4.1.0

- The updated spring-data-commons dependency was updated, which
  requires changes in Sort.by() and PageRequest.of()
- Lazy JPA repositories should now be supported. You can use DEFERRED
  and LAZY as bootstrap mode
- BasicRevisionBasedRepository has been deprecated due to the
  deprecation of Session.createCriteria() in favor of
  BasicRevisionBasedJpaRepository
- Support for complex DTOs with Dozer allowing deep cloning of more
  complex entities

### Spring Security Module 4.1.0

- Minor changes might be required if you use
  SwitchUserGrantedAuthority

## <span id="whats-new-sections"></span>Release notes

Links to the different what's new sections of the updated modules:

|                                                                                                                            |                 |
|----------------------------------------------------------------------------------------------------------------------------|-----------------|
| [Across Platform](https://foreach-across.github.io/ref-docs-5/across/releases/platform/5.x/5.1.0.html)                  | `5.1.0.RELEASE` |
| [Across Core & Web](https://foreach-across.github.io/ref-docs-5/across/releases/core-artifacts/releases-5.x.html#5-1-0) | `5.1.0.RELEASE` |
| [Across Auto Configure](https://foreach-across.github.io/ref-docs-5/across-autoconfigure/releases/2.x.html#2-1-0)       | `2.1.0.RELEASE` |
| [AcrossHibernateModule](https://foreach-across.github.io/ref-docs-5/hibernate-jpa-module/releases/4.x.html#4-1-0)       | `4.1.0.RELEASE` |
| [SpringSecurityModule](https://foreach-across.github.io/ref-docs-5/spring-security-module/releases/4.x.html#4-1-0)      | `4.1.0.RELEASE` |
