"""
PyStallone setup
"""
import sys
import os
from setuptools import setup

CLASSIFIERS = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
Programming Language :: Java
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Bio-Informatics
Topic :: Scientific/Engineering :: Chemistry
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
Topic :: Software Development :: Libraries :: Java Libraries
"""


# support python 2 and 3
jpype_species = 'JPype1>=0.5.6' if sys.version_info[0] == 2 else \
                'JPype1-py3>=0.5.5.2'
  
# same as git tag of stallone on github, change this on new release of stallone
stallone_version = u'v1.0'

# java library
jar_name = 'stallone-%s-jar-with-dependencies.jar' % stallone_version

dest = os.path.abspath(os.path.join(os.getcwd(), 'pystallone', jar_name))

class ReleaseNotFound(RuntimeError):
    pass

class ChecksumMismatch(RuntimeError):
    pass

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


def download_library():
    """downloads stallone jar library. uses global var stallone_version"""
    import hashlib
    import json
    import re

    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen

    print("downloading current jar library to %s" % dest)
    base_url="https://github.com/markovmodel/stallone/releases/download/"
    url = base_url + '/' + stallone_version + '/' + jar_name
    
    try:
        response = urlopen('https://api.github.com/repos/markovmodel/stallone/releases').read()
        releases = json.loads(response)
        # match tag_name with stallone_version
        for r in releases:
            if r['tag_name'] == stallone_version:
                rel = r
                break
        else:
            raise ReleaseNotFound()
        
        # extract sha256 checksum
        msg = rel['body']
        checksum = re.search('sha256:.(\w+)', msg).group(1)
       
        jar = urlopen(url).read()

        current = hashlib.sha256(jar).hexdigest()
        if not current == checksum:
            raise ChecksumMismatch('downloaded jar has invalid checksum.'
                               ' Is:\n"%s"\nShould be:\n"%s"' % (current, checksum))
        # write jar to pystallone/
        file = open(dest, 'wb')
        file.write(str(jar))
        print("finished")
    except IOError as ioe:
        print("error during download/saving jar:\n", ioe)
        sys.exit(1)
    except ChecksumMismatch as re:
        print("error during validation:\n", re)
        sys.exit(2)
    except ReleaseNotFound:
        print("target release '%s' could not be located on github."
              " Make sure this tag exists or change variable 'stallone_version'"
              " in this script." % stallone_version)
        sys.exit(3)
    except Exception as e:
        import traceback
        print("unknown exception occurred:\n")
        print(traceback.format_exc())
        sys.exit(255)


if not os.path.exists(dest):
    download_library()
    if not os.path.exists(dest):
        raise Exception("still not there - going to die... ^_^")

# write stallone jar filename to _file.py, so pystallone package knows it.
try:
    with open(os.path.join('pystallone', '_file.py'), 'w') as f:
        f.write('# auto-generated by setup.py, do NOT edit.\n')
        f.write('stallone_jar = "%s"\n' % jar_name)
except:
    print("failed to write jar filename to _file.py.")
    sys.exit(10) 


import imp
fp, pathname, description = imp.find_module('versioneer')
try:
    versioneer = imp.load_module('versioneer', fp, pathname, description)
finally:
    if fp: fp.close()

versioneer.VCS = 'git'
versioneer.versionfile_source = 'pystallone/_version.py'
versioneer.versionfile_build = None
versioneer.tag_prefix = 'v'  # tags are like v1.2.0
versioneer.parentdir_prefix = 'pystallone-'  # dirname like 'myproject-1.2.0'


metadata = dict(
    name='pystallone',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Python binding for Stallone java library',
    long_description=read('README.rst'),
    url='http://bitbucket.org/cmb-fu/stallone',
    author='Frank Noe, Martin K. Scherer',
    maintainer='Martin K. Scherer',
    author_email='stallone@lists.fu-berlin.de',
    packages=['pystallone'],
    package_data={'pystallone': [jar_name]},
    install_requires=[jpype_species,
                      'numpy >= 1.6.0'],
    tests_require=['unittest2', 'nose'],
    test_suite='nose.collector',
    zip_safe=False,
    keywords=['Markov modeling', 'Molecular trajectories analysis', 'MD'],
    license='Simplified BSD License',
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
)

# do not install requirements on readthedocs
if os.environ.get('READTHEDOCS'):
    metadata['install_requires'] = []

setup(**metadata)
