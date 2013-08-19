import os, sys, subprocess, tempfile
from jar import Jar

def getPom(jar):
  poms = jar.findEntries('.*/pom.xml$')
  if len(poms) > 1:
    raise 'More than one pom file found'
  if len(poms) < 1:
    raise 'No pom.xml found'
  pom = jar.getEntry(poms[0])
  fd, name = tempfile.mkstemp()
  out = os.fdopen(fd, 'w')
  for line in pom.readlines():
    out.write(line)
  out.close()
  return name

def resolve(name):
  print 'Resolving jars from pom.xml'
  retcode = subprocess.Popen('mvn -f ' + name + ' dependency:resolve', shell=True,
      stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
  if retcode < 0:
    print >>sys.stderr, 'Error resolving maven dependencies'
  else:
    print 'Dependencies resolved successfully'
  os.remove(name)

def getJarList(jar):
  return jar.readManifest()['Class-Path']

def makeSymlinks(names):
  names = [(name, os.path.basename(name)) for name in names.split(' ') if not os.path.exists(name)]
  for root, dirs, files in os.walk(os.path.join(os.environ['HOME'], '.m2', 'repository')):
    for name in names:
      if name[1] in files:
        dir = os.path.dirname(name[0])
        os.path.exists(dir) or os.mkdir(dir)
        os.symlink(os.path.join(root, name[1]), name[0])
        names.remove(name)
  if len(names) > 0:
    print >>sys.stderr, 'Could not find the following dependencies:'
    print >>sys.stderr, ', '.join([name[1] for name in names])

if len(sys.argv) < 2:
  print "usage: " + sys.argv[0] + " [-r] jar-file"
  print "    -r   Do maven resolution beforehand"
  sys.exit(-1)

do_resolve = False
if sys.argv[1] == '-r':
  do_resolve = True
  sys.argv.pop(1)
jar = Jar(sys.argv[1])
if do_resolve:
  resolve(getPom(jar))
makeSymlinks(getJarList(jar))
