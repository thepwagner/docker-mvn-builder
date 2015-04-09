#!/usr/bin/env python

import os
from lxml import etree

POM_NAMESPACE = 'http://maven.apache.org/POM/4.0.0'
POM_PREFIX = '{%s}' % POM_NAMESPACE

pom_root = etree.Element('%sproject' % POM_PREFIX, nsmap={None: POM_NAMESPACE})

etree.SubElement(pom_root, 'modelVersion').text = '4.0.0'
etree.SubElement(pom_root, 'groupId').text = 'com.github.thepwagner.docker'
etree.SubElement(pom_root, 'artifactId').text = 'docker-deps-project'
etree.SubElement(pom_root, 'version').text = '0.0.1-SNAPSHOT'

if 'POM_DEPS' in os.environ and os.environ['POM_DEPS']:
    deps = os.environ['POM_DEPS']
    dependencies = etree.SubElement(pom_root, 'dependencies')
    for dep in deps.split(','):
        group_id, artifact_id, version_classifier = dep.split(':')
        dependency = etree.SubElement(dependencies, 'dependency')

        etree.SubElement(dependency, 'groupId').text = group_id
        etree.SubElement(dependency, 'artifactId').text = artifact_id
        if '@' in version_classifier:
            version, classifier = version_classifier.split('@')
            etree.SubElement(dependency, 'version').text = version
            etree.SubElement(dependency, 'classifier').text = version_classifier
        else:
            etree.SubElement(dependency, 'version').text = version_classifier

build = etree.SubElement(pom_root, 'build')
build_plugins = etree.SubElement(build, 'plugins')


def add_build_plugin(group_id, artifact_id, version, config={}):
    plugin = etree.SubElement(build_plugins, 'plugin')
    etree.SubElement(plugin, 'groupId').text = group_id
    etree.SubElement(plugin, 'artifactId').text = artifact_id
    etree.SubElement(plugin, 'version').text = version
    if config:
        configuration = etree.SubElement(plugin, 'configuration')
        for k, v in config.items():
            etree.SubElement(configuration, k).text = v


add_build_plugin('org.apache.maven.plugins', 'maven-dependency-plugin', '2.8', config={
    'excludeTransitive': 'false'
})

build_extensions = etree.SubElement(build, 'extensions')


def add_build_extension(group_id, artifact_id, version, config={}):
    extension = etree.SubElement(build_extensions, 'extension')
    etree.SubElement(extension, 'groupId').text = group_id
    etree.SubElement(extension, 'artifactId').text = artifact_id
    etree.SubElement(extension, 'version').text = version


add_build_extension('org.springframework.build', 'aws-maven', '5.0.0.RELEASE')

print etree.tostring(pom_root, pretty_print=True, encoding='UTF-8')

