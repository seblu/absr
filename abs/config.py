# coding: utf-8

# abs - Archlinux Build System
# Copyright © 2012 Sébastien Luttringer
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from configparser import RawConfigParser
import abs.error
import logging
import os
import xdg.BaseDirectory as basedirectory

class AbsConfig(object):
    '''Base ABS config file'''

    def __init__(self, path, filename):
        '''Initialize config object'''
        if path is None:
            self.path = basedirectory.load_first_config("abs", filename)
        else:
            self.path = path
        logging.debug("initialized config file path is: %s" % self.path)
        if not isinstance(self.path, str) or not os.path.exists(self.path):
            raise abs.error.MissingConfigFile()
        self.load()

    def load(self):
        '''Load configuration if exists or create an empty one'''
        raise NotImplemented()


class PackagesConfigFile(AbsConfig):
    '''
    This class load an INI file

    Each section is a package name
    '''

    def load(self):
        '''Load configuration'''
        logging.debug("loading packages file at: %s" % self.path)
        # FIXME: use an ordereddict?
        self._configparser = RawConfigParser()
        # open config file
        try:
            self._configparser.read(self.path)
        except IOError as e:
            logging.error("Unable to open %s: %s" % (self.path, e))
            raise abs.error.ConfigFileError(e)
        self.packages = {}
        for name in sorted(self._configparser.sections()):
            self.packages[name] = dict(self._configparser.items(name))
