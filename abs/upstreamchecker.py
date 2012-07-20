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

import abs.error
import configparser
import distutils.version
import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
import xdg.BaseDirectory as BaseDirectory


class UpstreamChecker(object):

    def __init__(self, config):
        self.cp = configparser.RawConfigParser()
        # path of default config file if not given
        if config is None:
            config = os.path.join(BaseDirectory.save_config_path("auc"), "config")
        # open config file
        try:
            self.cp.read(config)
        except IOError as e:
            exit("Unable to open %s: %s" % (config, e))

    def softwares_generator(self, softwares=None):
        if softwares is None:
            softwares = sorted(self.cp.sections())
        for name in softwares:
            d = dict(self.cp.items(name))
            yield (name, d)

    def get_version_upstream(self, name, value):
        '''Return upstream version'''
        logging.debug("Get upstream version")
        # check upstream param
        if "url" not in value:
            logging.error("No url specified for %s" % name)
            raise NameError("Missing url in config file")
        url = value["url"]
        regex = value.get("regex", "%s[-_]v?(%s)%s" % (
                    value.get("regex_name", name),
                    value.get("regex_version", "[-.\w]+"),
                    value.get("regex_ext", "\.(?:tar(?:\.gz|\.bz2|\.xz)?|tgz|tbz2|zip)")))
        # do the job
        try:
            logging.debug("Requesting url: %s" % url)
            o = urllib.request.urlopen(url)
            logging.debug("Version regex: %s" % regex)
            v = re.findall(regex, o.read().decode("utf-8"))
            if v is None:
                raise abs.error.VersionNotFound("No regex match on upstream")
            # remove duplicity
            v = list(set(v))
            # list all found versions
            logging.debug("Found versions: %s" % v)
            v =  sorted(v, key=distutils.version.LooseVersion, reverse=True)[0]
            # list selected version
            logging.debug("Upstream version is : %s" % v)
            return v
        except urllib.error.URLError as e:
            raise abs.error.VersionNotFound("Upstream check failed for %s: %s" % (name, e))
        assert(False)

    def get_version_archlinux(self, name, value):
        '''Return archlinux version'''
        logging.debug("Get archlinux version")
        # check upstream param
        # if arch is specified
        if "arch" in value:
            archs = (value.get["arch"],)
        else:
            archs = ("x86_64", "i686", "any")
        # if archlinux repository is specified
        if "repo" in value:
            repos = (value["repo"],)
        else:
            repos = ("community-testing", "community", "testing", "extra", "core")
        for arch in archs:
            for repo in repos:
                url = "http://www.archlinux.org/packages/%s/%s/%s/json" % (repo, arch, name)
                logging.debug("Requesting url: %s" % url)
                try:
                    o = urllib.request.urlopen(url)
                    d = json.loads(o.read().decode("utf-8"))
                    v = d["pkgver"]
                    logging.debug("Archlinux version is : %s" % v)
                    return v
                except urllib.error.URLError as e:
                    logging.debug("Archlinux check failed for %s: %s" % (name, e))
        raise abs.error.VersionNotFound("No Archlinux package found")

    def get_version_aur(self, name, value):
        '''Return archlinux user repository version'''
        logging.debug("Get AUR version")
        try:
            url = "http://aur.archlinux.org/rpc.php?type=info&arg=%s" % (name)
            logging.debug("Requesting url: %s" % url)
            o = urllib.request.urlopen(url)
            d = json.loads(o.read().decode("utf-8"))
            v = d["results"]["Version"].rsplit("-")[0]
            logging.debug("AUR version is : %s" % v)
            return v
        except urllib.error.URLError as e:
            raise abs.error.VersionNotFound("AUR check failed for %s: %s" % (name, e))
        assert(False)

    def get_version_saved(self, name, value):
        '''Return local saved version'''
        raise NotImplemented()

    def print_names(self, softwares=None):
        for name, value in self.softwares_generator(softwares):
            print(name)

    def print_versions(self, softwares=None, only_diff=False):
        '''Print last version of registered software'''
        for name, value in self.softwares_generator(softwares):
            # get compare mode
            compare = value.get("compare", "archlinux")
            try:
                # upstream version
                v1 = self.get_version_upstream(name, value)
                if compare == "archlinux":
                    # compare with archlinux pkg
                    v2 = self.get_version_archlinux(name, value)
                    v1 = v1.replace("-", "_")
                    if only_diff and v1 == v2:
                        continue
                elif compare == "aur":
                    v2 = self.get_version_aur(name, value)
                    v1 = v1.replace("-", "_")
                    if only_diff and v1 == v2:
                        continue
                elif compare == "saved":
                    # compare with saved database
                    raise NotImplemented()
                else:
                    # no comparaison
                    # so no print if only_diff
                    if only_diff:
                        continue
                    v2 = None
                self.print_version(name, v1, v2)
            except abs.error.VersionNotFound as e:
                logging.error("%s: Unable to get version: %s" % (name, e))

    def print_version(self, name, v1, v2):
        if sys.stdout.isatty():
            if v2 is None:
                color = '\033[1;33m'
            elif v1 == v2:
                color = '\033[1;32m'
            else:
                color = '\033[1;31m'
            reset = '\033[m'
        else:
            color = ''
            reset = ''
        print("%s[%s] %s" % (color, name, v1), end="")
        if v2 is not None:
            print(" - %s" % v2, end="")
        print(reset)

    def save(self, database):
        '''Save poll result to database'''
        return

# vim:set ts=4 sw=4 et ai:
