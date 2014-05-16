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
import os
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
from gs.recipe.postfix.creator import ConfigurationCreator


class TestCreator(TestCase):
    'Test the creation of the script.'

    def setUp(self):
        self.creator = ConfigurationCreator()
        self.tempDir = mkdtemp()
        self.folder = os.path.join(self.tempDir, 'postfix')

    def tearDown(self):
        rmtree(self.tempDir)

    def test_create_config_folder(self):
        'Test the creation of the configuration folder'
        self.creator.create_config_folder(self.folder)
        self.assertTrue(os.path.isdir(self.folder))

    def _test_create_alias(self):
        'Test the creation of the alias-file'

    def _test_create_virtual(self):
        'Test the creation of the virtual file'

    def _test_create(self):
        'Test the create method.'
