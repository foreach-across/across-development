---
title: Across Platform 5.0.1 released
date: 2020-06-23
author: The Across Team
toc: true
---

Platform 5.0.1 is a major release containing numerous breaking changes.
It is the first release using the Spring Boot 2 line.

## Upgrading

Upgrading from 2.1.5 will not be trivial, due to major upgrades in the
Spring line as well. Developers are encouraged to thorougly read the
separate module release notes and follow the [migration
guide](https://docs.across.dev/across-site/production/migration/platform-2.1-to-5.0/index.html)
when upgrading.

<!--more-->

## What's new

This section lists some of the more notable changes included in this
release. Full details can be found in the [release
notes](across-platform-5-0-1-released.html#whats-new-sections) of the
corresponding modules.

### Across Core & Web 5.0.1

- Upgrade to Spring Boot 2.1.12 and Spring Framework 5.1.13.
- Improvements made to module configurations and the bootstrapping of
  ApplicationContexts.
- Refactoring of ViewElement and ViewElementBuilder infrastructure .
    - Includes improvements in extendability and customization through
      WitherSetter and WitherGetters.
- Removal of several deprecated classes.

### SpringSecurityModule 4.0.0

- Improvements (with breaking changes) regarding the web security
  infrastructure.
- Rework of the default authentication regarding SecurityPrincipals.
- Minor performance improvements due to becoming an extension module.

### DebugWebModule 3.0.0

- Support for viewing the registered security filter chains.
- Added a new cache browser section.

### BootstrapUiModule 3.0.0

- Upgraded the bootstrap dependency to Bootstrap 4, as well as various
  external libraries to their Bootstrap 4 variants.
- Several dependencies are now pulled in via webjars.
- Rework of ViewElement infrastructure. BootstrapUiBuilders has been
  removed in favour of BootstrapViewElements which provides access to
  view elements and their builders through static variables, including
  the removal of attributes in favour of WitherSetter and
  WitherGetters.

### EntityModule 4.0.0

- Updated the behaviour of EntityLinkBuilder due to Spring 5 changes
  concerning the URL encoding of parameters
- Improvements regarding manual entity registration.
- Improved support for customizing redirect and feedback messages
  after creating/saving/deleting an entity.

### FileManagerModule 2.0.0

Added support for Azure Blob storage repositories.

### ImageServerModules 6.0.0

- Reworked file storage to using FileManagerModule with specific
  repository ids.
- Added support for PDF files when ghostscript is present
- Added support for more advanced transformations on images.

### AcrossBootstrapTheme 0.0.1

Almost all styling and theming has been removed from the standard
modules, which leaves them with a clean bootstrap theme. An additional
module has then been introduced to improve customizations and
themability for across applications.

## <span id="whats-new-sections"></span>Release notes

|                                                                                                                              |               |
|------------------------------------------------------------------------------------------------------------------------------|---------------|
| [Across](https://docs.across.dev/across-site/production/across/releases/core-artifacts/releases-5.x.html#5-0-0)              | 5.0.1.RELEASE |
| [Across Autoconfigure](https://docs.across.dev/across-site/production/across-autoconfigure/index.html)                       | 2.0.0.RELEASE |
| [AcrossHibernateModule](https://docs.across.dev/across-site/production/hibernate-jpa-module/releases/4.x.html#4-0-0)         | 4.0.0.RELEASE |
| [SpringSecurityModule](https://docs.across.dev/across-site/production/spring-security-module/releases/4.x.html#4-0-0)        | 4.0.0.RELEASE |
| [DebugWebModule](https://docs.across.dev/across-site/production/debug-web-module/releases/3.x.html#3-0-0)                    | 3.0.0.RELEASE |
| [LoggingModule](https://docs.across.dev/across-site/production/logging-module/releases/3.x.html#3-0-0)                       | 3.0.0.RELEASE |
| [EhCacheModule](https://docs.across.dev/across-site/production/ehcache-module/releases/2.x.html#2-0-0)                       | 2.0.0.RELEASE |
| [SpringMobileModule](https://docs.across.dev/across-site/production/spring-mobile-module/releases/3.x.html#3-0-0)            | 3.0.0.RELEASE |
| [BootstrapUiModule](https://docs.across.dev/across-site/production/bootstrap-ui-module/releases/3.x.html#3-0-0)              | 3.0.0.RELEASE |
| [AdminWebModule](https://docs.across.dev/across-site/production/admin-web-module/releases/4.x.html#4-0-0)                    | 4.0.0.RELEASE |
| [ApplicationInfoModule](https://docs.across.dev/across-site/production/application-info-module/releases/2.x.html#2-0-0)      | 2.0.0.RELEASE |
| [EntityModule](https://docs.across.dev/across-site/production/entity-module/releases/4.x.html#4-0-0)                         | 4.0.0.RELEASE |
| [SpringSecurityAclModule](https://docs.across.dev/across-site/production/spring-security-acl-module/releases/4.x.html#4-0-0) | 4.0.0.RELEASE |
| [PropertiesModule](https://docs.across.dev/across-site/production/properties-module/releases/2.x.html#2-0-0)                 | 2.0.0.RELEASE |
| [UserModule](https://docs.across.dev/across-site/production/user-module/releases/3.x.html#4-0-0)                             | 4.0.0.RELEASE |
| [OAuth2Module](https://docs.across.dev/across-site/production/oauth2-module/releases/3.x.html#3-0-0)                         | 3.0.0.RELEASE |
| [LdapModule](https://docs.across.dev/across-site/production/ldap-module/releases/2.x.html#2-0-0)                             | 2.0.0.RELEASE |
| [SpringBatchModule](https://docs.across.dev/across-site/production/spring-batch-module/releases/2.x.html#2-0-0)              | 2.0.0.RELEASE |
| [FileManagerModule](https://docs.across.dev/across-site/production/file-manager-module/releases/2.x.html#2-0-0)              | 2.0.0.RELEASE |
| [ImageServerModules](http://project-docs.foreach.be/projects/image-server/6.0.0.RELEASE/reference/6.0.0.RELEASE/reference/)  | 6.0.0.RELEASE |
| [WebCmsModule](https://docs.across.dev/across-site/production/web-cms-module/releases/0.1.x.html#0-1-0)                      | 0.1.0.RELEASE |
| [DynamicFormsModule](https://docs.across.dev/across-site/production/dynamic-forms-module/releases/0.1.x.html#3-2-0)          | 0.1.0.RELEASE |
| Across Bootstrap Theme                                                                                                       | 0.0.1.RELEASE |
