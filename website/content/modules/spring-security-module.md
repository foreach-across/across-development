---
weight: 302
title: Spring Security module
repo-id: across-base-modules
module-name: SpringSecurityModule
---

The `SpringSecurityModule` activates Spring security in the Across
context and allows other modules to make use of the security
infrastructure, as well as to make security configuration changes (eg.
register additional security filters).

It also provides some additional infrastructure for custom security
principals.

This module is required to work with Spring security in an Across
application. It is a replacement for the Spring Boot security starter in
an Across setup.

### Artifacts

The SpringSecurityModule dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>spring-security-module</artifactId>
    </dependency>
