---
weight: 603
title: Image Server Module
aliases:
  - imageserver
  - imageserver-client

repo-id: across-media-modules
module-name: ImageServerCoreModule
---

`ImageServerCoreModule` provides functionality for serving images in
different resolutions. It can be used as an alternative to an actual
Image CDN like [Cloudinary](https://cloudinary.com/) when you need to
have the functionality inside your app (or local network).

<!--more-->

Apart from a server-side setup for actually serving and storing the
images, you will need to have a graphics library installed. A separate
client library is also provided for easy connecting to the ImageServer
from external applications.


### Artifacts

The ImageServer dependency is present in Across Platform.

    <!-- Core ImageServer -->
    <dependency>
      <groupId>com.foreach.across.modules</groupId>
      <artifactId>imageserver-core</artifactId>
    </dependency>

    <!-- Client library for external applications connecting to imageserver -->
    <dependency>
      <groupId>com.foreach.across.modules</groupId>
      <artifactId>imageserver-client</artifactId>
    </dependency>


### How it works

The basic principle of ImageServer is that original images are
uploaded to ImageServer and should never be removed. Variations of
that image - for example a crop or resize - are stored for performance
but can be removed as they will simply be recreated upon the next
request.


### Available features

ImageServer does not come close in available features to something
like a real Image CDN. But it does allow you to define image crops and
perform simple image transformations. It tries to be as performant as
possible. You can always throw away variant images, just don't throw
away the original.


### Integration with other modules

[WebCmsModule]({{< relref "web-cms-module.md" >}}) has configuration
options to automatically connect to an ImageServer as an alternative
to Cloudinary.


### Technical requirements

ImageServer requires either:

- [ImageMagick](https://www.imagemagick.org/script/index.php) or

- [GraphicsMagick](http://www.graphicsmagick.org/)

to be present on the system. The location of the binaries can be
configured using the [module
settings](https://repository.antwerpen.io-external.com/projects/image-server/4.0.0.RELEASE/reference/#_module_settings).
