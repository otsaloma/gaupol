# -*- coding: utf-8 -*-

# Copyright (C) 2008 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Separate object that can be activated and deactivated during runtime."""

__all__ = ("Extension",)


class Extension:

    """Separate object that can be activated and deactivated during runtime."""

    def setup(self, application):
        """
        Setup extension for use with `application`.

        This method is called every time the extension is associated with
        `application`, i.e. both when it is manually activated and also every
        time right after `application` start.
        """
        pass

    def show_help(self):
        """
        Show documentation on using extension.

        Subclasses can override this to, for example, launch a web browser with
        :func:`gaupol.util.show_uri` to view HTML documentation.
        """
        raise NotImplementedError

    def show_preferences_dialog(self, parent):
        """
        Show a preferences dialog for configuring extension.

        `parent` is the parent window that the dialog can be centered on.
        """
        raise NotImplementedError

    def teardown(self, application):
        """
        End use of extension with `application`.

        This method is called every time the extension is unassociated with
        `application`, i.e. both when it is manually deactivated and also every
        time right before `application` exit.
        """
        pass

    def update(self, application, page):
        """
        Update state of extension for `application` and active `page`.

        The main purpose of this method is to update sensitivities of UI
        manager actions associated with this extension.
        """
        pass
