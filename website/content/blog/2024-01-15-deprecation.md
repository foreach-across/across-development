---
title: "Across deprecation"
date: 2024-01-11T13:00:00+01:00
author: Davy
draft: true
pin: true
---

TODO: summary

<!--more-->


<!--
See also: https://confluence.hosted-tools.com/display/AX/Across+Alternatives
-->

Refer to https://spring.io/projects/spring-modulith


# Some alternatives

## User authentication and management

Use an off-the-shelf platform for this, it's essential for security
anyway, and it's near-trivial to use these platforms using Spring
Security.

For internal users, Microsoft Entra Id (formerly Azure Active
Directory or Azure AAD), and Okta are popular.

For external users, use social logins (Google, Facebook, ...) or a
Customer Identity and Access Management (CIAM) platform such as Auth0,
Azure AD B2C, Amazon Cognito, ... Or use a CIAM that also handles the
social logins for you.

There are also open source platforms such as Keycloak, Apache Shiro or
Spring Authorization Server ... But ask yourself: do you really want
to manage passwords, multi-factor-authentication, passkeys, dealing
with new vulnerabilities every week, fending off hackers or even
nation-state cyberwarfare? In a platform you manage yourself?


## Image Server

- Akamai image optimization

- https://www.cloudflare.com/developer-platform/cloudflare-images/


## File Manager

Take a look at Apache JClouds, but you may want to check if you can
easily use it with a cloud-native identity library such as
`azure-identity`, or at least with a secret vault.

<!--
Maybe mention:
https://en.wikipedia.org/wiki/Law_of_the_handicap_of_a_head_start (first-mover disadvantage)
https://nl.wikipedia.org/wiki/Wet_van_de_remmende_voorsprong
-->

