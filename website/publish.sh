#!/usr/bin/env bash

set -e

if [[ $# -ne 1 ]]
then
  echo "publish.sh <GIT_COMMENT>"
  exit 1
fi

comment=$1

rm -rf public/*
hugo
cd public
git restore README.md
git commit -a -m "$comment"
git push
