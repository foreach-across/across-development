---
weight: 404
title: Admin Web
aliases:
  - AdminWebModule

repo-id: across-entity-admin-modules
module-name: AdminWebModule
---

The `AdminWebModule` provides infrastructure for building a secured
administration section in your site. It sets up a default security layer
with a form login, and provides a Bootstrap based layout for the UI.

<!--more-->

Any module can provide one or more `@AdminWebController` components that
make up the admin UI. These will automatically be detected and mapped
behind the secured Admin Web section.

Several other modules automatically provide a management UI if
AdminWebModule is present in the application.

### Artifacts

The Admin Web dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>admin-web-module</artifactId>
    </dependency>
