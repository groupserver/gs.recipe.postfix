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
from mock import MagicMock
import os
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
from zc.buildout import UserError
import gs.recipe.postfix.recipe
from gs.recipe.postfix.recipe import PostfixConfigRecipe
UTF8 = 'utf-8'


class TestRecipe(TestCase):
    def setUp(self):
        self.tempdir = mkdtemp()
        self.bindir = os.path.join(self.tempdir, 'bin')
        os.mkdir(self.bindir)
        vardir = os.path.join(self.tempdir, 'var')
        os.mkdir(vardir)

        self.buildout = {'buildout': {'directory': self.tempdir,
                                        'bin-directory': self.bindir, }, }
        self.name = 'postfix'
        self.options = {}
        self.options['smtp2gs_path'] = os.path.join(self.tempdir, 'smtp2gs')
        self.options['site'] = 'groups.example.com'
        self.options['recipe'] = 'gs.recipe.postfix'
        self.recipe = PostfixConfigRecipe(self.buildout, self.name,
                                            self.options)

        gs.recipe.postfix.recipe.sys.stdout = MagicMock()
        gs.recipe.postfix.recipe.sys.stderr = MagicMock()

    def tearDown(self):
        rmtree(self.tempdir)

    def test_install(self):
        'Test a "normal" call of install'
        r = self.recipe.should_run()
        self.assertTrue(r)

        gs.recipe.postfix.recipe.ConfigurationCreator.create = MagicMock()
        self.recipe.install()

        c = gs.recipe.postfix.recipe.ConfigurationCreator.create.call_count
        self.assertEqual(1, c)
        c = gs.recipe.postfix.recipe.sys.stdout.write.call_count
        self.assertEqual(1, c)

        r = self.recipe.should_run()
        self.assertFalse(r)

    def test_install_oserror(self):
        'Test that ``install`` hitting an ``OSError`` raises a UserError'
        r = self.recipe.should_run()
        self.assertTrue(r)

        gs.recipe.postfix.recipe.ConfigurationCreator.create = \
            MagicMock(side_effect=OSError)
        self.assertRaises(UserError, self.recipe.install)

        r = self.recipe.should_run()
        self.assertTrue(r)  # Should not be locked after the raise
