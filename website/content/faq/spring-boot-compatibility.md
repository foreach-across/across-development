---
title: Spring Boot Compatibility
weight: 6
toc: true
---

### How is Across different from Spring Boot?

Across builds much more on top of Spring Framework than on Spring Boot.
Across applications execute as a Spring Boot application and use some
features provided by Spring Boot (like embedded webserver, YAML
configuration and devtools).

Auto-configuration, however, is not supported, which means simply adding
a starter to your project will not be enough. Many available
configuration classes from Spring Boot will also not work in an Across
application, because they are setup for a single `ApplicationContext`,
whereas Across uses a different hierarchy.

See the [across-autoconfigure
documentation](../across-autoconfigure-docs.html) for the list of
supported starters, and more information on how to make others
compatible.

There is often no actual limitation to using the starter libraries, but
some effort might be required to get the right configuration. We can
offer commercial support for this if required.


### How is Across different from Spring Framework?

Across builds on top of Spring framework and tries to stay as compatible
as possible. There are some important differences, however.

#### ApplicationContext hierarchy

Across builds an entire `ApplicationContext` hierarchy where every
module is its own `ApplicationContext`. A medium Across application
easily has 5 to 10 `ApplicationContext` instances. As a simplified
comparison: many classic Spring Framework web applications have two
`ApplicationContext` instances, a Spring Boot application usually has
only one.

You can use all features of Spring framework or related libraries in
Across applications, but due to the `ApplicationContext` hierarchy,
sometimes additional setup is required. Beans are only shared between
contexts if they are exposed, and a module `ApplicationContext` can only
access a bean from another module if the other module has already
started (unless an Across-specific mechanism like `@PostRefresh` is
being used).

#### ApplicationContext and implicit bean ordering

In a single `ApplicationContext`, you cannot rely on any bean ordering
unless you set it explicitly. Beans are only considered to be ordered if
they have an `@Order` annotation, or if they implement the `Ordered`
interface.

In an Across application, inter-module ordering must be reliable and is
determined by the dependencies that modules have on each other. The
actual order of modules is determined at bootstrap time and never
changed after. This ordering is used extensively throughout an Across
application:

-   Modules are started in order (and stopped in reverse order).
-   Installers are executed in module order, no matter during which
    bootstrap phase.
-   Event handlers are executed in module order.
-   `@RefreshableCollection` always returns the list in module order.

Explicit ordering using the `@Order` annotation can be used to order
beans regardless of module dependencies. An alternative `@OrderInModule`
is available if you only want to influence relative ordering of beans
within a module.

#### Events

Across uses its own event bus for publishing events. You can simply use
the Spring `ApplicationEventPublisher` and `@EventListener` annotations,
but how events are dispatched is subtly different in order to ensure
they get handled in Across module order.


### Can I use Spring Boot devtools with Across applications?

Absolutely.

Support for devtools is present when using `@AcrossApplication` to
configure your application. The [Across
Initializr](http://start-across.foreach.be) projects always add devtools
to their project structure.
