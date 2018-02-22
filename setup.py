#!/usr/bin/python

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="dojot-alarmlibrary",
    version="0.0.1",
    author="Marcelo",
    author_email="marcelon@cpqd.com",
    description=("Client library to communicate with the alarm manager server"),
    license="GPL-3.0",
    keywords="dojot alarm client",
    install_requires=['pika==0.11.2', 'enum34==1.1.6'],
    packages=find_packages(),
    long_description=read('README.md'),
)
