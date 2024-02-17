---
weight: 502
title: User Module

repo-id: across-user-auth-modules
module-name: UserModule
---

Provides a domain model for users, groups, roles and permissions.
Integrates automatically with [Admin Web Module]({{< relref
"admin-web-module.md" >}}) and [Security Module]({{< relref
"spring-security-module.md" >}}), so you can immediately authenticate
with these users and perform role based security checks.

<!--more-->

When [Admin Web Module]({{< relref "admin-web-module.md" >}}) and
[Entity Module]({{< relref "entity-module.md" >}}) are present,
`UserModule` also provides a user interface for managing the different
entities.


### Artifacts

The UserModule dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>user-module</artifactId>
    </dependency>
