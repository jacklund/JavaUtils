JavaUtils
=========

Utilities to help with Java development and deployment

## jar.py
Python class to parse Java jar files

## getJars.py
Python script to look inside an executable jar file, parse out its
classpath, optionally use any embedded `pom.xml` files to resolve jar dependencies, and then make symbolic links for all the dependencies in the classpath pointing to the local on-disk maven repository jars.