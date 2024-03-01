---
weight: 605
title: Web Content Management

repo-id: across-media-modules
module-name: WebCmsModule
---

`WebCmsModule` provides some basic web content management features for
your Across application.

<!--more-->

Out-of-the-box it provides the following features:

- an extensible [domain
  model](https://foreach-across.github.io/ref-docs-5/web-cms-module/domain-model/assets/index.html)
  with common asset types like
  [pages](https://foreach-across.github.io/ref-docs-5/web-cms-module/domain-model/pages/index.html),
  [articles](https://foreach-across.github.io/ref-docs-5/web-cms-module/domain-model/publication/index.html#_webcmsarticle)
  and
  [redirects](https://foreach-across.github.io/ref-docs-5/web-cms-module/domain-model/redirects/index.html)

- a way to manage the [URLs for these
  assets](https://foreach-across.github.io/ref-docs-5/web-cms-module/domain-model/publication/index.html)

- a [powerful
  model](https://foreach-across.github.io/ref-docs-5/web-cms-module/components/index.html)
  for building templates and managing dynamic content

- an easy way to [import data using YAML
  files](https://foreach-across.github.io/ref-docs-5/web-cms-module/importing/yaml-structure.html)

A fully functional administration UI is available using [Admin
Web]({{< relref "admin-web-module.md" >}}) and [EntityModule]({{<
relref "entity-module.md" >}}).


### Artifacts

The Web CMS dependency is present in Across Platform.

    <dependency>
         <groupId>com.foreach.across.modules</groupId>
         <artifactId>web-cms-module</artifactId>
    </dependency>
