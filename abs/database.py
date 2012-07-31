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

from abs.error import BaseError
import os
import json
import logging
import xdg.BaseDirectory as basedirectory

class JsonDatabase(dict):
    '''Json database'''

    def _get_path(self, path, default_filename, create=False):
        '''Get a path and ensure its exists if create is True'''
        if path is None:
            path = os.path.join(basedirectory.xdg_cache_home,
                                "abs", default_filename)
        if create and not os.path.exists(path):
            directory = os.path.split(path)[0]
            if directory != "" and not os.path.isdir(directory):
                try:
                    os.makedirs(directory)
                except (IOError, OSError) as e:
                    raise BaseError("Create database directories failed: %s" % e)
            try:
                open(path, "a")
            except (IOError, OSError) as e:
                raise BaseError("Create database filename failed; %s" % e)
        return path

    def load(self, path, default_filename):
        '''Load registered version database into this database'''
        assert(default_filename is not None)
        # find the right path
        path = self._get_path(path, default_filename)
        if path is not None:
            logging.debug("Loading database %s" % path)
            try:
                fileobj = open(path, "r")
                dico = json.load(fileobj)
                self.update(dico)
            except Exception as e:
                logging.error("Unable to load database %s: %s" % (path, e))


    def save(self, path, default_filename, save_empty=False):
        '''Save current version database into a file'''
        assert(default_filename is not None)
        if not save_empty and len(self) == 0:
            logging.debug("Not really saved. Database is empty")
            return
        # find the right path
        path = self._get_path(path, default_filename, create=True)
        if path is not None:
            logging.debug("Saving database %s" % path)
            try:
                fileobj = open(path, "w")
                dico = json.dump(self, fileobj)
            except Exception as e:
                logging.error("Unable to save database %s: %s" % (path, e))
