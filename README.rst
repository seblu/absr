======================
Archlinux Build System
======================

INTRODUCTION
============

The *Archlinux* [#]_ Build System revisted?


SOFTWARES
=========

ATS
---
*ats* (aka Archlinux Tree Sync) is a tool to sync an Archlinux package tree on
a local directory.

it was previously known as abs.

AUC
---
*auc* (aka Archlinux Upstream Checker) is a tool which check upstream program
version against Archlinux/AUR version.

Report can be sent by mail.

ABD
---
*abd* (aka Archlinux Builder Daemon) is a tool which build new version of
packages when they are updated.

ATC
---
*atc* (aka Archlinux Tree Cleaner) is a tool which remove unused files in a
package tree.

AURDOWN
-------
*aurdown* is a tool to download source of an AUR package.

PKGBUILD2JSON
-------------
*pkgbuild2json* is a tool which transform PKGBUILD variables into json.


DEPENDENCIES
============
- Bash 4 [#]_
- Python 3.2 [#]_
- PyXDG [#]_


SOURCES
=======
*ABS* sources are available on github [#]_.


LICENSE
=======
*ABS* is licensied under the term of GPL v2 [#]_.


AUTHOR
======
*ABS* is developped by Sébastien Luttringer.


LINKS
=====
.. [#] http://www.archlinux.org/
.. [#] http://www.gnu.org/software/bash/bash.html
.. [#] http://python.org/download/releases/
.. [#] http://freedesktop.org/wiki/Software/pyxdg
.. [#] https://github.com/seblu/abs/
.. [#] http://www.gnu.org/licenses/gpl-2.0.html
