#!/bin/bash

POM_XML="/home/mvnbuilder/pom.xml"
JAR_DIR="/home/mvnbuilder/target/dependency"

/pom-gen.py > $POM_XML
if [ $? == 0 ]; then
  su mvnbuilder -c "mvn -f $POM_XML clean dependency:copy-dependencies" > /mvn.log

  if [ -d $JAR_DIR ] && [ $(find $JAR_DIR -type f | wc -l) -gt 0 ]; then
      cd $(dirname $JAR_DIR)
      cat /Dockerfile.child | sed s/MAIN/${POM_MAIN}/g > Dockerfile
      tar -cf - *
  fi
fi
