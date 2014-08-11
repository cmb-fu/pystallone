"""
PyStallone setup
"""
from setuptools import setup 
import os


metadata = dict(
    name = 'pystallone',
    version = '1.0-SNAPSHOT',
    # TODO: add url
    url = '',
    author = 'Frank Noe, Martin Scherer',
    maintainer = 'Martin Scherer',
    author_email = 'stallone@lists.fu-berlin.de',
    packages = ['pystallone'],
    package_data = {'pystallone' : ['stallone-current-jar-with-dependencies.jar',
                                    'include/jni.h',
                                    'include/jni_md.h']},
    install_requires = ['JPype1 >= 0.5.5.3',
                        'numpy >= 1.6.0'],
)

# HACK for JPype installation:
# we do not want the user to install a complete JDK, so we provide jni.h here.
# NOTE: this temporarily overrides an existing set JAVA_HOME, if you want to avoid
# this, comment this line! 
os.environ['JAVA_HOME'] = os.path.abspath(os.path.join('pystallone', 'include'))


setup(**metadata)