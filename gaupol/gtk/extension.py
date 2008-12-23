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

    _conf_spec_file = None

    def read_config(self):
        """Read configurations from file according to spec_file.

        The configurations are read from the global gaupol configuration file
        according to the extension-specific specification file 'spec_file'.
        Options are stored as global variables under gaupol.gtk.conf and are
        written to the global configuration file automatically.
        """
        if self._conf_spec_file is None: return
        config_file = gaupol.gtk.conf.config_file
        config = gaupol.gtk.Config(config_file, self._conf_spec_file, False)
        dummy = gaupol.gtk.Config(None, self._conf_spec_file, False)
        config_sections = set(config["extensions"].keys())
        dummy_sections = set(dummy["extensions"].keys())
        for section in (config_sections - dummy_sections):
            # Remove all sections not in the spec file,
            # which should mostly be sections of other extensions.
            del config["extensions"][section]
        gaupol.gtk.conf.extensions.update(config["extensions"])

    def setup(self, application):
        """Setup extension for use with application.

        This method is called every time when the extension is associated with
        the application, i.e. both when it is manually activated and also every
        time right after application start.
        """
        pass

    def show_help(self):
        """Show documentation on using extension.

        Subclasses can override this to, for example, launch a web browser with
        gaupol.util.browse_url to view HTML documentation.
        """
        raise NotImplementedError

    def show_preferences_dialog(self, parent):
        """Show a preferences dialog for configuring extension.

        parent is the parent window that the dialog can be centered on.
        """
        raise NotImplementedError

    def teardown(self, application):
        """End use of extension with application.

        This method is called every time when the extension is unassociated
        with the application, i.e. both when it is manually deactivated and
        also every time right before application exit.
        """
        pass

    def update(self, application, page):
        """Update state of extension for application and active page.

        The main purpose of this method is to update sensitivities of UI
        manager actions associated with this extension.
        """
        pass
