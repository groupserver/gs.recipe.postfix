# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2014 OnlineGroups.net and Contributors.
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
import sys
from zc.buildout import UserError
from .creator import ConfigurationCreator
from gs.recipe.base import Recipe


class PostfixConfigRecipe(Recipe):
    """zc.buildout recipe to create the Postifx config file"""
    POSTFIX_CONF_DIR = 'postfix_config'

    def install(self):
        """Installer"""
        if self.should_run():
            d = self.buildout['buildout']['directory']
            configFolder = os.path.join(d, self.POSTFIX_CONF_DIR)
            try:
                configCreator = ConfigurationCreator()
                # The 'False' is deliberate
                useSSL = self.options.get('use_ssl', 'False').lower() \
                            not in ['false', 'off', 'no']
                writtenFiles = configCreator.create(
                    self.options['smtp2gs_path'],
                    self.options['site'],
                    self.options.get('port', ''),
                    useSSL,
                    configFolder)
            except OSError as e:
                m = '{0}: Failed to create example Postfix configuration :'\
                    'in "{1}":\n{2}'
                msg = m.format(self.name, d, e)
                raise UserError(msg)
            else:
                self.mark_locked()
                fns = '\n    '.join(writtenFiles)
                m = '\nExample Postfix configuration written to\n    {0}\n'
                msg = m.format(fns)
                sys.stdout.write(msg)
        return tuple()

    def update(self):
        """Updater"""
        self.install()
