# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.txt', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"), encoding='utf-8') as f:
    long_description += '\n' + f.read()

entry_point = 'gs.recipe.postfix:PostfixConfigRecipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

setup(name='gs.recipe.postfix',
      version=version,
      description="Setup the Postfix configuration for GroupServer",
      long_description=long_description,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Buildout',
        'Framework :: Zope2',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
      ],
      keywords='groupserver, Postfix, recipe, buildout, setup, email, install',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://source.iopen.net/groupserver/gs.recipe.postifx/',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'zc.buildout', ],
      entry_points=entry_points,
      test_suite='gs.recipe.postfix.tests.test_all',
      tests_require=['zope.testing', 'mock'],
      extras_require={'docs': ['Sphinx', ], },
      )
