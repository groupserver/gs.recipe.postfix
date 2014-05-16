# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
import codecs
import os
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
from gs.recipe.postfix.creator import ConfigurationCreator
UTF8 = 'utf-8'


class TestCreator(TestCase):
    'Test the creation of the script.'

    def setUp(self):
        self.creator = ConfigurationCreator()
        self.tempDir = mkdtemp()
        self.folder = os.path.join(self.tempDir, 'postfix')

    def tearDown(self):
        rmtree(self.tempDir)

    def file_test(self, filePath):
        self.assertIn(self.tempDir, filePath)
        self.assertTrue(os.path.isfile(filePath))

    def file_content_test(self, filePath, contents=[]):
        with codecs.open(filePath, mode='r', encoding=UTF8) as inFile:
            data = inFile.read()
        for c in contents:
            self.assertIn(c, data)

    def test_create_config_folder(self):
        'Test the creation of the configuration folder'
        self.creator.create_config_folder(self.folder)
        self.assertTrue(os.path.isdir(self.folder))

    def test_create_alias(self):
        'Test the creation of the alias-file'
        r = self.creator.create_alias('smtp2gs', 'groups.example.com',
                                        self.tempDir)
        self.file_test(r)
        self.file_content_test(r, ('smtp2gs', 'groups.example.com'))

    def test_create_virtual(self):
        'Test the creation of the virtual file'
        r = self.creator.create_virtual('groups.example.com',
                                        self.tempDir)
        self.file_test(r)
        self.file_content_test(r, ('groups.example.com', ))

    def test_create(self):
        'Test the create method.'
        r0, r1 = self.creator.create('smtp2gs', 'groups.example.com',
                                            self.folder)
        self.file_test(r0)
        self.file_content_test(r0, ('smtp2gs', 'groups.example.com'))
        self.file_test(r1)
        self.file_content_test(r1, ('groups.example.com', ))
