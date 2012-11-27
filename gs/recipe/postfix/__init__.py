# -*- coding: utf-8 -*-
import os
import sys
from creator import ConfigurationCreator


class Recipe(object):
    """zc.buildout recipe"""

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
Skipped: The setup script %s has already been run. If you want
to run it again set the run-once option to false or delete
%s
*********************************************************************\n\n''' %\
                    (self.name, self.fileName)
                sys.stdout.write(m)
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
            except OSError, e:
                m = '{name}: Failed to create example Postfix configuration :'\
                    'in "{dir}":\n{error}\n'
                sys.stderr.write(m.format(name=self.name, dir=d, error=e))
                sys.exit(1)
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
