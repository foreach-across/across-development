---
title: New and improved documentation site
date: 2018-07-23
author: The Across Team
toc: true
---

In the past couple of months we've been very actively migrating the
available documentation to a new setup. Today is an important milestone
as we've integrated the new [documentation site](../documentation.html)
in the Across website. All available documentation for every standard
module can now easily be accessed from the single new section.

### Some background

Both the core projects and all standard modules have always had their
own documentation repository. Documentation itself was usually written
in Asciidoc and then generated as a separate HTML document, deployed on
a static webserver.

We found the flexibility of regular Asciidoc files to sometimes be a bit
limited when it came to presenting on - or as - a website. Cross-linking
between documents was not very easy, a feature like *Edit this page* was
hard to come by and styling across the different documentation
repositories required repeated work in every repository separately.

We had experimented with Gitbook for some modules as well, but the
Asciidoc support appeared to be sub-par and after a couple of months we
decided to drop Gitbook and revert back to regular Asciidoc generation.
It proved to be more stable and less of a hassle.

### In comes Antora...

Not that long ago the first version of [Antora](https://antora.org) was
released. Antora is a documentation site generator that:

- supports multiple, separate repositories as documentation sources
- works on top of Git and uses branches/tags for documentation
  versions
- is 100% focused on Asciidoc
- adds features like cross-linking between documents and generating a
  navigation section
- allows you to separate documentation content from the UI, where the
  latter can also easily be customized

Antora fit our needs perfectly and came at exactly the right time, so we
decided to migrate almost immediately. And today we move from
development to production with our documentation site.

### The advantages

You can see the result on the [site documentation
section](../documentation.html). Using our new setup brings several
advantages (both in front and behind the scenes):

- We still manage the documentation for different projects in separate
  Git repositories. Content is still written in Asciidoc.
- A custom-built UI that seamlessly integrates our documentation with
  the rest of the website.
- Several navigation sections allowing for more advanced structuring:
    - the bottom-left documentation set selector for switching between
      modules or projects
    - the left-hand tree navigation to navigate within a single
      documentation set
    - the table of contents on the right-hand side for navigating in a
      single document
- Full-text search across all available documentation. Not so much a
  feature of Antora itself but easily integrated in the UI. This is
  done with [Algolia](https://www.algolia.com/) on a community
  license.
- Support for multiple versions of a document in the UI. Currenly not
  visible but relevant for future releases where we can still keep
  separate versions of the documentation, linked to for example the
  corresponding module version.
- An *Edit this page* function on every page that will bring you
  straight to the correct file on Github, allowing anyone to launch a
  pull-request almost instantly from his or her browser.

Even though we already integrate over 20 documentation repositories, the
entire site generation is still only a matter of seconds.

If you are interested in our setup, you can check out our main
[documentation site
repository](https://github.com/ForeachOS/ax-docs-across-site) which
holds the main Antora configuration.

### Work in progress

Our documentation still remains a big work in progress. We currently
only migrated all existing documentation to the new format.

Some additional documentation has also been added over the past weeks,
but it was mostly a form and not a content migration. As such some
modules are still quite lacking in documentation, and you may encounter
broken links in several spots.

Revising and updating the documentation is a big task that will take us
several months at least. But we're confident that our current setup with
Antora is the right one, and it will help us in developing the docs, as
well as our users in using them and finding the information they are
looking for.
