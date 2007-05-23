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


"""Reading, writing and storing all configurations.

Module variables:
 * config_file: Path to the configuration file

Importing this module will read the default configurations from the spec file.
To read some actual saved configurations, assign a path to the 'config_file'
attribute and call 'read'. All configuration sections are made available as
module variables. See the spec file for a list of those sections, options,
their default values and types.
"""


import os

from gaupol import paths, util, __version__
from gaupol.gtk.errors import ConfigParseError
from .config import Config
from .container import Container


config_file = None


def _handle_transitions(config):
    """Handle transitions of section and option names."""

    version = config["general"]["version"]
    if version is not None:
        if util.compare_versions(version, "0.7.999") == -1:
            print "Ignoring old-style configuration file entirely."
            spec_file = os.path.join(paths.DATA_DIR, "conf.spec")
            return Config(None, spec_file)
    return config

def _translate_nones(config):
    """Translate Nones to a False value of appropriate type."""

    config.translate_none("editor", "font", "")
    config.translate_none("file", "directory", "")
    config.translate_none("file", "encoding", "")
    config.translate_none("preview", "custom_command", "")

def connect_require(obj, section, option):
    assert section in globals()
    assert hasattr(globals()[section], option)

@util.contractual
def connect(obj, section, option):
    """Connect option's signal to object's callback method."""

    signal = "notify::%s" % option
    suffix = signal.replace("::", "_")
    method_name = "_on_conf_%s_%s" % (section, suffix)
    if not hasattr(obj, method_name):
        method_name = method_name[1:]
    method = getattr(obj, method_name)
    globals()[section].connect(signal, method)

def read_ensure(value):
    assert "_config" in globals()

@util.contractual
def read():
    """Read configurations from file."""

    try:
        spec_file = os.path.join(paths.DATA_DIR, "conf.spec")
        config = Config(config_file, spec_file)
        config = _handle_transitions(config)
    except ConfigParseError:
        raise SystemExit(1)
    _translate_nones(config)
    config["general"]["version"] = __version__
    globals()["_config"] = config
    for key, value in config.items():
        globals()[key] = Container(value)

def write_ensure(value):
    assert "_config" in globals()
    assert os.path.isfile(config_file)

@util.contractual
def write():
    """Write configurations to file."""

    # pylint: disable-msg=E0602
    _config.filename = config_file
    _config.write_to_file()

read()
