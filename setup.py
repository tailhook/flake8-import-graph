#!/usr/bin/env python3

from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), 'rt') as f:
    long_description = f.read()

setup(name='flake8-import-graph',
      version='0.1.0',
      description="A flake8 lint to enforce that some modules "
                  "can't be imported from other modules.",
      author='Paul Colomiets',
      author_email='paul@colomiets.name',
      url='http://github.com/tailhook/flake8-import-graph',
      packages=find_packages(where='src'),
      package_dir={"": "src"},
      install_requires=[
        'flake8 > 3.0.0',
      ],
      entry_points={
          'flake8.extension': [
              'IMP = flake8_import_graph:ImportGraphChecker',
          ],
      },
      classifiers=[
          "Framework :: Flake8",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Quality Assurance",
      ],
      long_description=long_description,
)
