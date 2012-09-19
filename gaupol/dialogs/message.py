# -*- coding: utf-8 -*-

# Copyright (C) 2005-2007,2010,2012 Osmo Salomaa
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

"""Message dialog classes."""

from gi.repository import Gtk

__all__ = ("ErrorDialog", "InfoDialog", "QuestionDialog", "WarningDialog")


class ErrorDialog(Gtk.MessageDialog):

    """Base class for error dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize an :class:`ErrorDialog` object."""
        Gtk.MessageDialog.__init__(self,
                                   parent=parent,
                                   flags=(Gtk.DialogFlags.MODAL |
                                          Gtk.DialogFlags.DESTROY_WITH_PARENT),

                                   type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.NONE,
                                   message_format=title)

        if message is not None:
            self.format_secondary_text(message)


class InfoDialog(Gtk.MessageDialog):

    """Base class for info dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize an :class:`InfoDialog` object."""
        Gtk.MessageDialog.__init__(self,
                                   parent=parent,
                                   flags=(Gtk.DialogFlags.MODAL |
                                          Gtk.DialogFlags.DESTROY_WITH_PARENT),

                                   type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.NONE,
                                   message_format=title)

        if message is not None:
            self.format_secondary_text(message)


class QuestionDialog(Gtk.MessageDialog):

    """Base class for question dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize a :class:`QuestionDialog` object."""
        Gtk.MessageDialog.__init__(self,
                                   parent=parent,
                                   flags=(Gtk.DialogFlags.MODAL |
                                          Gtk.DialogFlags.DESTROY_WITH_PARENT),

                                   type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.NONE,
                                   message_format=title)

        if message is not None:
            self.format_secondary_text(message)


class WarningDialog(Gtk.MessageDialog):

    """Base class for warning dialogs."""

    def __init__(self, parent, title, message=None):
        """Initialize a :class:`WarningDialog` object."""
        Gtk.MessageDialog.__init__(self,
                                   parent=parent,
                                   flags=(Gtk.DialogFlags.MODAL |
                                          Gtk.DialogFlags.DESTROY_WITH_PARENT),

                                   type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.NONE,
                                   message_format=title)

        if message is not None:
            self.format_secondary_text(message)
