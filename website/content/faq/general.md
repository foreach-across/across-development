---
title: General
weight: 1
toc: true
---

### Is Across free to use?

Yes. Across Framework as well as all modules built by the same team are
published under the [Apache 2.0
license](https://www.apache.org/licenses/LICENSE-2.0.html). The source
code can be found on the [Foreach
Bitbucket](https://bitbucket.org/beforeach/) space.


### What experience do I need to get started with Across?

You need a good grasp of Java (8) and [Spring
Framework](https://projects.spring.io/spring-framework/). [Spring MVC
experience](https://docs.spring.io/spring/docs/4.3.x/spring-framework-reference/html/mvc.html)
is strongly advised, and some Spring Boot knowledge might be helpful.

At the very least you should be familiar with Spring’s approach for
dependency injection, the `ApplicationContext` and java-based
configuration.

Other commonly used libraries that are useful to know are
[Hibernate](http://hibernate.org/orm/), [Spring
Data](http://projects.spring.io/spring-data/),
[Liquibase](http://www.liquibase.org/) and
[Thymeleaf](http://www.thymeleaf.org).


### What are the dependencies of Across?

At its heart, Across only requires [Spring
Framework](https://projects.spring.io/spring-framework/)and [Spring
Boot](https://projects.spring.io/spring-boot/)for running applications.
However, most of the provided functionality is aimed at web
applications, so Spring MVC usually comes into play as well. When
playing on the web, default modules setup
[Thymeleaf](http://www.thymeleaf.org) for server-side templating.

When using installers (which is a pretty common thing), a minimal RDBMS
is required as well and Liquibase will be used for the default schema.
All standard Across modules that require a RDBMS are tested on H2,
HSQLDB, MySQL, Oracle, and MS SQL.

All third-party libraries used by Across are free, open source and
backed by a large community.

#### Dependency versions

<table>
<thead>
<tr class="header">
<th style="text-align: center;">Across Platform</th>
<th style="text-align: center;">Spring Framework</th>
<th style="text-align: center;">Spring Boot</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: center;">2.1.x</td>
<td style="text-align: center;">4.3.x</td>
<td style="text-align: center;">1.5.x</td>
</tr>
<tr class="even">
<td style="text-align: center;">2.0.x</td>
<td style="text-align: center;">4.3x</td>
<td style="text-align: center;">1.4.x</td>
</tr>
</tbody>
</table>


### Which versions of Java and Spring is Across compatible with?

The latest version of Across Platform (2.1.x) is compatible with Java 8,
Spring Framework 4.3.x and Spring Boot 1.5.x.

See the [dependency table](what-are-the-dependencies-of-across.html) for
an overview of the current dependencies.


### What is the difference between Across Framework and Across Platform?

Across Framework is an actual Java library providing all the
infrastructure necessary to build Across modules and to run applications
based on them.

[Across Platform](../modules.html) is a set of curated dependencies and
Across modules that play well together and help developers assemble
applications. It is provided as a bill-of-material POM, extending the
[Spring IO platform BOM](http://platform.spring.io/platform/).

Across applications usually use the Across Platform BOM as a basis, to
ensure that both third-party libraries as well as common Across modules
are compatible.


### Can I use Across without the standard modules?

Absolutely. We advise you to use the [Across Platform
BOM](../modules.html) for dependency management, but there is no
requirement to actually use any of the standard modules.


### Can I use Across for a non-web application?

Yes. The core framework for bootstrapping a module based application
does not require a web context. Be aware, however, that most of Across’
features and modules are web dependent, so you will not be able to use
those.


### I'd like to contribute. Is that possible?

Absolutely! Across is open source and anyone can fork the repositories
on [Bitbucket](https://bitbucket.org/beforeach). Please read our
[contributor guidelines](../contributing.html) if you are serious about
making contributions.

If you’d like to contribute by sharing knowledge there’s also several
ways to do so:

-   Write blogs, tutorials and quick starts; we will gladly reference
    them on the Across website.
-   Answer questions of fellow developers on [Stack
    Overflow](https://stackoverflow.com/), or comment on issues in the
    issue trackers.
-   Contribute to the [documentation](../documentation.html) of the
    respective modules.


### I have a question. How can I get in touch?

The team actively monitors [Stack Overflow](https://stackoverflow.com/),
so we prefer you post technical questions there using the tag
**\#across**.

More general questions or feature requests can be filed in the issue
tracker as a **Question issue type**. The issue tracker is also the tool
used for filing bug reports. You can find the issue tracker of a
specific module on the [module detail page](../modules.html).

There is also a Gitter channel where most of the core developers reside:
[https://gitter.im/thinking-across](https://gitter.im/thinking-across/Lobby).

If you are looking for professional support, please see our [support
page](../support.html).


### What do you mean with "modular web applications"?

There are many ways to modularize a web application. In our case we’re
talking about an application made up of several Across modules. Across
modules can be both technical modules (like a module setting up
Hibernate or Ehcache) and functional modules (like a module providing a
domain model for working with orders).

An application is a combination of different modules put together.
Modules can depend on other modules, but only ever in one direction (no
cyclic dependencies).

Technical modules as described above are very common in the Java/Spring
landscape, Across, however, aims to stimulate the creation of more
functional modules. Although Across can be used perfectly well in a
microservice landscape, its greatest value possibly lies in helping
developers create “modular monoliths”, aka monolithic applications done
in a better way.

Some background on the idea of modularizing monoliths:

- Simon Brown on Modular Monoliths

  - <http://www.codingthearchitecture.com/presentations/sa2015-modular-monoliths>
  - <https://www.youtube.com/watch?v=kbKxmEeuvc4>

- Oliver Gierke on Refactoring to a System of Systems

  - <https://speakerdeck.com/olivergierke/refactoring-to-a-system-of-systems>


### Can I use Across for microservices?

Yes, you can, but please be aware that Across is actually better suited
for developing modular monoliths and does not necessarily bring much
added value for small applications often representing a single module.

The [Spring Boot](https://projects.spring.io/spring-boot/) and [Spring
Cloud](http://projects.spring.io/spring-cloud/) communities are very
active when it comes to microservices and most of their features have
not yet been tested in Across based applications. It might involve some
more in-depth technical work to get things working correctly. We can
offer commercial support for this if required.

In future releases of Across we expect to improve the out-of-the-box
integration with Spring Boot and Spring Cloud libraries.


### Can I add my own module to your list?

Absolutely.

If you've created your own shared Across module and would like to have
it listed on the [modules page](../modules.html), just [let us
know](../documentation.html#get-in-touch).
