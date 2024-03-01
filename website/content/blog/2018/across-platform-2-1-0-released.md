---
title: Across Platform 2.1.0 released
date: 2018-04-03
author: The Across Team
toc: true
---

[Across Platform
2.1.0](https://docs.across.dev/across-platform/2.1.0.RELEASE/reference/#2-1-0-release)
bumps Across Core to a new major version (3.x) that greatly improves
compatibility with standard Spring and Spring Boot. The Spring Boot
dependency has also been updated from 1.4.x to 1.5.x.

This platform upgrade has a lot of updated modules, both with new
features and technical (sometimes breaking) refactorings/improvements.
We strongly advise you to read the [module specific release
notes](across-platform-2-1-0-released.html#whats-new-sections) for all
details.

<!--more-->

## Migration guide

Platform 2.1.0 includes some major updates related to improving Spring
Boot 1.5 compatibility. This introduces some breaking changes that
require you to update your existing code base. A separate [migration
guide](https://docs.across.dev/across-platform/2.1.0.RELEASE/reference/migration-2.0.x-to-2.1.x.html)
has been provided to help upgrading from platform 2.0.x to 2.1.0.

## What's new

This chapter contains an excerpt of the more noteworthy changes.

### Across Autoconfigure 1.0.0

A separate `across-autoconfigure` artifact has been added that adds
Spring Boot autoconfiguration support for many Spring Boot starters.
This is the new base dependency for most of your projects and can
replace the separate dependencies to `across-core` and `across-web`
artifacts.

See the [across-autoconfigure documentation
section](https://docs.across.dev/across/3.0.0.RELEASE/reference/spring-boot.html#spring-boot)
for more information.

### Across Core 3.0.0

- better support for Spring Boot autoconfiguration
- addition of `@ConditionalOnAcrossModule` for conditional component
  creation
- overhaul of the event handling system: the standard Spring Framework
  `@EventListener` infrastructure replaces the previous `@Event`
  implementation
- better startup failure feedback when running as a
  `SpringApplication`
- improved `@ModuleConfiguration` support
- `@InstallerMethod` now supports method arguments which will be
  autowired when executing the method

### Across Web 3.0.0

- major internal refactoring - Spring MVC configuration is now based
  on the Spring Boot autoconfiguration classes
- several improvements have been made to the `Menu` building
  infrastructure
- websocket support is activated automatically if the corresponding
  libraries are on the classpath

### Hibernate JPA module 3.0.0

- internal refactoring - the default configuration now builds on top
  of Spring Boot JPA support
- the Spring Boot JPA properties are now also supported for
  configuration and more property configuration options are available
    - when switching from using the Spring Boot JPA starter (now
      possible with across-autoconfigure), a single
      `AcrossHibernateJpaModule` will transparently take over the
      infrastructure without requiring application changes
- a `PlatformTransactionManager` is now always created and exposed,
  along with a `TransactionTemplate`
- added `AcrossHibernateJpaModule.builder()` to easily create a module
  for an additional `EntityManager`
- it is now possible to add a module extension with an `@EntityScan`
  annotation to specify where to scan for entities

### Spring Security module 3.0.1

- internal refactoring to re-use the Spring Boot auto-configuration
  security classes
- `WebSecurityConfigurer` beans from other modules are now directly
  supported instead of the Across specific
  `SpringSecurityWebConfigurer`
- the default Spring Boot security configuration is applied with some
  minor changes
    - basic authentication for an application can be configured using
      the Spring Boot properties (it is not active by default)

### Admin Web 3.0.1

The `EntityAdminMenu` and `EntityAdminMenuEvent` types have been
deprecated. The new equivalent types in EntityModule should be used
instead.

### Bootstrap UI 2.0.1

- `TooltipViewElement` has been added to quickly generate a tooltip
  icon with a corresponding message
- a `FormGroupElement` now supports a description, a help block and a
  tooltip
- added support for Java 8 date/time types on `DateTimeFormElement`

### EntityModule 3.0.1

- the module dependencies have been optimized: `EntityModule` can now
  be used without `AdminWebModule` or `BootstrapUiModule`
    - the corresponding features are simply disabled when either of
      the modules is missing
- new message codes for adding a tooltip or a help block to a form
  group
- it is now possible to configure default view element modes on an
  `EntityConfiguration`
    - these will determine the default behaviour if none is specified
      on a property level
- added `EntityViewCustomizers` to help customizing entity view
  configuration in a more fluent fashion
    - added helpers for registering an admin menu item or an access
      validator for a custom view
- added the `ExtensionViewProcessorAdapter` base class for easily
  creating a view for a custom extension class
- you can now manually force a property to show as required
- the `EntityLinkBuilder` has been deprecated in favour of a central
  `EntityViewLinks` component with a new `EntityViewLinkBuilder`
    - the new components make it much easier to create (customized)
      links to entity views

### User module 3.0.0

Compatibility updates for the updated SpringSecurityModule.

### Access Control module 3.0.1

- a single `AclPermissionFactory` is now used which makes it easier
  for modules to register custom ACL permissions
- `AclPermissionForm` infrastructure has been added, allowing a
  developer to build a UI for updating ACL permissions for an entity
    - this requires EntityModule and AdminWebModule to be active in
      your application

### Web CMS 0.0.4

Compatibility updates with changes in Across 3.0.0 and EntityModule
3.0.1.

### LDAP module 1.0.1

Minor updates and fixes.

## <span id="whats-new-sections"></span>What's new sections

Links to the different what's new sections of the updated modules:

|                                                                                                                                           |                 |
|-------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| [Across Platform](https://docs.across.dev/across-platform/2.1.0.RELEASE/reference/#2-1-0-release)                                         | `2.1.0.RELEASE` |
| [Across Core](https://docs.across.dev/across/3.0.0.RELEASE/reference/whats-new.html#3-0-0)                                                | `3.0.0.RELEASE` |
| [Across Web](https://docs.across.dev/across/3.0.0.RELEASE/reference/whats-new.html#3-0-0)                                                 | `3.0.0.RELEASE` |
| [AcrossHibernateJpaModule](https://docs.across.dev/across-standard-modules/AcrossHibernateModule/3.0.0.RELEASE/reference/#_3_0_0_release) | `3.0.0.RELEASE` |
| [AdminWebModule](https://docs.across.dev/across-standard-modules/AdminWebModule/3.0.1.RELEASE/reference/#_3_0_1_release)                  | `3.0.1.RELEASE` |
| [BootstrapUiModule](https://docs.across.dev/across-standard-modules/BootstrapUiModule/2.0.1.RELEASE/reference/#2-0-1-release)             | `2.0.1.RELEASE` |
| [WebCmsModule](https://docs.across.dev/across-standard-modules/WebCmsModule/0.0.4.RELEASE/reference)                                      | `0.0.4.RELEASE` |
| [SpringSecurityModule](https://docs.across.dev/across-standard-modules/SpringSecurityModule/3.0.1.RELEASE/reference/#3-0-1-release)       | `3.0.1.RELEASE` |
| [SpringSecurityAclModule](https://docs.across.dev/across-standard-modules/SpringSecurityAclModule/3.0.1.RELEASE/reference/#3-0-1-release) | `3.0.1.RELEASE` |
| [EntityModule](https://docs.across.dev/across-standard-modules/EntityModule/3.0.1.RELEASE/reference/#3-0-1-release)                       | `3.0.1.RELEASE` |
| [UserModule](https://docs.across.dev/across-standard-modules/UserModule/3.0.0.RELEASE/reference/#_3_0_0_release)                          | `3.0.0.RELEASE` |
| [LdapModule](https://docs.across.dev/across-standard-modules/LdapModule/1.0.1.RELEASE/reference/#_1_0_1_release)                          | `1.0.1.RELEASE` |
