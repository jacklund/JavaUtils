JavaUtils
=========

Utilities to help with Java development and deployment

## Module jar.py
### Jar Class
Python class to parse Java jar files

#### Methods
##### Jar(jarfile)
Constructor for Jar class. _jarfile_ can be a string pathname or a file object

##### Jar.getEntry(name)
Retrieves the jar file entry _name_ as a file object

##### Jar.findEntries(regex)
Returns a list of entries in the jar file that match the given regular expression

##### Jar.readManifest()
Returns the jar manifest entries as a dictionary

## getJars.py
Python script to look inside an executable jar file, parse out its
classpath, optionally use any embedded `pom.xml` files to resolve jar dependencies, and then make symbolic links for all the dependencies in the classpath pointing to the local on-disk maven repository jars.

### Usage
    $ python getJars.py [-r] jar-file
        where -r means do maven dependency resolution first

What this script does is the following:

1. If the `-r` flag is specified, it finds the `pom.xml` file in the jar file, and does a `mvn dependency:resolve` on the pom file, which downloads all the dependencies into the local Maven repository (usually located in `~/.m2/repository`)
2. Next, it retrieves the `Class-Path` entry from the jar's `META-INF/MANIFEST.MF` file, and looks for each entry in the local Maven repository
3. For each jar file dependency it finds, it creates a symbolic link from the value specified in the manifest class path, pointing to the actual jar file in the Maven repository

Thus, assuming all dependencies are resolved and found, your executable jar file should be have all its dependencies resolved, and should run with `java -jar jar-file`.