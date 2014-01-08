# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.opensearch
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.5'

long_description = (
    read('README.rst')
    + '\n' +
    read("docs", "HISTORY.txt")
    #+ '\n' +
    #'Detailed Documentation\n'
    #'**********************\n'
    #+ '\n' +
    #read('collective', 'opensearch', 'README.txt')
    #+ '\n' +
    #'Contributors\n'
    #'************\n'
    #+ '\n' +
    #read('CONTRIBUTORS.txt')
    #+ '\n' +
    #'Download\n'
    #'********\n'
    )

tests_require = ['zope.testing']

setup(name='collective.opensearch',
      version=version,
      description="""Collective Opensearch Collective.opensearch adds
        the ability to produce search results in the simple OpenSearch
        format.""",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='http://plone.org/products/plos',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                         'plone.app.registry',
                         'feedparser',
                         'chardet',
                         'htmllaundry',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='collective.opensearch.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
