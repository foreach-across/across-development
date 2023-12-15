#!/usr/bin/env bash

set -e

# This makes some assumptions:
# - Tags start with a single letter, which is dropped to make the version. Everybody uses "v" for this.
# - Only tag and branch commits are supported, merge requests are not.

#CI_COMMIT_BRANCH=5.3
CI_COMMIT_TAG=v5.3.0

#if [[ "${CI_COMMIT_TAG}" = "" ]]
#then
#  ARTIFACT_VERSION="${CI_COMMIT_BRANCH}-SNAPSHOT"
#else
#  ARTIFACT_VERSION="$(echo ${CI_COMMIT_TAG} | cut -c2-100)"
#fi

# if [[ "${CI_COMMIT_TAG}" = "" ]]; then ARTIFACT_VERSION="${CI_COMMIT_BRANCH}-SNAPSHOT"; else ARTIFACT_VERSION="$(echo ${CI_COMMIT_TAG} | cut -c2-100)"; fi

ARTIFACT_VERSION=$(if [[ "${CI_COMMIT_TAG}" = "" ]]; then echo "${CI_COMMIT_BRANCH}-SNAPSHOT"; else echo "$(echo ${CI_COMMIT_TAG} | cut -c2-100)"; fi)

echo $ARTIFACT_VERSION
