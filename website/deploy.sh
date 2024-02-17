#!/usr/bin/env bash

set -e

if [[ $# -ne 1 ]]
then
  echo "publish.sh <GIT_COMMENT>"
  exit 1
fi

comment=$1

rm -rf public/*
HUGO_ENV=production hugo
cd public
git restore README.md
git restore google*.html
git add *
git commit -a -m "$comment"
git push
