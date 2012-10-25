# -*- coding: utf-8 -*-
import os
import sys


class ConfigurationCreator(object):
    automagic = 'groupserver-automagic'
    def __init__(self):
        pass

    def create_config_folder(self, configFolder):
        if not(os.path.isdir(configFolder)):
            os.mkdir(configFolder, 0755)
        assert os.path.isdir(configFolder), \
            '{} does not exist'.format(configFolder)

    def create_alias(self, smtp2gs, site, configFolder):
        outFileName = '{}/groupserver.aliases'.format(configFolder)
        m = '# Postfix aliases, created by GroupServer.\n# See aliases(5) for '\
            'more information on this file. For more\n# GroupServer options '\
            'see\n#    {smtp2gs} --help\n'
        alias = '{automagic}:  "|{smtp2gs} http://{site}"\n'
        outText = (m + alias).format(automagic=self.automagic, smtp2gs=smtp2gs, 
                                     site=site)
        with file(outFileName, 'w') as outFile:
            outFile.write(outText)
        return outFileName
    
    def create_virtual(self, site, configFolder):
        outFileName = '{}/groupserver.virtual'.format(configFolder)
        m = '# Postfix virtual host setup, created by GroupServer.\n# See '\
            'virtual(5) for more information on the file format.\n'
        virtual = '{site}  virtual\n@{site}  {automagic}\n'
        outText = m + virtual.format(site=site, automagic=self.automagic)
        with file(outFileName, 'w') as outFile:
            outFile.write(outText)
        return outFileName

    def create(self, stmp2gsPath, site, configFolder):
        self.create_config_folder(configFolder)
        f1 = self.create_alias(stmp2gsPath, site, configFolder)
        f2 = self.create_virtual(site, configFolder)
        return [f1, f2]
