#!/usr/bin/env python

from setuptools import setup, find_packages

#
# Setuptools configuration, used to create python .eggs and such.
# See: http://bashelton.com/2009/04/setuptools-tutorial/ for a nice
# setuptools tutorial.
#

setup(
    name = "PyCardRPG",
    version = "0.1",
    description = "",
    long_description = "",
    url = "",
    download_url = "",
    
    # configuration information
    package_data = {"": ['*.yaml']},
    packages = find_packages(exclude="test"),
    
    # packages needed
    install_requires = [
        'pygame>=1.9.1'
    ],
    
    # entry_points
    entry_points = {
        'console_scripts': ['pycardrpg = pycardrpg.main:PyCardRPG.start']
    },
    
    # zip safe
    zip_safe = False
)