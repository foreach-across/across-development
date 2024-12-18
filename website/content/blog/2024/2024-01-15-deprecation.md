---
title: "Across deprecation"
date: 2024-01-11T13:00:00+01:00
lastmod: 2024-12-17T13:00:00+01:00
author: Davy
toc: true
pin: true
---

Across development will be very limited from now on, basically only
upgrading to newer Spring Boot versions. Modules that are not used
anymore, will be gradually removed as applications will migrate away
from Across.

You should definitely not start any new projects with Across.

A more lightweight alternative is [Spring
Modulith](https://spring.io/projects/spring-modulith).


<!--more-->


<!--
See also: https://confluence.hosted-tools.com/display/AX/Across+Alternatives
-->


# Some alternatives

Here are some alternatives for the functionality provided by some of
the Across modules.

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
to manage passwords, multi-factor-authentication, the up-and-coming
passkeys, dealing with new vulnerabilities every week, fending off
hackers or even nation-state cyberwarfare? In a platform you manage
yourself?

There are many others as well, often written in Go:

- https://casdoor.org/

- https://github.com/JanssenProject/jans: Project behind
  [Gluu](https://gluu.org/foss/)

- https://github.com/aerobase

- https://www.shibboleth.net/

- https://github.com/ory (Germany)

- https://github.com/authelia/authelia

- https://github.com/zitadel/zitadel (Switzerland)

- https://github.com/goauthentik/authentik (not Go, but Python)

and a whole bunch of others.


## Image Server

- [Cloudinary](https://cloudinary.com/)

- [Akamai image optimization](https://techdocs.akamai.com/ivm/docs/optimize-images)

- [Cloudflare Images](https://www.cloudflare.com/developer-platform/cloudflare-images/)

Self-hosted options, see for instance:
https://github.com/topics/image-server

There are lots of Golang-based options, all using `libvips` underneath:

- [imgproxy](https://github.com/imgproxy/imgproxy) seems like the
  leader of the pack. It uses the MIT-license for the open source
  version, and the commercial version has [much more
  features](https://imgproxy.net/features/) (not that we need those,
  except perhaps the option to select the resizing
  algorithm). Supports Azure Blob Storage, which most others don't.

- [imaginary](https://github.com/h2non/imaginary): development seems
  to still happen, but there hasn't been a release since mid-2020, which
  is also the last time the [docker
  image](https://hub.docker.com/r/h2non/imaginary) was updated.

- [Imagor](https://github.com/cshum/imagor) looks like another great option:

  - Written in Go, with an official docker image available (<100MB)

  - Uses Thumbor URL syntax for which there is a good-looking Java client for
    this, which includes handling the HMAC:
    https://github.com/square/pollexor

Then there is [Thumbor](https://www.thumbor.org/) itself of course
(Python, MIT license).

In Java, there is [Cantaloupe](https://cantaloupe-project.github.io/)
(custom license, seems BSD/MIT style).

https://www.imageflow.io/, C++/Rust core library, with a [dotNET based
server](https://github.com/imazen/imageflow-dotnet-server) (AGPL).

[Scrimage](https://sksamuel.github.io/scrimage/) is a
Java/Kotlin/Scala library for image manipulation (Apache 2.0 license).

See also: https://github.com/libvips/libvips/wiki/Projects-using-libvips

The Caddy web server has a number of modules for manipulating images,
resize, crop, etc: Search for "image" in the [list of
modules](https://caddyserver.com/docs/modules/).


## File Manager

Most of the functionality of the Across {{< module-ref
file-manager-module >}} has been extracted to a Maven module in the
[Foreach Common Java Libraries (FCJL)]({{< relref fcjl-2.0.0.md >}}),
with no dependencies on Across, so if you rely on specific behaviour
of the `file-manager-module`, such as the
[`CachingFileRepository`](https://foreach-across.github.io/ref-docs-5/file-manager-module/file-repositories/caching.html),
this is your best alternative.

Another interesting option is the [Apache JClouds blob store
support](https://jclouds.apache.org/start/blobstore/). But you may
want to check if you can easily use it with a cloud-native
authentication (such as [Azure Managed
Identities](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
and [Azure Workload
Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview?tabs=java),
or at least with a secret vault.


<!--
Maybe mention:
https://en.wikipedia.org/wiki/Law_of_the_handicap_of_a_head_start (first-mover disadvantage)
https://nl.wikipedia.org/wiki/Wet_van_de_remmende_voorsprong
-->


## Admin Panels for entity management

Basically many low-code/no-code tools provide this. There are some
open source low-code/no-code tools as
well. [Supabase](https://supabase.com/) for instance has [75kstars on
GitHub](https://github.com/supabase/supabase)

If want to stick to the Java world, there is:

- [Jmix](https://www.jmix.io/), based on Vaadin
- [Apache Causeway](https://causeway.apache.org/), based on Apache Wicket

Outside the Java world, there's of course the originals:

- [Ruby on Rails](https://rubyonrails.org/)
- [Python Django](https://www.djangoproject.com/)

The most promising option comes from the front-end / React world: 

[React-admin](https://marmelab.com/react-admin/) (check out the
[demo's](https://marmelab.com/react-admin/Demos.html)!), which can
easily be combined with a Java backend. The open-source version
provides much of what you need, but you probably need the entreprise
version: the pricing is fair, and they have [a pretty good blog series
about how they got to their business model and
goals](https://marmelab.com/blog/2023/11/08/open-source-profit-1.html).

Another interesting option is the combination of React-admin,
PostgreSQL, and [PostgREST](https://postgrest.org). Marmelab has a
[good
blog](https://marmelab.com/blog/2024/11/04/postgrest-revolutionizing-web-development-with-instant-apis.html)
about that too. Supabase is also based on PostgREST.
