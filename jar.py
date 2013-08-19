import re, sys, zipfile

class Jar:
  """Class to parse a Java Jar file"""

  def __init__(self, jarfile):
    """Constructor. Takes a filename or file object"""
    self.zip = zipfile.ZipFile(jarfile, 'r')
    self.manifest = None

  def getEntry(self, name):
    """Return a file object for a Jar file entry named 'name'"""
    return self.zip.open(name)

  def findEntries(self, name):
    """Return a list of Jar file entries that match the given regular expression 'name'"""
    pattern = re.compile(name)
    list = []
    for info in self.zip.infolist():
      if pattern.match(info.filename):
        list.append(info.filename)
    return list

  def readManifest(self):
    """Read the Jar's manifest and return it as a dictionary"""
    pattern = re.compile('(^\S*): (.*)$')
    if not self.manifest:
      self.manifest = {}
      key = None
      value = None
      with self.getEntry('META-INF/MANIFEST.MF') as f:
        for line in f:
          line = line[:-2]
          match = pattern.match(line)
          if match:
            if (key):
              self.manifest[key] = value
            key = match.group(1)
            value = match.group(2)
          else:
            value = ''.join([value, line[1:]])
      self.manifest[key] = value
    return self.manifest

if __name__ == "__main__":
  jar = Jar(sys.argv[1])
  print jar.readManifest()['Class-Path']
  pom = jar.findEntries('.*/pom.xml$')
  print pom[0]
