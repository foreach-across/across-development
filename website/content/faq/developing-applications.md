---
title: Developing Across applications
weight: 3
toc: true
---

### What is the meaning of the project structure created by Across Initializr?

> Update 2024-02-11: Across Initializr is no longer available.

[Across Initializr](http://start-across.foreach.be) generates a typical
project structure for an Across application. Which structure gets
created exactly depends on the options you checked when generating the
project.

It will create both a Java package structure and a structure for the
embedded resources. At first glance some part of it might seem bloated
(especially the resources). The main reason for this is that Across
really likes your code to be bundled inside a module and uses module
specific paths for both its packages and resource locations. As such,
the unique module resources key will always be part of a resource path.
This ensures that there are no resource location conflicts between
modules, as many modules embed (the same type of) resources.

In addition, the default resource locations are setup in such a way that
they enable development mode (automatic resource reloading) and static
resource versioning.

#### Related questions

To get a better idea of the purpose of this structure, please see the
following questions:

-   [What is an Across context?](what-is-an-across-context.html)
-   [What is a good project structure for an Across
    module?](what-is-a-good-project-structure-for-an-across-module.html)
-   [How is the Across application different from the Across application
    module?](how-is-the-across-application-different-from-the-across-application-module.html)
-   [What is "development mode"?](what-is-development-mode.html)


### Do I need a RDBMS for building an Across application?

Although a RDBMS is not strictly required by Across Framework, you will
need one if you are going to use installers. The RDBMS is necessary for
Across to be able to track the the installer state between application
starts.

Across itself creates only a minimal set of tables and will do so only
when required, that is when installers need executing.

See the [reference documentation section on
Installers](../reference-docs%3Fsection=installers.html) for more
details.


### What are the dynamic/application modules?

See the question [How is the Across application different from the
Across application
module?](how-is-the-across-application-different-from-the-across-application-module.html)


### How is the Across application different from the Across application module?

To understand the answer to this question, it is important you first
understand the answer to the question [What is an Across
context?](what-is-an-across-context.html)

The **Across application** is the combination of all modules configured
in your application. The **Across application module** is a single
module in your application, it is the one containing your application
specific logic. The application module is always considered to depend on
all other “shared” modules, and as such is started as the last module
(with the exception of possible specialized postprocessor modules).

Shared modules have an explicit module descriptor, whereas the
application module has an implicit one that is derived from the name and
package of the `@AcrossApplication` annotated class. The application
module is determined using a convention-over-configuration approach. The
content of the application module is all content present in the
`application` package that is a child of the package holding the
`@AcrossApplication` class. The key for resources of this module will be
derived from the `@AcrossApplication` class name.

An example:

-   your `@AcrossApplication` class is `com.foo.MyApplication`
-   your application module would be named `MyApplicationModule`
-   the module configuration would be all components scanned from the
    child packages of `com.foo.application`
-   The resources key of your application module would be `my`

An application module will only be created if there is a package named
`application`. You can have an Across application built using only
shared modules.

The `@AcrossApplication` class is part of the root
Spring `ApplicationContext`. That class should typically only contain
application setup and configuration code. Anything declared in that
`ApplicationContext` will be available to all modules. The other way
around - accessing module components on the `@AcrossApplication` level
directly - should be avoided.

Across prefers all business logic to be packaged in modules. Having your
application-specific logic bundled inside an application module allows
you to use any of the exposed beans from other modules, as the bootstrap
order can be guaranteed. Conditions on the existence of components will
work as expected and it also makes it easier to convert the application
module to a shared module at any point in time (by simply providing a
module descriptor).


### Where can I find the documentation for module X?

Links to the available documentation are present on the [module detail
page](../modules.html).

Documentation is an ongoing effort for every team responsible, so
contributions are very welcome. See our [contributor
guidelines](../contributing.html) if you have an interest in
contributing.


### Where can I report issues or request features?

Most modules have their own issue tracker that is listed on the [module
detail page](../modules.html).  
Please see the question [How can i get in
touch?](i-have-a-question-how-can-i-get-in-touch.html) for more
information.


### How can I handle events published by other modules?

Across uses its own event bus for publishing events. Any module can
define multiple event handlers. An event handler is a single parameter
method:

-   The parameter type implements `AcrossEvent` and defines the type of
    event the method handles.
-   The method is annotated with `@Event`, indicating it is an event
    handler.

All created components will automatically be scanned for event handler
methods.

See the [reference documentation section on
Events](../reference-docs%3Fsection=events.html) for more details.
