# Copyright (C) 2007 Osmo Salomaa
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

"""Base class for dialog-running classes."""

__all__ = ("Runner",)


class Runner(object):

    """Base class for dialog-running classes.

    Using this base class and its methods to run dialogs allows unit testing to
    override the methods with something that doesn't actually run the dialog,
    but rather returns a response without user interaction.
    """

    def flash_dialog(self, dialog):
        """Run dialog, destroy it and return response."""

        response = dialog.run()
        dialog.destroy()
        return response

    def run_dialog(self, dialog):
        """Run dialog and return response."""

        return dialog.run()
