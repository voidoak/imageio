# -*- coding: utf-8 -*-
# Copyright (C) 2012, imageio contributers
#
# imageio is distributed under the terms of the (new) BSD License.
# The full license can be found in 'license.txt'.

import os
import sys
from distutils.core import setup

name = 'imageio'
description = 'Library for reading and writing a wide range of image formats.'

# Get version and docstring
__version__ = None
__doc__ = ''
docStatus = 0 # Not started, in progress, done
initFile = os.path.join(os.path.dirname(__file__), '__init__.py')
for line in open(initFile).readlines():
    if (line.startswith('__version__')):
        exec(line.strip())
    elif line.startswith('"""'):
        if docStatus == 0:
            docStatus = 1
            line = line.lstrip('"')
        elif docStatus == 1:
            docStatus == 2
    if docStatus == 1:
        __doc__ += line

# todo: Allow downloading during runtime as well (but not when frozen)
# todo: Windows generates a warning popup when trying to load the MAC dll.
# todo: make libs work when frozen

# Download libs and put in the lib dir
from freeimage_install import retrieve_files
if 'sdist' in sys.argv:
    retrieve_files(True) # Retieve *all* binaries
else:
    retrieve_files() # Retieve only the one for this OS


setup(
    name = name,
    version = __version__,
    author = 'imageio contributers',
    author_email = 'a.klein@science-applied.nl',
    license = '(new) BSD',
    
    url = 'http://imageio.readthedocs.org',
    download_url = 'http://bitbucket.org/almarklein/imageio/downloads',    
    keywords = "FreeImage image imread imwrite io",
    description = description,
    long_description = __doc__,
    
    platforms = 'any',
    provides = ['imageio'],
    requires = ['numpy'],
    
    packages = ['imageio'],
    package_dir = {'imageio': '.'}, # must be a dot, not an empty string
    package_data = {'imageio': ['lib/*',]},
    zip_safe = False, # I want examples to work
    )