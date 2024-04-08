#!/usr/bin/env bash

# For example:
# ax-exec.sh git status
# ax-exec.sh git diff
# ax-exec.sh git diff HEAD
# ax-exec.sh ls -ltr
# ax-exec.sh mciwt

set -e

repos=$(ax-list.py repositories)

for repo in ${repos}; do
  cd "${repo}"
  echo
  echo "---------------------------------------------"
  echo
  pwd
  echo
  "$@"
  cd - >/dev/null
done
