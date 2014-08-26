"""
PyStallone setup
"""
from setuptools import setup 
import os
import sys

# support python 2 and 3
PY3 = (sys.version_info[0] >= 3)
jpype_species = 'JPype1-py3>=0.5.5.2' if PY3 else 'JPype1>=0.5.5.4'

# java library
jar_name = 'stallone-1.0-SNAPSHOT-jar-with-dependencies.jar'

dest = os.path.abspath(os.path.join(os.getcwd(),'pystallone', jar_name))

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

def download_library():
    import hashlib
    if sys.version_info >= (3,):
        import urllib.request as urllib2
    else:
        import urllib2

    print("downloading current jar library to %s" % dest)
    # TODO: move destination of jar to maven central and validate via gpg
    base_url = 'http://www.mi.fu-berlin.de/users/marscher/'
    jar_url = base_url + jar_name
    try:
        data = urllib2.urlopen(jar_url).read() # binary
        checksum = urllib2.urlopen(jar_url + '.sha256').read().decode().split(' ')[0]
        current = hashlib.sha256(data).hexdigest()
        if not current == checksum:
            raise RuntimeError('downloaded jar has invalid checksum.'
                               ' Is:\n"%s"\nShould be:\n"%s"' % (current, checksum))
        # write jar to pystallone/
        file = open(dest, 'w')
        file.write(str(data))
        print("finished")
    except IOError as ioe:
        print("error during download/saving jar:\n", ioe)
        sys.exit(1)
    except RuntimeError as re:
        print("error during validation:\n", re)
        sys.exit(2)
    except Exception as e:
        import traceback
        print("unknown exception occurred:\n")
        print(traceback.format_exc())
        sys.exit(3)


if not os.path.exists(dest):
    download_library()
    if not os.path.exists(dest):
        raise Exception("still not there - going to die... ^_^")

metadata = dict(
    name = 'pystallone',
    version = '1.0-SNAPSHOT',
    description = 'Python binding for Stallone java library',
    long_description = read('README.rst'),
    url = 'http://bitbucket.org/cmb-fu/stallone',
    author = 'Frank Noe, Martin K. Scherer',
    maintainer = 'Martin K. Scherer',
    author_email = 'stallone@lists.fu-berlin.de',
    packages = ['pystallone'],
    package_data = {'pystallone' : [jar_name,
                                    'include/jni.h',
                                    'include/jni_md.h']},
    install_requires = [jpype_species,
                        'numpy >= 1.6.0'],
    tests_requires = ['unittest2'],
    keywords = ['Markov modeling', 'Molecular trajectories analysis', 'MD'],
    license='Simplified BSD License',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Java',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Java Libraries'
    ],
)

# HACK for JPype installation:
# we do not want the user to install a complete JDK, so we provide jni.h here.
# NOTE: this temporarily overrides an existing set JAVA_HOME, if you want to avoid
# this, comment this line! 
os.environ['JAVA_HOME'] = os.path.abspath(os.path.join('pystallone', 'include'))


setup(**metadata)