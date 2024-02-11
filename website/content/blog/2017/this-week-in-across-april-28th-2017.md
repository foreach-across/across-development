---
title: This week in Across - April 28th 2017
date: 2017-04-28
author: The Across Team
toc: true
summary: |
  Changes in Across Core, Bootstrap UI Module, Entity UI Module and LDAP module.
---

A short overview of recent changes in the SNAPSHOT versions of the
following modules:

### Aross core 2.0.0

- Base classes for `ViewElementBuilder` now also
  have `addFirst()` methods to add children
- `AcrossModuleMessageSource` no longer falls back to the system
  default locale for resolving property files
- `ContainerViewElementUtils` now has several stream related methods
  for manipulating elements
  like `findAll()`, `removeAll()` and `flatStream()`
- common `ContainerViewElementUtils` methods have been added directly
  on the `ContainerViewElement` for easier use
- Bug fixes:
    - `AbstractViewElementTemplateTest` now clears any default web
      templates before rendering

### BootstrapUiModule 1.0.0

- Added `ViewElement` name rendering [when development mode is
  active](https://docs.across.dev/across-standard-modules/BootstrapUiModule/1.0.0.RELEASE/reference/#_development_mode_rendering)
- Label, control and help block properties of
  a `FormGroupElement` will now be returned by container find
  methods

### EntityUiModule 2.0.0

- List views now support [a custom `EntityQuery` predicate (as EQL
  statement) that will always be applied when fetching list
  items](https://docs.across.dev/across-standard-modules/EntityModule/2.0.0.RELEASE/reference/#eql-predicate-on-list-view)
- Enum property types can have a specific list of selectable values
  configured for form views
- The base entity validators now implement `SmartValidator`  -
  allowing use of validation hints
- Default property controls will have their control name prefixed
  with **entity.** only if they do not have
  an `EntityAttributes.CONTROL_NAME` attribute and if they are native
  property
    - This removes the requirement for some workarounds when manually
      adding (calculated) properties you want to make writable on a
      form
- Bug fixes:
    - Fix issue where table sorting was wrong if the sort property was
      different than the rendered property
    - Fix delete view to use the entity based delete method -
      previously it was id based which caused
      the `EntityInterceptor` delete methods to be skipped
    - Delete tab was not always highlighted in the entity admin menu

### LdapModule 1.0.0

- Extend `LdapEntityProcessedEvent` with boolean methods to indicate
  if it is the first synchronization of the object or an update
