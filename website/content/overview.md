---
title: Overview
toc: true
---

## Across Framework

{{< across >}} is a Java framework for developing your application using a
modular approach.  It provides a way to define application modules as
well as the infrastructure to run the entire application.  Geared
towards developers with a love for Spring, Across is both free and
open source.

An Across module:

- bundles technical or business domain functionality

- explicitly depends on zero or more other modules

- exposes components like services or repositories for other modules
  to use

- uses exposed components from other modules

- has zero or more installers taking care of things like initial data
  creation or schema migrations

- is a single Spring ApplicationContext


## An Across application

- specifies the modules to use

- sets up common infrastructure (e.g. the event bus)

- ensures modules are ordered according to their dependencies and
  bootstrapped in that same order

- runs as a Spring Boot application


## Across Platform

Across Platform is a set of Across modules that help developers
assemble applications.

There is an [overview of all the modules](/modules) with links to
documentation, Git, Maven Central, and more.


## Learn more

See the documentation for [Across Framework and
Platform](/ref-docs-5/across/).

There are also a few [high-level guides and
tutorials](https://foreach-across.github.io/ref-docs-5/guides/).

Arne and Steven gave a [presentation about Across at Devoxx Belgium in November 2017](https://www.youtube.com/watch?v=00Jn3d12L2M)


[Old website](/old)
