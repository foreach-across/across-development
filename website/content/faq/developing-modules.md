---
title: Developing Across modules
weight: 4
toc: true
---

### How can I create a module to share between multiple projects?

Declaring a module only requires you to define a valid module
descriptor. To be able to share it across multiple projects, simply move
all components and the descriptor to a shared JAR. A module usually
corresponds to a single JAR, but this is not a requirement.

See the [reference documentation section on Development Across
modules](../reference-docs-section-developing-across-modules.html) for
general information on developing modules.  
See also the question [What is a good project structure for an Across
module?](what-is-a-good-project-structure-for-an-across-module.html) for
some best practices.


### What is a good project structure for an Across module?

A module should never conflict with another module. As such, there are
some best practices for creating a module:

-   Put every module in its own discrete package; avoid package overlap
    with other modules.
-   Define `@AcrossDepends` dependencies to other modules you require.
-   Avoid cyclic dependencies on other modules.
-   Avoid cyclic package dependencies with other modules (this is where
    putting them in separate JARs can help, as boundaries become
    explicit).
-   Avoid relying on the ordering of modules you do not have a required
    dependency on.
-   Always rely on ordering of modules you have required dependencies
    on: these will be started before your own module.
-   Define a unique module name and a unique resources key; avoid
    resource overlap with other modules.
-   Put all your module resources in a location mapped with the
    resources key.

#### An example

-   `MyModule` module descriptor would be in package
    `com.foo.modules.my`**.**
-   All components would be in either `com.foo.modules.my` or a child
    package.
-   The basic configuration classes would be in
    `com.foo.modules.my.config`.
-   If the resources key of the module would be `my`, then all embedded
    resources would be in a location containing that key, for example:
    -   `/messages/my/default.properties` (message code)
    -   `/installers/my` (installer files)
    -   `/views`
        -   `/static/my` (static resources)  
            -   `/css`
            -   `/js`
        -   `/th/my` (Thymeleaf templates)


### Can I access components from other modules that are not exposed?

Yes, though it’s usually better to expose them. See also the question
[Can I manually expose existing beans from another
module](can-i-manually-expose-existing-beans-from-another-module.html).

There are two ways to manually retrieve non-exposed components from
other modules:

-   `@RefreshableCollection` has an attribute to specify whether the
    collection should contain all beans of that type, regardless of the
    fact if they are exposed or not.
-   The `AcrossContextBeanRegistry` component allows you to access any
    module `ApplicationContext`, and to interact with their components.


### How can I test my shared module?

There is a separate artifact called **across-test** that contains
several utility classes for integration testing your module.  
See the [reference documentation on
Testing](../reference-docs-section-across-test.html) for more details.


### Can my module extend another module's configuration?

Yes.

There are 3 ways a module can change the configuration of another module
before it gets started:

1.  Your module can provide a `@ModuleConfiguration` class in its
    extension packages. A `@ModuleConfiguration` is like a regular
    `@Configuration` which will be added to the target module instead of
    the module that declares it.  See the [reference documentation on
    `@ModuleConfiguration`](../reference-docs-section-moduleconfiguration.html)
    for more information.
2.  Your module descriptor can implement the `prepareForBootstrap()`
    method, which also allows registering additional configuration
    classes on other modules.
3.  Your module can subscribe to the `AcrossModuleBeforeBootstrapEvent`
    and modify the module configuration at that point. Please note this
    requires your own module to have been started. You will only receive
    this event for modules that start after your own.

An example of the practical use of module configuration extensions can
be found in the
[AcrossHibernateJpaModule](../modules/acrosshibernatemodule.html).
Additional entities to scan are defined through module extensions.


### How can I retrieve all beans of a certain type, even the ones created after my own module has started?

You can annotate a `Collection<>` property with
`@RefreshableCollection`. This will update the collection of members
after the entire context has bootstrapped. All exposed beans matching
the member type will be added.

Alternatively you can use the `AcrossContextBeanRegistry` component to
retrieve beans from an Across context at any point in time.


### Can my module replace components from another module?

Yes, see the the question [Can my module extend another modules’
configuration?](can-my-module-extend-another-module-s-configuration.html)
for more details.


### Can I manually expose existing beans from another module?

Yes. You can do so by customizing the configuration of the target module
that holds the bean.

There are several ways to do this:

1.  By subscribing to the `AcrossModuleBeforeBootstrapEvent` in any
    module that has already started. This event will be published before
    your target module starts and allows you to customize the module
    configuration, which includes adding exposed bean types.
2.  By implementing the `prepareForBootstrap()` method on your own
    module descriptor and changing the configuration of the target
    module.
3.  By adding the target module manually as a bean to your application,
    instead of scanning by name or adding it transitively. Defining the
    module as a bean creates an instance of `AcrossModule`, which allows
    modifying the expose filter.

Exposing additional beans from other modules can be somewhat circuitous.
We hope to improve this in future releases of Across.


### Can I put more than one module in the same jar?

Absolutely.

Across poses no actual restrictions on how to package your module. We do
advocate a default project structure to help you avoid common problems.
See the question [What is a good project structure for an Across
module?](what-is-a-good-project-structure-for-an-across-module.html) for
more information.
