# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.opensearch',
      version=version,
      description="Adds OpenSearch descriptions and functionality to Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Héctor José Rico García, Pedro Pernías, Manolo Marco, Leonel Iriarte',
      author_email='',
      url='http://svn.plone.org/svn/collective/collective.opensearch',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
