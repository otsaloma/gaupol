# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

"""Message dialog classes."""

from gi.repository import Gtk

__all__ = ("ErrorDialog", "InfoDialog", "QuestionDialog", "WarningDialog")


class ErrorDialog(Gtk.MessageDialog):

    """Base class for error dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize an :class:`ErrorDialog` instance."""
        Gtk.MessageDialog.__init__(self,
                                   transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.NONE,
                                   text=title)

        if message is not None:
            self.format_secondary_text(message)


class InfoDialog(Gtk.MessageDialog):

    """Base class for info dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize an :class:`InfoDialog` instance."""
        Gtk.MessageDialog.__init__(self,
                                   transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.NONE,
                                   text=title)

        if message is not None:
            self.format_secondary_text(message)


class QuestionDialog(Gtk.MessageDialog):

    """Base class for question dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize a :class:`QuestionDialog` instance."""
        Gtk.MessageDialog.__init__(self,
                                   transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.NONE,
                                   text=title)

        if message is not None:
            self.format_secondary_text(message)


class WarningDialog(Gtk.MessageDialog):

    """Base class for warning dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize a :class:`WarningDialog` instance."""
        Gtk.MessageDialog.__init__(self,
                                   transient_for=parent,
                                   modal=True,
                                   destroy_with_parent=True,
                                   message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.NONE,
                                   text=title)

        if message is not None:
            self.format_secondary_text(message)
