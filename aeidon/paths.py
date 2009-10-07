# Copyright (C) 2005-2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Paths to files and directories used.

:var CONFIG_HOME_DIR: Path to the user's local configuration directory
:var DATA_DIR: Path to the global data directory
:var DATA_HOME_DIR: Path to the user's local data directory
:var LOCALE_DIR: Path to the global locale directory

Of the directory attributes defined in this module, :data:`CONFIG_HOME_DIR` and
:data:`DATA_HOME_DIR` depend only on the platform used; on non-Windows systems
they adher to freedesktop.org_'s `XDG Base Directory Specification`_ and on
Windows they are both under the ``%APPDATA%`` directory.

The values of :data:`DATA_DIR` and :data:`LOCALE_DIR` as defined in this file
depend on whether Gaupol is run from the source directory or from a frozen
``py2exe`` installation. In other cases, i.e. a proper installation on a
non-Windows system, the values of these attributes are overwritten during
installation based on arguments given to ``setup.py``.

.. _freedesktop.org: http://www.freedesktop.org/
.. _XDG Base Directory Specification:
   http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""

import aeidon
import os
import shutil
import sys

__all__ = ("CONFIG_HOME_DIR", "DATA_DIR", "DATA_HOME_DIR", "LOCALE_DIR",)


def get_config_home_directory():
    """Return path to the user's configuration directory."""
    if sys.platform == "win32":
        return get_config_home_directory_windows()
    return get_config_home_directory_xdg()

def get_config_home_directory_windows():
    """Return path to the user's configuration directory on Windows."""
    directory = os.path.expanduser("~")
    directory = os.environ.get("APPDATA", directory)
    directory = os.path.join(directory, "Gaupol")
    return os.path.abspath(directory)

def get_config_home_directory_xdg():
    """Return path to the user's XDG configuration directory."""
    directory = os.path.join(os.path.expanduser("~"), ".config")
    directory = os.environ.get("XDG_CONFIG_HOME", directory)
    directory = os.path.join(directory, "gaupol")
    return os.path.abspath(directory)

def get_data_directory():
    """Return path to the global data directory."""
    if hasattr(sys, "frozen"):
        return get_data_directory_py2exe()
    return get_data_directory_source()

def get_data_directory_py2exe():
    """Return path to the global data directory on ``py2exe``."""
    directory = os.path.dirname(sys.argv[0])
    directory = os.path.join(directory, "share", "gaupol")
    return os.path.abspath(directory)

def get_data_directory_source():
    """Return path to the global data directory when running from source."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(directory, ".."))
    directory = os.path.join(directory, "data")
    return os.path.abspath(directory)

def get_data_home_directory():
    """Return path to the user's data directory."""
    if sys.platform == "win32":
        return get_data_home_directory_windows()
    return get_data_home_directory_xdg()

def get_data_home_directory_windows():
    """Return path to the user's data directory on Windows."""
    directory = os.path.expanduser("~")
    directory = os.environ.get("APPDATA", directory)
    directory = os.path.join(directory, "Gaupol")
    return os.path.abspath(directory)

def get_data_home_directory_xdg():
    """Return path to the user's XDG data directory."""
    directory = os.path.join(os.path.expanduser("~"), ".local", "share")
    directory = os.environ.get("XDG_DATA_HOME", directory)
    directory = os.path.join(directory, "gaupol")
    return os.path.abspath(directory)

def get_locale_directory():
    """Return path to the locale directory."""
    if hasattr(sys, "frozen"):
        return get_locale_directory_py2exe()
    return get_locale_directory_source()

def get_locale_directory_py2exe():
    """Return path to the locale directory on ``py2exe``."""
    directory = os.path.dirname(sys.argv[0])
    directory = os.path.join(directory, "share", "locale")
    return os.path.abspath(directory)

def get_locale_directory_source():
    """Return path to the locale directory when running from source."""
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.abspath(os.path.join(directory, ".."))
    directory = os.path.join(directory, "locale")
    return os.path.abspath(directory)

