---
title: Across Platform 2.1.1 released
date: 2018-07-24
author: The Across Team
toc: true
---

This release upgrades several modules and related dependencies. Mostly
bugfixes and security patches, with the addition of some minor features.

<!--more-->

## Upgrading

Upgrading from 2.1.0 should be seamless, and we advise developers to do
so when possible.

## What's new

This section lists some of the more notable changes included in this
release. Full details can be found in the [release
notes](across-platform-2-1-1-released.html#whats-new-sections) of the
corresponding modules.

### Spring Platform Brussels-SR11

Across Platform 2.1.1 upgrades the Spring Platform dependency
to [Brussels-SR11](https://docs.spring.io/platform/docs/Brussels-SR11/reference/htmlsingle/)
which includes several security patches and third-party dependency
updates.

### Auto-configuration support

Auto-configuration support has been added for [Spring Cloud
OpenFeign](https://docs.across.dev/across-site/production/across-autoconfigure/1.0.1/starters/spring-cloud.html#_spring_cloud_openfeign)
and
[GraphQL](https://docs.across.dev/across-site/production/across-autoconfigure/1.0.1/starters/contributed-starters.html#_spring_boot_graphql)
starters.

### BootstrapUiModule 2.1.0

New component has been added to make it easier to [change the control
names of generated form
controls](https://docs.across.dev/across-site/production/bootstrap-ui-module/2.1.0/guides/prefixing-control-names.html).

### WebCmsModule 0.0.5

Fixes a bug where the use of double square brackets in text components
got evaluated as Thymeleaf expressions.

### OAuth2Module 2.0.1

Fixes a performance issue with the Hibernate mapping of the
`OAuth2Client` entity. In a setup without caching performance would
deteriorate exponentially for every client added.

### EntityModule 3.1.0

- EntityModule now uses `evo-inflector` to auto-generate plural forms,
  this should yield better results in English
- it is now possible to customize the format of `Auditable` properties
  using message codes
- several bugfixes and improvements related to `EntityQuery` and EQL
  filtering

### DynamicFormsModule 0.0.1

Across Platform 2.1.1 is the first iteration that contains
the [Documents & Forms module](../modules/documents-and-forms.html).
This is a new standard module that provides some services to define a
custom document and have data entry/retrieval for those documents. It
can be used as the basis for dynamic forms and simple data entry.

Version 0.0.1 is the first development version published. See the
separate documentation section (work in progress) for more information
on what you can do with it and how to use.

## <span id="whats-new-sections"></span>Release notes

Links to the different what's new sections of the updated modules:

|                                                                                                                                  |                 |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------|
| [Across Platform](https://docs.across.dev/across-site/production/across/2.1.1/releases/platform/2.1.1.html)                      | `2.1.1.RELEASE` |
| [Across Core & Web](https://docs.across.dev/across-site/production/across/2.1.1/releases/core-artifacts/releases-3.x.html#3-1-0) | `3.1.0.RELEASE` |
| [Auto-configuration Support](https://docs.across.dev/across-site/production/across-autoconfigure/1.0.1/index.html)               | `1.0.1.RELEASE` |
| [BootstrapUiModule](https://docs.across.dev/across-site/production/bootstrap-ui-module/2.1.0/releases/2.x.html#2-1-0)            | `2.1.0.RELEASE` |
| [WebCmsModule](https://docs.across.dev/across-site/production/web-cms-module/0.0.5/releases/0.0.x.html#0-0-5)                    | `0.0.5.RELEASE` |
| [SpringSecurityModule](https://docs.across.dev/across-site/production/spring-security-module/3.0.2/releases/3.x.html#3-0-2)      | `3.0.2.RELEASE` |
| [OAuth2Module](https://docs.across.dev/across-site/production/oauth2-module/2.0.1/releases/2.x.html#2-0-1)                       | `2.0.1.RELEASE` |
| [EntityModule](https://docs.across.dev/across-site/production/entity-module/3.1.0/releases/3.x.html#3-1-0)                       | `3.1.0.RELEASE` |
| [DynamicFormsModule](https://docs.across.dev/across-site/production/dynamic-forms-module/0.0.1/releases/0.0.x.html#0-0-1)        | `0.0.1.RELEASE` |
