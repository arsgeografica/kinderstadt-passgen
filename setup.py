#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer


versioneer.VCS = 'git'
versioneer.versionfile_source = 'kinderstadt_passgen/_version.py'
versioneer.versionfile_build = 'kinderstadt_passgen/_version.py'
versioneer.tag_prefix = 'v'
versioneer.parentdir_prefix = 'kinderstadt_passgen-'


setup(
    name="kinderstadt-passgen",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    install_requires=[

    ],
    extras_require={
        'devel': [
            'autopep8',
            'flake8',
            'ipython',
        ]
    },
)
