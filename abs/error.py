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

ERR_USAGE = 1
ERR_FATAL = 2

class AbsError(Exception):
    '''ABS errors base class'''
    pass

class VersionNotFound(AbsError):
    '''Version of a package is not found'''
    pass

class ConfigFileError(AbsError):
    '''All errors related to config file '''
    pass

class MissingConfigFile(ConfigFileError):
    '''Config file is missing'''
    pass

class InvalidConfigFile(ConfigFileError):
    '''Config file is bad formatted'''
    pass

# vim:set ts=4 sw=4 et ai:
