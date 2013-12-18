#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from setuptools import setup


def readfile(file_name):
    f = open(os.path.join(os.path.dirname(__file__), file_name))
    return f.read()


setup(
    name='tornado-cors',
    version='0.4.0',
    keywords='tornado cors',
    author='globo.com',
    author_email='guilherme.cirne@corp.globo.com',
    url='https://github.com/globocom/tornado-cors',
    license = 'MIT',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Software Development :: Libraries',
    ],
    include_package_data=True,
    packages = ['tornado_cors'],
    install_requires=[requirement for requirement in readfile('requirements.txt').split('\n') if requirement],
)
