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
from __future__ import unicode_literals
import codecs
import os
UTF8 = 'utf-8'


class ConfigurationCreator(object):
    'Create the configuration for Postfix'

    AUTOMAGIC = 'groupserver-automagic'
    ALIAS = 'groupserver.aliases'
    VIRTUAL = 'groupserver.virtual'

    def create_config_folder(self, configFolder):
        'Create the configuration folder'
        if not(os.path.isdir(configFolder)):
            os.mkdir(configFolder, 0o755)

    def create_alias(self, smtp2gs, site, configFolder):
        'Create the alias file'
        outFileName = os.path.join(configFolder, self.ALIAS)
        m = '# Postfix aliases, created by GroupServer.\n# See aliases(5) '\
            'for more information on this file. For more\n# GroupServer '\
            'options see\n#    {smtp2gs} --help\n'
        alias = '{automagic}:  "|{smtp2gs} http://{site}"\n'
        outText = (m + alias).format(automagic=self.AUTOMAGIC,
                                        smtp2gs=smtp2gs, site=site)
        with codecs.open(outFileName, mode='w', encoding=UTF8) as outFile:
            outFile.write(outText)
        return outFileName

    def create_virtual(self, site, configFolder):
        'Create the virtual file'
        outFileName = os.path.join(configFolder, self.VIRTUAL)
        m = '# Postfix virtual host setup, created by GroupServer.\n# See '\
            'virtual(5) for more information on the file format.\n'
        virtual = '{site}  virtual\n@{site}  {automagic}\n'
        outText = m + virtual.format(site=site, automagic=self.AUTOMAGIC)
        with codecs.open(outFileName, mode='w', encoding=UTF8) as outFile:
            outFile.write(outText)
        return outFileName

    def create(self, stmp2gsPath, site, configFolder):
        self.create_config_folder(configFolder)
        f1 = self.create_alias(stmp2gsPath, site, configFolder)
        f2 = self.create_virtual(site, configFolder)
        return [f1, f2]
