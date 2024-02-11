---
weight: 102
title: Across Web

repo-id: across-framework
module-name: AcrossWebModule
---

`AcrossWebModule` is a basic building block of pretty much every Across
application.

It activates Spring MVC support for all modules in the Across context.
This means modules can configure Spring MVC features, adding things like
controllers, servlets and filters.

On top of regular Spring MVC components, `AcrossWebModule` adds the
following out of the box:

- Thymeleaf template rendering with a custom [Thymeleaf
  dialect](https://docs.across.dev/across-site/production/across/across-web/thymeleaf-dialect.html)
  for interacting with the Across web infrastructure

- infrastructure for
  [templates](https://docs.across.dev/across-site/production/across/across-web/web-views/layout-templates.html),
  [menu
  building](https://docs.across.dev/across-site/production/across/across-web/web-views/working-with-menus.html)
  and [registering web
  resources](https://docs.across.dev/across-site/production/across/across-web/web-views/web-resources.html)

- a [programmatic model for creating UI
  components](https://docs.across.dev/across-site/production/across/across-web/web-views/view-elements.html)
  from code

- support for [prefixing request mappings and adding custom request
  condition](https://docs.across.dev/across-site/production/across/across-web/basic-features/custom-request-mapping-support.html) -
  extending default `@RequestMapping` behaviour

- auto configuration of static resources with [client-side
  caching](https://docs.across.dev/across-site/production/across/across-web/configuration/resource-versioning.html#client-side-caching)
  and [url
  versioning](https://docs.across.dev/across-site/production/across/across-web/configuration/resource-versioning.html#resource-url-versioning)


### Artifacts

The Across Web dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across</groupId>
         <artifactId>across-web</artifactId>
    </dependency>
