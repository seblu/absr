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

from collections import OrderedDict
from configparser import RawConfigParser
import abs.error
import logging
import os
import xdg.BaseDirectory as basedirectory

class BaseConfigFile(object):
    '''Base ABS config file'''

    def __init__(self, path, default_filename):
        '''Initialize config object'''
        assert(default_filename is not None)
        self.path = path
        if path is None:
            self.path = basedirectory.load_first_config("abs", default_filename)
        if not isinstance(self.path, str) or not os.path.exists(self.path):
            logging.debug("No such config file: %s" % self.path)
            raise abs.error.MissingConfigFile()
        self.load()

    def load(self):
        '''Load configuration'''
        logging.debug("loading config file at: %s" % self.path)
        # FIXME: use an ordereddict?
        self._configparser = RawConfigParser()
        self._configparser.read(self.path)
        self.config = OrderedDict()
        for name in self._configparser.sections():
            self.config[name] = OrderedDict(self._configparser.items(name))
