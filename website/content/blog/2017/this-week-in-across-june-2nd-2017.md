---
title: This week in Across - June 2nd 2017
date: 2017-06-02
author: The Across Team
toc: true
summary: |
  Changes in Across Framework, Bootstrap UI Module, Admin Web Module, Entity Module and Web CMS Module.
---

### Across 2.1.0

- Added `LocalizedTextResolver` to easily localize (eg. translate)
  text snippets
    - The default
      implementation `MessageCodeSupportingLocalizedTextResolver` supports
      special message code snippets, examples:
        - *Some text* will always return *Some text*
        - *\#{my.code}* will return the resolved message code
          or *my.code* if no message found
        - *\#{my.code=Some text}* will return the resolved message
          code or *Some text* if no message found
    - A default singleton bean is exposed and attached to the current
      MessageSource
- `ViewElementBuilderContext` implements
  the `LocalizedTextResolver` interface as well as now having
  several message code related methods
    - This makes it useful to localize texts when creating
      a `ViewElement` inside a `ViewElementBuilder`

### BootstrapUiModule 1.1.0

- `Menu` structures can now also be rendered to panels based markup
  (sidebar as in AdminWebModule) and as breadcrumb
    - `BootstrapUiComponentFactory` provides access to the specific
      builders
    - Builders support filtering of items making it useful to render
      the same Menu in multiple ways (example in
      AdminWebModule: `AdminMenu` and `AdminWebLayoutTemplate`)
    - Builders also support message code snippets for item titles, eg
      you can now put *\#{my.item=My default item title}* as title
- Select box controls now support more advanced bootstrap-select
  controls
    - These can be customised by setting
      a `SelectFormElementConfiguration`

### AdminWebModule 2.1.0

- Improved AdminWeb layout template:
    - slightly improved base styling and nav components
    - fix some styling issues in mobile view
    - support full customisation of all navigational components:  top
      menu (left & right), sidebar and breadcrumb
    - FontAwesome icon set is also added by default
- All dismissible alerts are now rendered as Toastr notifications that
  automatically disappear after a number of seconds

### EntityModule 2.1.0

- improve the ability to customise page titles and layouts
    - all entity views now set a page (sub) title if a matching
      message code returns a non-empty string
    - there is a default title for all views except the list view
    - list views now also publish
      an `EntityPageStructureRenderedEvent`
- all select options are by default rendered as a bootstrap-select
    - a `SelectFormElementConfiguration` attribute on a property
      descriptor will be used as the configuration for a select box
      type property

### WebCmsModule 0.0.2

- Implement basic web component infrastructure
    - Ability to render components in Thymeleaf markup but use default
      template markup if no component present
    - Allow creation of web components to be triggered from Thymeleaf
      and be prefilled with Thymeleaf markup
    - Support placeholder segments defined in the Thymeleaf templates
    - Provide component hierarchy: multiple scopes can be defined (eg:
      global, page...) and components can be searched for bottom-up
        - This allows overriding default components on a per
          page/asset level
    - Basic components can be imported using YAML
    - The `WebCmsComponentModel` also implements `ViewElement` making
      it very easy to mix with other `ViewElement` rendering
      functionality
- Add default components:
    - Image component that allows selecting a `WebCmsImage` asset
      (type: image)
    - Text component that supports plain-text, rich-text or html
      markup (types: plain-text, text-field, rich-text, html)
        - Markup supports content markers for rendering other
          components or placeholders inside the markup
    - Container component that represents an ordered collection of
      other components (type: container)
- Add shared components functionality: global components
- Article assets now use web components for their fields
    - This allows templates to be used for different article types and
      applications to customize which fields they want an article to
      have
    - Article template can be configured on `WebCmsArticleType`
