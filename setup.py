# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-pluggableappsettings',
    version='2.1.0',
    packages=find_packages(exclude=['*.tests',]),
    include_package_data=True,
    install_requires=['Django >=2.2',],
    license='MIT License',
    description='A convenience class for providing default values for a django app setting.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/NB-Dev/django-pluggableappsettings',
    author='Tim Schneider',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

