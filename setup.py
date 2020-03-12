#!/usr/bin/env python3
"""
Run 'pip install .' to install emPHASEis.
"""

# Make sure this is being run with Python 3.4 or later.
import sys
if sys.version_info.major != 3 or sys.version_info.minor < 4:
    print('Error: you must execute setup.py using Python 3.4 or later')
    sys.exit(1)

import os
import shutil
from distutils.command.build import build
from distutils.core import Command
import subprocess
import multiprocessing
import fnmatch
import importlib.util

# Install setuptools if not already present.
if not importlib.util.find_spec("setuptools"):
    import ez_setup
    ez_setup.use_setuptools()

from setuptools import setup
from setuptools.command.install import install

# Get the program version from another file.
exec(open('emphaseis/version.py').read())


setup(name='emphaseis',
      version=__version__,
      description='emPHASEis: Putting the emPHASEis on the right sylLABle. A next-generation read phaser for diagnostic amplicons.',
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      url='http://github.com/aineniamh/emPHASEis',
      author='Aine O Toole,
      author_email='aine.otoole@ed.ac.uk',
      license='GPL',
      packages=['emphaseis'],
      entry_points={"console_scripts": ['emphaseis = emphaseis.emphaseis:main']},
      zip_safe=False,
      cmdclass={'build': Build,
                'install': Install,
                'clean': Clean}
      )
