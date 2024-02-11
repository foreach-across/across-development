---
title: Across Platform 2.1.5 released
date: 2019-09-03
author: The Across Team
toc: true
---

This release updates a number of standard modules with new features and
a few bugfixes.

<!--more-->

## Upgrading

Upgrading from 2.1.4 should be seamless, and we advise developers to do
so when possible. Upgrading only individual modules might result in
breaking changes and is not advised.

## What's new

This section lists some of the more notable changes included in this
release. Full details can be found in the [release
notes](across-platform-2-1-5-released.html#whats-new-sections) of the
corresponding modules.

### Across Core & Web 3.2.1

Small configuration changes related to the artifact repositories for the
standard-module-bom.

### AdminWebModule 3.2.0

Added additional message codes to support translations for the login and
dashboard pages.

### BootstrapUiModule 2.2.2

Improved autosuggest controls by adding support for templates and
client-side reconfiguration of datasets

### EntityModule 3.4.0

Most important new features:

- Provided additional support for custom styling by adding additional
  css classes and data attributes
- Support for configuring autosuggest controls
- Added a new ViewElementMode `ViewElementMode.FORM_GROUP` to support
  the configuration of form groups for basic filter controls
- Added support for marking entity queries and conditions as
  translated, for cases where non-registered properties should be
  queried.

## <span id="whats-new-sections"></span>Release notes

Links to the different what's new sections of the updated modules:

|                                                                                                                            |                 |
|----------------------------------------------------------------------------------------------------------------------------|-----------------|
| [Across Platform](https://docs.across.dev/across-site/production/across/releases/platform/2.1.5.html)                      | `2.1.5.RELEASE` |
| [Across Core & Web](https://docs.across.dev/across-site/production/across/releases/core-artifacts/releases-3.x.html#3-2-1) | `3.2.1.RELEASE` |
| [AdminWebModule](https://docs.across.dev/across-site/production/admin-web-module/releases/3.x.html#3-2-0)                  | `3.2.0.RELEASE` |
| [BootstrapUiModule](https://docs.across.dev/across-site/production/bootstrap-ui-module/releases/2.x.html#2-2-2)            | `2.2.2.RELEASE` |
| [EntityModule](https://docs.across.dev/across-site/production/entity-module/releases/3.x.html#3-4-0)                       | `3.4.0.RELEASE` |
