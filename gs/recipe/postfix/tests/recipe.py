# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from mock import patch, MagicMock
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

    def tearDown(self):
        rmtree(self.tempdir)

    @patch('gs.recipe.postfix.recipe.sys.stdout')
    def test_install(self, m_stdout):
        'Test a "normal" call of install'
        r = self.recipe.should_run()
        self.assertTrue(r)

        gs.recipe.postfix.recipe.ConfigurationCreator.create = MagicMock()
        self.recipe.install()

        c = gs.recipe.postfix.recipe.ConfigurationCreator.create.call_count
        self.assertEqual(1, c)
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertEqual('', args[2])
        self.assertFalse(args[3])  # use_ssl

        c = m_stdout.write.call_count
        self.assertEqual(1, c)

        r = self.recipe.should_run()
        self.assertFalse(r)

    def test_install_port(self):
        'Test an install with a port specified'
        gs.recipe.postfix.recipe.ConfigurationCreator.create = MagicMock()
        self.options['port'] = '90210'
        with patch('gs.recipe.postfix.recipe.sys.stdout'):
            self.recipe.install()

        c = gs.recipe.postfix.recipe.ConfigurationCreator.create.call_count
        self.assertEqual(1, c)
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertEqual('90210', args[2])
        self.assertFalse(args[3])  # use_ssl

    def test_install_ssl(self):
        'Test an install with a use_ssl specified'
        gs.recipe.postfix.recipe.ConfigurationCreator.create = MagicMock()
        self.options['use_ssl'] = '90210'  # Anything not False is True.
        with patch('gs.recipe.postfix.recipe.sys.stdout'):
            self.recipe.install()

        c = gs.recipe.postfix.recipe.ConfigurationCreator.create.call_count
        self.assertEqual(1, c)
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertEqual('', args[2])  # Port
        self.assertTrue(args[3])  # use_ssl

    def test_install_ssl_off(self):
        'Test an install with a use_ssl specified as false.'
        gs.recipe.postfix.recipe.ConfigurationCreator.create = MagicMock()
        self.options['use_ssl'] = 'off'
        with patch('gs.recipe.postfix.recipe.sys.stdout'):
            self.recipe.install()

        c = gs.recipe.postfix.recipe.ConfigurationCreator.create.call_count
        self.assertEqual(1, c)
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertEqual('', args[2])  # port
        self.assertFalse(args[3])  # use_ssl

        self.options['use_ssl'] = 'false'
        with patch('gs.recipe.postfix.recipe.sys.stdout'):
            self.recipe.install()
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertFalse(args[3])  # use_ssl

        self.options['use_ssl'] = 'no'
        with patch('gs.recipe.postfix.recipe.sys.stdout'):
            self.recipe.install()
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertFalse(args[3])  # use_ssl

    def test_install_ssl_port(self):
        'Test an install with a use_ssl specified'
        gs.recipe.postfix.recipe.ConfigurationCreator.create = MagicMock()
        self.options['use_ssl'] = 'Yes'  # Anything not False is True.
        self.options['port'] = '90210'
        with patch('gs.recipe.postfix.recipe.sys.stdout'):
            self.recipe.install()

        c = gs.recipe.postfix.recipe.ConfigurationCreator.create.call_count
        self.assertEqual(1, c)
        args, kwargs = \
            gs.recipe.postfix.recipe.ConfigurationCreator.create.call_args
        self.assertEqual('90210', args[2])  # Port
        self.assertTrue(args[3])  # use_ssl

    def test_install_oserror(self):
        'Test that ``install`` hitting an ``OSError`` raises a UserError'
        r = self.recipe.should_run()
        self.assertTrue(r)

        gs.recipe.postfix.recipe.ConfigurationCreator.create = \
            MagicMock(side_effect=OSError)
        self.assertRaises(UserError, self.recipe.install)

        r = self.recipe.should_run()
        self.assertTrue(r)  # Should not be locked after the raise
