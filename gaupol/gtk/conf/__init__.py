# Copyright (C) 2006-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Configuration.

Module variables:

    _CONFIG: Instance of Config used

The configuration file is read and validated upon import. All configuration
sections are made available as module variables. See the spec file for what
these sections and options are.
"""


import os

from gaupol import util, __version__
from gaupol.gtk import paths
from gaupol.gtk.errors import ConfigParseError
from .wrappers import Config, Container


__all__ = ["Config", "Container"]

_CONFIG = None


def _translate_nones(config):
    """Translate Nones to a False value of proper type."""

    options = (
        ("editor" , "font"          , ""),
        ("file"   , "directory"     , ""),
        ("file"   , "encoding"      , ""),
        ("preview", "custom_command", ""),)
    for section, option, value in options:
        if config[section][option] is None:
            config[section][option] = value
            config[section].defaults.append(option)

def connect(obj, section, option):
    """Connect option's signal to object's callback method."""

    signal = "notify::%s" % option
    method_name = "_on_conf_%s_%s" % (section, signal.replace("::", "_"))
    if not hasattr(obj, method_name):
        method_name = method_name[1:]
    method = getattr(obj, method_name)
    eval(section).connect(signal, method)

def read():
    """Read configurations from file."""

    try:
        config = Config(paths.CONFIG_FILE, paths.SPEC_FILE)
    except ConfigParseError:
        raise SystemExit(1)
    version = config["general"]["version"]
    if version is not None:
        if util.compare_versions(version, "0.7.999") == -1:
            print "Ignoring old-style configuration file entirely."
            config = Config(None, paths.SPEC_FILE)
    config["general"]["version"] = __version__
    _translate_nones(config)

    globals()["_CONFIG"] = config
    for key, value in config.items():
        globals()[key] = Container(value)

def write():
    """Write configurations to file."""

    # pylint: disable-msg=E1101
    _CONFIG.filename = paths.CONFIG_FILE
    _CONFIG.write_to_file()


read()
