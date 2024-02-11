---
title: This week in Across - May 5th 2017
date: 2017-05-05
author: The Across Team
toc: true
summary: |
  Changes in Entity Module, Bootstrap UI Module and Web CMS Module.
---

### EntityModule 2.0.0

- Transaction support for default entity views has been added
    - the default `PlatformTransactionManager` is now detected for all
      Spring Data repositories and the bean name added as
      a `EntityConfiguration` attribute: `EntityAttributes.TRANSACTION_MANAGER_NAME`
    - `EntityViewFactoryBuilder` supports configuring transactions for
      state modifying HTTP methods (POST, PUT, PATCH or DELETE) -
      all `doControl()` methods of all processors involved will
      happen in a single transaction
        - configuration can be done by specifying either the
          transaction manager bean name,
          the `PlatformTransactionManager` to use or the
          specific `TransactionTemplate` that should be used
        - if a transaction manager bean name is registered on
          the `EntityConfiguration`, transaction support will be
          enabled for all form views (create, update, delete and
          custom form views)
- If an `OptionIterableBuilder` (select, radio or multi-checkbox)
  returns only a single item and a value for the control is required,
  the single item will be automatically selected
- The default Hibernate Validator *ValidationMessages* properties is
  now included by EntityModule
- Improve the ability to customize view page layouts
    - If a message code is non-empty a page title and optional sub
      title will always be set for every view
    - the `EntityPageStructureRenderedEvent` is published for all view
      types - allowing modifications across multiple views without
      requiring separate `EntityViewProcessors`
- Bug fixes:
    - It is now possible to force a `String` property to generate
      a `TextareaFormElement` even if it has a length/size validator
      that would generate a single-line control

### BootstrapUiModule 1.0.0

- Bug fixes:
    - The HTML id of a generated `SelectFormElement` will now always
      be the same as the control name unless explicitly set
    - The wrapping div of radio or checkbox options control now has a
      HTML id of the form *options-CONTROL\_NAME*

### WebCmsModule 0.0.1

- Implement basic web component infrastructure
    - Ability to render components in Thymeleaf markup but use default
      template markup if no component present
    - Allow creation of web components to be triggered from Thymeleaf
      and be prefilled with Thymeleaf markup
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
    - Container component that represents an ordered collection of
      other components (type: container)
        - Container components can currently only be manages from code
          or YAML - the UI does not yet support adding members
- Add shared components functionality: global components
- Article assets now use web components for their fields
    - This allows templates to be used for different article types and
      applications to customize which fields they want an article to
      have
    - Article template can be configured on `Publication` type
