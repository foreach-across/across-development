#!/usr/bin/env bash

set -e

for jar in `ls *.jar`
do
    name=`basename --suffix=.jar $jar`
    echo $name
    mkdir -p $name
    cd $name
    jar xf ../$jar
    cd -
done
