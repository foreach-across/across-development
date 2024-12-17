---
title: Troubleshooting
weight: 5
toc: true
---

### I try to wire a bean in my application, but while I know it gets created, I still get an exception.

This is perhaps the most common problem when working with Across
modules. It usually has one of the following causes:

#### The bean gets created in another module and is not exposed.

The most likely fix here is to expose that bean. See the question [Can I
manually expose existing beans from another
module?](can-i-manually-expose-existing-beans-from-another-module.html)
for more information.

#### The module that creates the bean is bootstrapped after the one that tries to access it.

This usually indicates that the module does not define its dependencies
on other modules correctly.

In some cases a cyclic dependency can occur when changing dependencies.
To prevent this, you can use `@PostRefresh` to retrieve the bean after
the context has bootstrapped.


### My modules are bootstrapped in the wrong order.

The order in which modules are started is determined by the dependencies
they have on each other. If module B depends on module A, then module A
will be started before module B. If modules are started in the wrong
order, this means their dependencies are not clearly defined.

There is a difference between a required and an optional dependency,
however. If a dependency is required, the order is guaranteed and the
application will not start if any form of cyclic dependency occurs. If a
dependency is optional, the order is not guaranteed and cyclic
dependencies are technically possible (but should still be avoided).

As a last resort you can define runtime dependencies on your module.
This can only be done by declaring your module as a bean and setting the
runtime dependencies property.


### I added my module to @AcrossApplication, but it is not being picked up.

By default the `@AcrossApplication` scans certain packages to look for
modules by name. If you add a custom module by name to the application
annotation, you will need to specify the additional package in which to
scan for it. You can so using either the **modulePackages** or
**modulePackageClasses** attribute.


### I would like to retrieve a component from a module that is bootstrapped later.

There's a couple of ways you can do this:

-   Spring mechanisms to retrieve the actual bean instance upon first
    use:
    -   demarcate your property as `@Lazy` so a lazy-initialization
        proxy gets wired instead
    -   use an `ObjectProvider` instance instead of your bean type and
        retrieve the instance manually
-   You can use `@PostRefresh` to ensure a single bean gets set after
    the context has bootstrapped. You can use a `@RefreshableCollection`
    to wire a collection of beans that automatically gets refreshed.

See the [reference documentation on
Refreshing](../reference-docs-section-refreshing.html) for more
information.


### I added a Spring Boot starter to my project, but it's not added to the application.

The current version of Across does not support all Spring Boot
starters.

Because a default Spring Boot application and an Across application are
fundamentally different in setup, the configuration might not work out
of the box. Increasing compatibility with auto-configuration is a major
point for future releases of Across.

See the separate [across-autoconfigure
documentation](../across-autoconfigure-docs.html) for details on which
starters are currently supported and how you can make others compatible.

### Related questions

- [How is Across different from Spring
  Boot?](../spring-boot-compatibility#how-is-across-different-from-spring-boot)
