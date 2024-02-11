---
weight: 503
title: LDAP Module

repo-id: across-user-auth-modules
module-name: LdapModule
---

`LdapModule` provides a services for connecting to [LDAP](https://ldap.com/) directories. It
provides a domain model for configuring LDAP connections and integrating
them with an authentication layer. If [UserModule](../user-module) is
also present support for synchronizing users and groups from LDAP will
also be active.

<!--more-->


### Artifacts

The LdapModule dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>ldap-module</artifactId>
    </dependency>
