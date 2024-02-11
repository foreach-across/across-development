---
weight: 501
title: Spring Security Acl Module

repo-id: across-user-auth-modules
module-name: SpringSecurityAclModule
---

The `SpringSecurityAclModule` provides infrastructure for securing your
application using Access Control Lists (ACLs). It is built on top of
Spring Security ACL.

Adding `SpringSecurityAclModule` to your application will set up all
infrastructure to create and manage ACLs, as well as to evaluate them
using Spring security (in any module). This module requires an RDBMS
datasource to create the tables for holding the ACL data.

Components are also provided to easily build a user interface for
updating ACLs using [EntityModule](../entity-module).


### Artifacts

The Access Control module dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>spring-security-acl-module</artifactId>
    </dependency>
