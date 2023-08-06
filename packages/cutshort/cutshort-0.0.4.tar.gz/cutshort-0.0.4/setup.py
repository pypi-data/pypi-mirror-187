# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 21 Jan 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import setuptools
from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='cutshort',
    version='0.0.4',
    author='Sabbir Amin',
    author_email='sabbiramin.cse11ruet@gmail.com',
    description='Yet another, experimental utility to write wsgi REST API apps using python functions, Mostly.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sabbiramin113008/cutshort',
    packages=setuptools.find_packages(),
    install_requires=['parse', 'WebOb', 'Werkzeug'],
    license='MIT',
    keywords=['python', 'wsgi', 'RESTAPI', 'function-to-rest-endpoint'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    zip_safe=False
)
