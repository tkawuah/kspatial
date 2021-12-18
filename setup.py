# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 15:41:12 2021

@author: Awuah
"""
from setuptools import setup, find_packages

__author__ = 'Kwame T. Awuah'
__email__ = 'tkawuah@gmail.com'

classifiers=[
    'Development Status :: 3 - Alpha'
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

with open('requirements.txt') as foo:
    REQUIREMENTS = [l.strip() for l in foo.readlines()]

setup(
    name=kspatial,
    version='0.0.1',
    url='https://github.com/tkawuah/kspatial',
    description='A collection of functions for processing geospatial raster and vector data',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    license='MIT',
    platforms='any',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    install_requires=REQUIREMENTS,
    keywords='geoprocessing, raster, vector',
    python_requires='>=3.0',
    classifiers=classifiers
)