def get_obsolete_profile_directory():
    """Return path to the profile directory used prior to version 0.14."""
    directory = os.path.expanduser("~")
    directory = os.path.join(directory, ".gaupol")
    return os.path.abspath(directory)

def xdg_copy_config_files():
    """Copy config files from ``OBSOLETE_HOME_DIR`` to ``CONFIG_HOME_DIR``."""
    dst_directory = os.path.join(CONFIG_HOME_DIR, "patterns")
    try: aeidon.util.makedirs(CONFIG_HOME_DIR)
    except (IOError, OSError): pass
    # $XDG_CONFIG_HOME_DIR/patterns/*.conf
    src_directory = os.path.join(OBSOLETE_HOME_DIR, "patterns")
    try: files = os.listdir(src_directory)
    except (IOError, OSError): files = []
    files = [x for x in files if x.endswith(".conf")]
    for basename in files:
        src = os.path.join(src_directory, basename)
        dst = os.path.join(dst_directory, basename)
        try: shutil.copyfile(src, dst)
        except (IOError, OSError): pass
    # $XDG_CONFIG_HOME_DIR/gaupol.gtk.conf
    src = os.path.join(OBSOLETE_HOME_DIR, "gaupol.gtk.conf")
    dst = os.path.join(CONFIG_HOME_DIR, "gaupol.gtk.conf")
    try: shutil.copyfile(src, dst)
    except (IOError, OSError): pass
    # $XDG_CONFIG_HOME_DIR/search/
    # $XDG_CONFIG_HOME_DIR/spell-check/
    for basename in ("search", "spell-check"):
        src = os.path.join(OBSOLETE_HOME_DIR, basename)
        dst = os.path.join(CONFIG_HOME_DIR, basename)
        try: shutil.copytree(src, dst)
        except (IOError, OSError): pass
    path = os.path.join(OBSOLETE_HOME_DIR, "README")
    aeidon.util.writelines(path, (
        "This directory is obsolete since gaupol version 0.14",
        "and can be safely removed."))

def xdg_copy_data_files():
    """Copy data files from ``OBSOLETE_HOME_DIR`` to ``DATA_HOME_DIR``."""
    # $XDG_DATA_HOME/extensions/
    # $XDG_DATA_HOME/headers/
    for basename in ("extensions", "headers"):
        src = os.path.join(OBSOLETE_HOME_DIR, basename)
        dst = os.path.join(DATA_HOME_DIR, basename)
        try: shutil.copytree(src, dst)
        except (IOError, OSError): pass
    # $XDG_DATA_HOME/patterns/
    dst_directory = os.path.join(DATA_HOME_DIR, "patterns")
    try: aeidon.util.makedirs(dst_directory)
    except (IOError, OSError): pass
    src_directory = os.path.join(OBSOLETE_HOME_DIR, "patterns")
    try: files = os.listdir(src_directory)
    except (IOError, OSError): files = []
    files = [x for x in files if x.endswith((".capitalization",
                                             ".common-error",
                                             ".hearing-impaired",
                                             ".line-break"))]

    for basename in files:
        src = os.path.join(src_directory, basename)
        dst = os.path.join(dst_directory, basename)
        try: shutil.copyfile(src, dst)
        except (IOError, OSError): pass
    path = os.path.join(OBSOLETE_HOME_DIR, "README")
    aeidon.util.writelines(path, (
        "This directory is obsolete since gaupol version 0.14",
        "and can be safely removed."))

def xdg_copy_if_applicable():
    """Copy config and data files to XDG folders if applicable."""
    if (os.path.isdir(OBSOLETE_HOME_DIR)
        and sys.platform != "win32"):
        if not os.path.isdir(CONFIG_HOME_DIR):
            xdg_copy_config_files()
        if not os.path.isdir(DATA_HOME_DIR):
            xdg_copy_data_files()


CONFIG_HOME_DIR = get_config_home_directory()
DATA_DIR = get_data_directory()
DATA_HOME_DIR = get_data_home_directory()
LOCALE_DIR = get_locale_directory()
OBSOLETE_HOME_DIR = get_obsolete_profile_directory()
