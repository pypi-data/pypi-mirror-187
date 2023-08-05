# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 21 Jan 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import setuptools
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='finlay',
    version='0.1.8',
    author='Sabbir Amin',
    author_email='sabbiramin.cse11ruet@gmail.com',
    description='A Toy Experiment to ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sabbiramin113008/finlay',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    zip_safe=False
)