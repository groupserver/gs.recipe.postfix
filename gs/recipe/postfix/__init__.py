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


class Recipe(object):
    """zc.buildout recipe to create the Postifx config file"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.fileName = os.path.join(self.buildout['buildout']['directory'],
                                     'var', "%s.cfg" % self.name)

        # suppress script generation
        self.options['scripts'] = ''
        options['bin-directory'] = buildout['buildout']['bin-directory']

    def should_run(self):
        runonce = ((('run-once' in self.options)
                    and self.options['run-once'].lower()) or 'true')
        #We'll use the existance of this file as flag for the run-once option
        retval = True  # Uncharactistic optomisim
        if runonce not in ['false', 'off', 'no']:
            if os.path.exists(self.fileName):
                m = '''
*********************************************************************
Skipped: The setup script {0}} has already been run. If you want
to run it again set the "run-once" option to false or delete
{1}
*********************************************************************\n\n'''
                msg = m.format(self.name, self.fileName)
                sys.stdout.write(msg)
                retval = False
        return retval

    def mark_locked(self):
            with file(self.fileName, 'w') as lockfile:
                lockfile.write('1')

    def install(self):
        """Installer"""
        if self.should_run():
            d = '{directory}/postfix_config'
            configFolder = d.format(**self.buildout['buildout'])
            try:
                configCreator = ConfigurationCreator()
                writtenFiles = configCreator.create(
                    self.options['smtp2gs_path'],
                    self.options['site'],
                    configFolder)
            except OSError as e:
                m = '{0}: Failed to create example Postfix configuration :'\
                    'in "{1}":\n{2}'
                msg = m.format(self.name, d, e)
                UserError(msg)
            else:
                self.mark_locked()
                m = '\nExample Postfix configuration written to\n'
                sys.stdout.write(m)
                for fileName in writtenFiles:
                    sys.stdout.write('{0}\n'.format(fileName))
                sys.stdout.write('\n')
        return tuple()

    def update(self):
        """Updater"""
        self.install()
