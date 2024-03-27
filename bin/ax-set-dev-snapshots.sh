#!/usr/bin/env sh

set -e

# WARNING: Do not run this script from the top-level directory,
# since that will cause all revision properties to become the same in all repositories.

# sed (stream editor) for beginners: s/abc/xyz/g substitutes (s) all "abc" with "xyz" globally (g).
# We don't really need the g flag, but I left it in because it's so common.
# However, instead of the conventional / separator, we use :, because / appears in the closing XML tags.
# Multiple -e options should be supported by the BSD sed on macOS as well.

# Nope: not possible, because you cannot just replace any "<version>whatever</version>"
# TODO use a regular expression, to just replace any version within the tags: it's probably just ".+".
# That way, the script can be used in both directions.

find . -name pom.xml -print0 | xargs -0 sed -i -E \
-e "s:<revision>.+</revision>:<revision>dev-SNAPSHOT</revision>:g" \
-e "s:<across-framework.version>.+</across-framework.version>:<across-framework.version>dev-SNAPSHOT</across-framework.version>:g" \
-e "s:<across-autoconfigure.version>.+</across-autoconfigure.version>:<across-autoconfigure.version>dev-SNAPSHOT</across-autoconfigure.version>:g" \
-e "s:<across-base-modules.version>.+</across-base-modules.version>:<across-base-modules.version>dev-SNAPSHOT</across-base-modules.version>:g" \
-e "s:<across-entity-admin-modules.version>.+</across-entity-admin-modules.version>:<across-entity-admin-modules.version>dev-SNAPSHOT</across-entity-admin-modules.version>:g" \
-e "s:<across-user-auth-modules.version>.+</across-user-auth-modules.version>:<across-user-auth-modules.version>dev-SNAPSHOT</across-user-auth-modules.version>:g" \
-e "s:<across-media-modules.version>.+</across-media-modules.version>:<across-media-modules.version>dev-SNAPSHOT</across-media-modules.version>:g"

#-e "s:<version>.+</version>:<version>${ACROSS_FRAMEWORK_VERSION}</version>:g" \

echo "You will still need to manually set the parent version to dev-SNAPSHOT."
