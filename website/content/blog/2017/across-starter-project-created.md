---
title: Across starter project created
date: 2017-03-23
author: The Across Team
toc: true
---

> Update 2024-02-11: Across Initializr is no longer available.

We've created a starter project template for Across applications. This
should help you quickly setup new projects with the most common basic
options.

You can find the starter
at <https://bitbucket.org/beforeach/across-starter>.

<!--more-->


## How to use

Just clone the repository, import the maven pom.xml in you favourite IDE
and then go change the module/class/file names to the ones you want.
The README.MD file included should tell you what you need to know.

You can just run the sample application using the **dev** profile. From
command-line you can do `mvn exec:java` in the *my-application* folder.

## Contents

The starter application sets up a basic web application with the
following contents:

- Base structure for a maven multi-module project
- Spring Boot application with devtools active: auto restart and live
  reloading enabled out of the box when started with dev profile
- application configuration
  in *application.yml* and *application-dev.yml*
- Using a H2 database with /h2-console enabled in dev
- Sample homepage with a controller, thymeleaf view and including some
  static resources
- Sample `Page` entity as auditable entity with a corresponding Spring
  data repository
- Installers for the base schema and adding the auditable columns to
  the my\_page table
- AdminWebModule (/admin) and a custom admin controller
- UserModule for user domain and default user for securing the admin
  section
- DebugWebModule (/debug) section - secured by basic auth configured
  in the application properties
- Lombok and QueryDSL support

## Possible improvements

Feel free to hop in to add any of these to the sample project, just
launch a PR to master branch.

- Add script for configuration of your project (replace all starter
  names automagically based on some Q\&A)
- Add a sensible default logging configuration
- Add sample debug controller
- Add gulp based generation of frontend resources
- Add asciidoc generation and in-app deploy
- Add a sample data installer
- Add sample QueryDSL query to the homepage - listing all pages
  (illustrate that QueryDSL is active)
- Add customization to the entity views of Page entity
