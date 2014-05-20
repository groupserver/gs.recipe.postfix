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

    #: The name of the Postfix rule that will be created, and referred to in
    #: both the Alias and the Virtual file.
    AUTOMAGIC = 'groupserver-automagic'

    #: The name of the Postfix Alias file that will be created. See
    #: :manpage:`aliases(5)`.
    ALIAS = 'groupserver.aliases'

    #: The name of the Postfix Virtual file that will be created. See
    #: :manpage:`virtual(5)`.
    VIRTUAL = 'groupserver.virtual'

    @staticmethod
    def create_config_folder(configFolder):
        '''Create the configuration folder

:param str configFolder: The folder to created.
:return: ``None``

Creates the directory to hold the configuration files, if it does not already
exist.'''
        if not(os.path.isdir(configFolder)):
            os.mkdir(configFolder, 0o755)

    def create_alias(self, smtp2gs, site, port, usessl, configFolder):
        '''Create the alias file

:param str smtp2gs: The full path to the smtp2gs executable.
:param str site: The URL to the GroupServer site.
:param str port: The port that the GroupServer site is running on.
:param bool usessl: ``True`` if TLS should be used.
:param str configFolder: The path to the folder to write the alias file to.
:return: The path to the newly created configuration file.
:rtype: ``str``

This method creates an alias-file that can be used by Postfix.

.. seealso:: The :manpage:`aliases(5)` manual page.
'''
        outFileName = os.path.join(configFolder, self.ALIAS)
        m = '''# Postfix aliases, created by GroupServer.
# See aliases(5) for more information on this file. For more GroupServer
#     options see
#         {smtp2gs} --help
# Based on an example from VIRUAL_README
#     <http://www.postfix.org/VIRTUAL_README.html#mailing_lists>\n\n'''
        h = 'https' if usessl else 'http'
        # Format the port. Ignore if blank or the default for HTTP(S).
        p = ':%s' % port if (port and (port not in ('80', '443'))) else ''
        alias = '{automagic}:  "|{smtp2gs} {http}://{site}{port}"\n'
        o = m + alias
        outText = o.format(automagic=self.AUTOMAGIC, smtp2gs=smtp2gs, http=h,
                            site=site, port=p)
        with codecs.open(outFileName, mode='w', encoding=UTF8) as outFile:
            outFile.write(outText)
        return outFileName

    def create_virtual(self, site, configFolder):
        '''Create the virtual file

:param str site: The URL to the GroupServer site.
:param str configFolder: The path to the folder to write the alias file to.
:return: The path to the newly created configuration file.
:rtype: ``str``

This method creates an alias-file that can be used by Postfix.

.. seealso:: The :manpage:`virtual(5)` manual page.
'''
        outFileName = os.path.join(configFolder, self.VIRTUAL)
        m = '# Postfix virtual host setup, created by GroupServer.\n# See '\
            'virtual(5) for more information on the file format.\n'
        virtual = '{site}  virtual\n@{site}  {automagic}@localhost\n'
        outText = m + virtual.format(site=site, automagic=self.AUTOMAGIC)
        with codecs.open(outFileName, mode='w', encoding=UTF8) as outFile:
            outFile.write(outText)
        return outFileName

    def create(self, stmp2gs, site, port, usessl, configFolder):
        '''Create the alias and virtual files

:param str smtp2gs: The full path to the smtp2gs executable.
:param str site: The URL to the GroupServer site.
:param str port: The port that the GroupServer site is running on.
:param bool usessl: ``True`` if TLS should be used.
:param str configFolder: The path to the folder to write the alias file to.
:return: The paths to the newly created configuration files, as a two-member
         list: ``[alias, virtual]``
:rtype: ``list``

This is the main entry-point to the creator.
'''
        self.create_config_folder(configFolder)
        f1 = self.create_alias(stmp2gs, site, port, usessl, configFolder)
        f2 = self.create_virtual(site, configFolder)
        return [f1, f2]
