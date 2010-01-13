# Copyright (C) 2006-2008 Osmo Salomaa
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

"""Reading, writing and storing all configurations.

Module variable '_config' holds the instance of Config used and '_default'
holds the Config instance with the default configuration. 'config_file' is the
path to the configuration file used.

Importing this module will read the default configurations from the spec file.
To read some actual saved configurations, assign a path to the 'config_file'
attribute and call 'read'. All configuration sections are made available as
module variables after reading. See the spec file for a list of those sections,
options, their default values and types.
"""

import gaupol
import os

from .attrdict import ConfigAttrDict
from .config import Config

__all__ = ("Config", "ConfigAttrDict")

config_file = None


def _get_spec_file_ensure(value):
    assert os.path.isfile(value)

@aeidon.deco.contractual
def _get_spec_file():
    """Return the path to the configuration specification file."""

    return os.path.join(aeidon.DATA_DIR, "gaupol.conf.spec")

def _handle_transitions(config):
    """Handle transitions of section and option names."""

    version = config["general"]["version"]
    if not version: return config
    if aeidon.util.compare_versions(version, "0.7.999") == -1:
        print "Ignoring old-style configuration file entirely."
        return Config(None, _get_spec_file())
    return config

def connect_require(obj, section, option):
    assert section in globals()
    assert hasattr(globals()[section], option)

@aeidon.deco.contractual
def connect(obj, section, option):
    """Connect option's signal to object's callback method."""

    signal = "notify::%s" % option
    suffix = signal.replace("::", "_")
    method_name = "_on_conf_%s_%s" % (section, suffix)
    if not hasattr(obj, method_name):
        method_name = method_name[1:]
    method = getattr(obj, method_name)
    globals()[section].connect(signal, method)

def disconnect_require(obj, section, option):
    assert section in globals()
    assert hasattr(globals()[section], option)

@aeidon.deco.contractual
def disconnect(obj, section, option):
    """Disconnect option's signal from object's callback method."""

    signal = "notify::%s" % option
    suffix = signal.replace("::", "_")
    method_name = "_on_conf_%s_%s" % (section, suffix)
    if not hasattr(obj, method_name):
        method_name = method_name[1:]
    method = getattr(obj, method_name)
    globals()[section].disconnect(signal, method)

def read_ensure(value):
    assert "_config" in globals()
    config = globals()["_config"]
    version = aeidon.__version__
    assert general.version == version
    assert config["general"]["version"] == version

@aeidon.deco.contractual
def read():
    """Read configurations from file."""

    try:
        config = Config(config_file, _get_spec_file())
        config = _handle_transitions(config)
    except gaupol.ConfigParseError:
        raise SystemExit(1)
    config["general"]["version"] = aeidon.__version__
    globals()["_config"] = config
    # Create or update attribute dictionaries on the module level for each
    # section to have an attribute-based interface for configurations.
    for key, value in config.items():
        if key in globals():
            globals()[key].replace(value)
        else: # Create a new attribute dictionary.
            globals()[key] = ConfigAttrDict(value)

def read_defaults_ensure(value):
    assert "_defaults" in globals()

@aeidon.deco.contractual
def read_defaults():
    """Read the default values of configuration variables."""

    defaults = Config(None, _get_spec_file())
    defaults = _handle_transitions(defaults)
    defaults["general"]["version"] = aeidon.__version__
    globals()["_defaults"] = defaults

def restore_defaults():
    """Restore the values of configuration variables to their defaults."""

    if "_defaults" not in globals():
        read_defaults()
    defaults = globals()["_defaults"]
    for key, value in defaults.items():
        globals()[key].update(value)
    # Reread defaults to get an unconnected dictionary of defaults values
    # unaffected by any possible changes in attribute dictionaries.
    read_defaults()

def write_ensure(value):
    assert "_config" in globals()
    assert os.path.isfile(config_file)

@aeidon.deco.contractual
def write():
    """Write configurations to file."""

    _config.filename = config_file
    _config.write_to_file()

read()
