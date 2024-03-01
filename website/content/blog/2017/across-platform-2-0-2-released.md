---
title: Across Platform 2.0.2 released
date: 2017-12-26
author: The Across Team
toc: true
---

[Across Platform
2.0.2](https://docs.across.dev/across-platform/2.0.2.RELEASE/reference/#_what_s_new_in_this_version)
updates a number of the standard modules with new features.

## What's new

A summary of the most important updates included in this release. Refer
to the [module specific
documentation](across-platform-2-0-2-released.html#whats-new-sections)
for all details.

<!--more-->

### Across Core 2.1.1

- `@PostRefresh`now supports method arguments, behaving as an
  equivalent of`@Autowired`but after the Across context has
  bootstrapped.

### AdminWebModule 2.1.1

- [AdminWebModule](../modules/AdminWebModule.html)now has the brand
  new Across logo in its default layout.

### BootstrapUiModule 1.2.0

- `BootstrapUiBuilders` is a new static facade for all builders,
  removing the requirement to wire the `BootstrapUiFactory` or
  `BootstrapUiComponentFactory` bean.
- `TextboxFormElement` has an option to disable line breaks, allowing
  you to create autosizing single-line text boxes.

### WebCmsModule 0.0.3

- Multi domain/multi site support has been added, which is a major
  feature.
- It is now possible to filter the component types that can be created
  on a global level or added as members of a container.
- Text components can have a rich-text profile set using Javascript,
  in order to customize the client-side editor that should be used.
  Default implementations use TinyMCE and CodeMirror.
- `WebCmsAsset` has a `sortIndex` property that can be used for manual
  sorting of assets.
- `WebCmsUrl` and redirects can now also be imported using YAML
  format.

### SpringSecurityModule 2.0.1

This release contains some minor bugfixes.

### EntityModule 2.0.2

[Several
improvements](https://foreachos.gitbooks.io/ax-entity-module/content/whats-new-in-this-version.html)for
building your user interfaces:

- The main admin menu items (like 'Entity management') can now also be
  configured using message codes.
- `EntityQuery`now allows sorting using a `Sort` specifier or by
  providing an `order by` clause in EQL.
- An `OptionIterableBuilder` can now also implement the `isSorted()`
  method to more easily create pre-sorted option lists.
- EntityQuery filtering has been expanded, and a basic filter mode
  with visual controls has been added. Any repository supporting
  EntityQuery can now easily add simple filters to its list views.

## <span id="whats-new-sections"></span>What's new sections

Links to the different what's new sections of the updated modules:

|                                                                                                                                      |                 |
|--------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| [Across Platform](https://docs.across.dev/across-platform/2.0.2.RELEASE/reference/#_2_0_2_release)                                   | `2.0.2.RELEASE` |
| [Across Core](https://docs.across.dev/across/2.1.1.RELEASE/reference/#_2_1_1_release)                                                | `2.1.1.RELEASE` |
| [AdminWebModule](https://docs.across.dev/across-standard-modules/AdminWebModule/2.1.1.RELEASE/reference/#_2_1_1_release)             | `2.1.1.RELEASE` |
| [BootstrapUiModule](https://docs.across.dev/across-standard-modules/BootstrapUiModule/1.2.0.RELEASE/reference/#_1_2_0_release)       | `1.2.0.RELEASE` |
| [WebCmsModule](https://foreachos.gitbooks.io/ax-web-cms-module/whats-new.html)                                                       | `0.0.3.RELEASE` |
| [SpringSecurityModule](https://docs.across.dev/across-standard-modules/SpringSecurityModule/2.0.1.RELEASE/reference/#_2_0_1_release) | `2.0.1.RELEASE` |
| [EntityModule](https://foreachos.gitbooks.io/ax-entity-module/content/whats-new-in-this-version.html)                                | `2.0.2.RELEASE` |

Upgrading from Platform 2.0.1 to 2.0.2 should be seamless. The [Across
Initializr](http://start-across.foreach.be) has been updated to generate
new projects using `2.0.2.RELEASE` by default.
