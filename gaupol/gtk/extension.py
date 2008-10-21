# Copyright (C) 2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Separate object that can be activated and deactivated during runtime."""

import gaupol

__all__ = ("Extension",)


class Extension(object):

    """Separate object that can be activated and deactivated during runtime."""

    spec_file = None

    def read_config(self):
        """Read configurations from file according to spec_file.

        The configurations are read from the global gaupol configuration file
        according to the extension-specific specification file 'spec_file'.
        Options are stored as global variables under gaupol.gtk.conf and are
        written to the global configuration file automatically.
        """
        conf = gaupol.gtk.conf.extensions
        config_file = gaupol.gtk.conf.config_file
        config = gaupol.gtk.Config(config_file, self.spec_file)
        config = config["extensions"]
        # Create or update AttrDicts at conf module level.
        for key, value in config.items():
            if hasattr(gaupol.gtk.conf.extensions, key):
                getattr(conf, key).update(value)
            else: # Create AttrDict.
                setattr(conf, key, gaupol.AttrDict(value))

    def setup(self, application):
        """Setup extension for use with application.

        This method is called every time when the extension if associated with
        the application, i.e. both when it is manually activated and also every
        time right after application start.
        """
        pass

    def teardown(self, application):
        """End use of extension with application.

        This method is called every time when the extension is unassociated
        with the application, i.e. both when it is manually deactivated and
        also every time right before application exit.
        """
        pass

    def update(self, application, page):
        """Update state of plugin for application and active page.

        The main purpose of this method is to update sensitivities of UI
        manager actions associated with this extension.
        """
        pass
