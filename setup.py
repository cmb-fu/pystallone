"""
PyStallone setup
"""
from setuptools import setup 
import os
import sys

# support python 2 and 3
jpype_species = 'JPype1>=0.5.5.4' if sys.version_info[0] == 2 else 'JPype1-py3>=0.5.5.2'

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

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
    package_data = {'pystallone' : ['stallone-current-jar-with-dependencies.jar',
                                    'include/jni.h',
                                    'include/jni_md.h']},
    install_requires = [jpype_species,
                        'numpy >= 1.6.0'],
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