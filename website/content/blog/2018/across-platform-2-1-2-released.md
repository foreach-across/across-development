---
title: Across Platform 2.1.2 released
date: 2018-11-19
author: The Across Team
toc: true
---

This release upgrades several modules and related dependencies. Mostly
bugfixes and security patches, with the addition of some minor features.

<!--more-->

## Upgrading

Upgrading from 2.1.1 should be seamless, and we advise developers to do
so when possible. Upgrading only individual modules might result in
breaking changes and is not advised.

## What's new

This section lists some of the more notable changes included in this
release. Full details can be found in the [release
notes](across-platform-2-1-2-released.html#whats-new-sections) of the
corresponding modules.

### Spring Platform Brussels-SR14

Across Platform 2.1.2 upgrades the Spring Platform dependency
to [Brussels-SR14](https://docs.spring.io/platform/docs/Brussels-SR14/reference/htmlsingle/)
which includes several security patches and third-party dependency
updates.

### Auto-configuration support

Auto-configuration for HATEOAS has been improved.

### AdminWebModule 3.1.0

The user context menu (logout link) can be more easily customized and is
preconfigured to support avatar images.

### BootstrapUiModule 2.1.1

A `ScriptViewElement` component has been added which can be used for
embedding HTML templates as script blocks. Nested blocks are supported
with client-side javascript to transparently resolve them. This
construct is mainly useful for situations where you wish to use
`ViewElements` to render template blocks which will be used in
javascript.

### DynamicFormsModule 0.0.2

Several bugfixes along with some new features:

- Message codes and translations can be managed in a document
  definition.
- Fieldsets support basic styling options.
- Collections of fieldsets are now possible.
- File attachments are possible if FileManagerModule is present in the
  application.
- It's possible to define a summary view (preview) for a document in a
  list view.
- Several improvements to calculated fields.

### EntityModule 3.2.0

Most important new features:

- It's possible for a property or view to define the type of form
  encoding it requires. Especially useful for multipart file uploads.
- Fieldsets now support a template attribute which can be used for
  custom styling.
- A detail (readonly) view is now active by default and it's possible
  to configure an entity to link to the detail view by default,
  instead of to the update form view.
- A list view can be customized to show only the items for which the
  user has a specific `AllowableAction`.
- Embedded association views have been extended: they now have a page
  title and support an additional menu. This allows for more complex
  embedded associations.
- The delete button has been moved to the update form and detail view,
  and removed from the general tab menu. This avoids confusion when
  editing an associated entity.
- Collections of embedded objects are now supported out-of-the-box. A
  default control will allow adding/removing an item from the
  collection, and a single item will render it's own form controls,
  optionally with validation attached.
- Addition of the `EntityPropertiesBinder` and
  `EntityPropertyController`, allowing for more flexibility for
  defining custom properties and related databinding.

Multiple bugfixes and small improvements.

### FileManagerModule 1.3.0

Adds the `FileReference` entity with default file upload support. When
AcrossHibernateJpaModule is available this entity will be provided and
usable as related entity. When EntityModule is present a default control
for single and multiple file uploads will be rendered.

### OAuth2Module 2.1.0

An administration UI for managing OAuth2 clients is now available, built
on top of EntityModule and AdminWebModule.

### WebCmsModule 0.0.6

It's now possible to add some textual metadata to a `WebCmsImage`. A
default image search which searches through all text fields has been
configured.

## <span id="whats-new-sections"></span>Release notes

Links to the different what's new sections of the updated modules:

|                                                                                                                                  |                 |
|----------------------------------------------------------------------------------------------------------------------------------|-----------------|
| [Across Platform](https://docs.across.dev/across-site/production/across/2.1.2/releases/platform/2.1.2.html)                      | `2.1.2.RELEASE` |
| [Across Core & Web](https://docs.across.dev/across-site/production/across/2.1.2/releases/core-artifacts/releases-3.x.html#3-1-1) | `3.1.1.RELEASE` |
| [Auto-configuration Support](https://docs.across.dev/across-site/production/across-autoconfigure/1.0.2/index.html)               | `1.0.2.RELEASE` |
| [AdminWebModule](https://docs.across.dev/across-site/production/admin-web-module/3.1.0/releases/3.x.html#3-1-0)                  | `3.1.0.RELEASE` |
| [BootstrapUiModule](https://docs.across.dev/across-site/production/bootstrap-ui-module/2.1.1/releases/2.x.html#2-1-1)            | `2.1.1.RELEASE` |
| [DynamicFormsModule](https://docs.across.dev/across-site/production/dynamic-forms-module/0.0.2/releases/0.0.x.html#0-0-2)        | `0.0.2.RELEASE` |
| [EntityModule](https://docs.across.dev/across-site/production/entity-module/3.2.0/releases/3.x.html#3-2-0)                       | `3.2.0.RELEASE` |
| [FileManagerModule](https://docs.across.dev/across-site/production/file-manager-module/1.3.0/releases/1.x.html#1-3-0)            | `1.3.0.RELEASE` |
| [OAuth2Module](https://docs.across.dev/across-site/production/oauth2-module/2.1.0/releases/2.x.html#2-1-0)                       | `2.1.0.RELEASE` |
| [UserModule](https://docs.across.dev/across-site/production/user-module/3.1.0/releases/3.x.html#3-1-0)                           | `3.1.0.RELEASE` |
| [WebCmsModule](https://docs.across.dev/across-site/production/web-cms-module/0.0.6/releases/0.0.x.html#0-0-6)                    | `0.0.6.RELEASE` |
