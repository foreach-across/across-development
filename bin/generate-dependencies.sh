#!/usr/bin/env bash

set -e

# Run this script whenever you make changes to the maven build scripts.

# The dependency.tree.txt file shows where a (transitive) dependency came from.
# That tree often changes very dramatically, even when making a small adjustment.
# To be able to easily see only the version changes, we also keep an alphabetically
# sorted dependency.list.txt file.
# We keep both files under version control, so it's easy to compare them
# when doing upgrades (Across, Spring, ...)

PLUGIN_VERSION=3.6.1

# Ascii-based sorting, using the traditional C locale; otherwise sorting will be dependant on the user's locale:
export LC_ALL=C
unset LANG

mvn org.apache.maven.plugins:maven-dependency-plugin:${PLUGIN_VERSION}:tree -DoutputFile=dependency.tree.txt

mvn org.apache.maven.plugins:maven-dependency-plugin:${PLUGIN_VERSION}:list -DoutputFile=dependency-tmp.list.txt
# shellcheck disable=SC2044
for dep_file in $(find . -name dependency-tmp.list.txt)
do
  dir=$(dirname "$dep_file")
  grep -v "The following files have been resolved:" "$dep_file" | cut -d' ' -f 4 | cut -d $'\033' -f 1 | grep -v "^[[:space:]]*$" | sort | uniq > "$dir"/dependency.list.txt
  rm "$dep_file"
done

find . -name dependency.list.txt -print0 | xargs -0 cat | egrep -v ':tests:|io.netty:netty-tcnative-boringssl-static' | cut -d: -f1,2,4 | sort | uniq > uniq_deps_with_version.txt
find . -name dependency.list.txt -print0 | xargs -0 cat | egrep -v ':tests:|io.netty:netty-tcnative-boringssl-static' | cut -d: -f1,2 | sort | uniq > uniq_deps_without_version.txt

uniq_deps_with_version=$(wc -l uniq_deps_with_version.txt | cut -d' ' -f 1)
uniq_deps_without_version=$(wc -l uniq_deps_without_version.txt | cut -d' ' -f 1)

diff=$((uniq_deps_with_version - uniq_deps_without_version))

#exit 0

# This may be inevitable with bamboo-specs !
# if [[ $uniq_deps_with_version != $uniq_deps_without_version ]]
if [[ $diff != 0 ]]
then
  echo
  echo "ERROR: There are ${diff} dependencies with multiple versions:"
  # echo "Check the uniq_deps_with_version.txt file!"
  cut -d: -f1,2 uniq_deps_with_version.txt | uniq -c | grep -v "      1 "
  # echo
  exit 1
fi

rm uniq_deps_with_version.txt
rm uniq_deps_without_version.txt

echo ""
echo "Successfully generated:"
find . -name "dependency.*.txt" | sort

echo ""
git status
