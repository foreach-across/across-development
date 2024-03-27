#!/usr/bin/env sh

set -e

# WARNING: Do not run this script from the top-level directory,
# since that will cause all revision properties to become the same in all repositories.

if [ $# -ne 1 ]
then
    echo "Expecting exactly one argument: the value for the revision property."
    echo "Note that this script also requires 0 (for across-framework only) or more ACROSS_*_VERSION environment variables."
    exit 1
fi

REVISION=$1

# sed (stream editor) for beginners: s/abc/xyz/g substitutes (s) all "abc" with "xyz" globally (g).
# We don't really need the g flag, but I left it in because it's so common.
# However, instead of the conventional / separator, we use :, because / appears in the closing XML tags.
# Multiple -e options should be supported by the BSD sed on macOS as well.

# Nope: not possible, because you cannot just replace any "<version>whatever</version>"
# TODO use a regular expression, to just replace any version within the tags: it's probably just ".+".
# That way, the script can be used in both directions.

find . -name pom.xml -print0 | xargs -0 sed -i -E \
-e "s:<revision>dev-SNAPSHOT</revision>:<revision>${REVISION}</revision>:g" \
-e "s:<version>dev-SNAPSHOT</version>:<version>${ACROSS_FRAMEWORK_VERSION}</version>:g" \
-e "s:<across-framework.version>dev-SNAPSHOT</across-framework.version>:<across-framework.version>${ACROSS_FRAMEWORK_VERSION}</across-framework.version>:g" \
-e "s:<across-autoconfigure.version>dev-SNAPSHOT</across-autoconfigure.version>:<across-autoconfigure.version>${ACROSS_AUTOCONFIGURE_VERSION}</across-autoconfigure.version>:g" \
-e "s:<across-base-modules.version>dev-SNAPSHOT</across-base-modules.version>:<across-base-modules.version>${ACROSS_BASE_MODULES_VERSION}</across-base-modules.version>:g" \
-e "s:<across-entity-admin-modules.version>dev-SNAPSHOT</across-entity-admin-modules.version>:<across-entity-admin-modules.version>${ACROSS_ENTITY_ADMIN_MODULES_VERSION}</across-entity-admin-modules.version>:g" \
-e "s:<across-user-auth-modules.version>dev-SNAPSHOT</across-user-auth-modules.version>:<across-user-auth-modules.version>${ACROSS_USER_AUTH_MODULES_VERSION}</across-user-auth-modules.version>:g" \
-e "s:<across-media-modules.version>dev-SNAPSHOT</across-media-modules.version>:<across-media-modules.version>${ACROSS_MEDIA_MODULES_VERSION}</across-media-modules.version>:g"
