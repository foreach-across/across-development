---
title: Fundamentals
weight: 2
toc: true
---

### What is an Across module?

An Across module bundles technical or business domain functionality,
most often the latter. It represents a single Spring
`ApplicationContext` that holds all the components the module defines
and - optionally - makes these components available to other modules.

Across modules can depend on other modules. These dependencies will
determine the relative order of a module versus other modules in the
same application. A module will start (or ‘bootstrap’) after all the
modules it depends on have already started. During the bootstrap phase a
module can perform one or more initialization tasks through special
installer components.

An Across application is usually made up of multiple Across modules.
Most often a single Across module corresponds with a single jar file,
but this is in no way an actual requirement. Every Across module has a
unique name, and a single module descriptor that describes the basic
configuration of the module.


### What is an Across context?

The Across context is the set of configured modules that make up the
application. There is a single configured Across context in an Across
application.

You can configure the Across context using the `@EnableAcrossContext`
annotation. When you use `@AcrossApplication`, this is already done
behind the scenes. `@AcrossApplication` sets up a Spring Boot
application with a single Across context.

#### Some background

The Across context represents a Spring `ApplicationContext` that is also
the parent `ApplicationContext` of every module that belongs to the
Across context. Usually the Across context itself has a parent
`ApplicationContext`, for example the `EmbeddedWebApplicationContext` of
a Spring Boot application.

#### Terminology

When referring to the **Across application**, we refer to the entire
`ApplicationContext` hierarchy, including the Across context and all its
optional parents. When referring to the **Across context**, we refer
only to the `ApplicationContext` hierarchy of the individual Across
modules and their direct parent.

For simplicity’s sake however, you can consider them the same.


### What is the Across bootstrap?

The Across bootstrap is the actual starting of the application. During
the bootstrapping phase the entire Spring `ApplicationContext` hierarchy
of an application is created.

A typical Across application has the following bootstrap phases:

**1.** The root `ApplicationContext` is scanned, which includes the
configuration of the Across context (represented by the
`@AcrossApplication` annotation).

**2.** The `AcrossContext` bean is created as early as possible:

-   the Across context configuration is analyzed and the modules are
    ordered according to their dependencies;
-   the different module descriptors are offered a chance to customize
    the Across context configuration;
-   the parent Across `ApplicationContext` is created to serve as parent
    for the `ApplicationContext` of individual modules;
-   every module creates its own `ApplicationContext` in the order
    assigned by the Across context;
-   exposed beans are pushed up the `ApplicationContext` hierarchy as
    far as possible.

**3.** Other beans in the root `ApplicationContext` are created; these
can optionally use exposed components from the Across modules.

**4.** The root `ApplicationContext` returns and is ready to be used. In
case of a Spring Boot application, the Spring `ApplicationReadyEvent`
gets published.

Several Across [events are published during
bootstrap](../reference-docs-section-bootstrap-events.html), allowing
modules to interact with each other.

See the [reference documentation section on the Across
bootstrap](../reference-docs-section-across-bootstrap.html) for more
details.


### What is the module descriptor?

The Across module descriptor represents the configuration for a single
Across module. The module descriptor is a class extending
`AcrossModule`. Settings are defined by implementing or overriding
corresponding methods.

The module descriptor takes care of the following:

-   sets the unique name for the Across module;
-   defines the dependencies the module has on other modules using
    `@AcrossDepends`;
-   defines the resources key for the module: this unique key is used to
    search for resources owned by that module in the default locations;
-   describes how the `ApplicationContext` of the module should be
    configured (eg. where to scan for components, etc.);
-   describes where the module defines its installers and module
    extensions;
-   describes which components should be exposed.

Most modules use default settings and only its name, dependencies and
resources key are modified. See the `AcrossModule` class for details on
the overridable methods.

See the [reference documentation on Creating an Across
module](../reference-docs-section-creating-an-acrossmodule.html) for
more information.


### What is an installer and how does it differ from a regular component?

An installer is a special component that performs one or more
installation tasks. Technically, an installer is represented by a simple
class with 2 special attributes:

1.  the `@Installer` annotation that identifies the installer and
    defines the basic metadata for executing the installer: at what
    point and under which conditions;
2.  one or more parameter-less methods annotated with
    `@InstallerMethod`. These represent the actual tasks the installer
    should perform.

Installers are created just like other beans and can access any other
component visible. The major differences with regular module components
are:

-   installer components are **created only if the necessary conditions
    are true**;
-   installer components are created in a separate `ApplicationContext`
    that only exists during the bootstrapping of the Across application.
    **Once the application has fully started, all installers will be
    removed from the memory.**

The phase to which an installer is attached will determine which
components from other modules it can use.

When you want to use installers, a single RDBMS (database) is required
for Across to track installer state between application runs. At the
same time a simple locking mechanism will be used on the database so
multiple applications using the same RDBMS can rely on installers being
executed only once.

See the [reference documentation section on
Installers](../reference-docs-section-installers.html) for more
details.


### What is "exposing beans"?

Exposing beans or components is making them available for other modules.

There are several ways to expose beans, but in most cases it is done by
annotating the bean or its implementing class with `@Exposed`.

#### How this works

Beans are exposed by pushing a special `BeanDefinition` as far up the
`ApplicationContext` hierarchy as possible. Exposing beans has no impact
on the number of bean instances that will get created, it simply makes
them visible in the parent `ApplicationContext`.

All modules have the same parent `ApplicationContext`, so bean
definitions in the parent are available to all modules.

See the [reference documentation on Exposing
beans](../reference-docs-section-exposing-beans.html) for more
details.


### What is "development mode"?

Development mode is a special startup mode of an Across application,
aimed to improve developer productivity. When development mode is
active, modules can load different configuration options.

Examples include:

-   automatic reloading of message sources;
-   automatic reloading of [Thymeleaf](http://www.thymeleaf.org)
    templates;
-   disabling client-side caching of web requests and static resources;
-   adding developer tools in an administration UI.

Development mode is activated by default if a Spring profile called
**dev** is active, but it can also be (de)activated manually.

#### A word of warning

Development mode should never be active on a production environment, as
it will negatively impact performance and might even pose a security
risk.

See the [reference documentation on Development
mode](../reference-docs-section-development-mode.html) for more
details.
