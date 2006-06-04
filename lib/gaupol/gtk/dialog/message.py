# Copyright (C) 2005 Osmo Salomaa
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


"""Base classes for message dialogs."""


import gtk


FLAGS = gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT


class ErrorDialog(gtk.MessageDialog):

    """Base class for error dialogs."""

    def __init__(self, parent, title, message):

        gtk.MessageDialog.__init__(
            self,
            parent,
            FLAGS,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_OK,
            title
        )

        self.format_secondary_text(message)


class InfoDialog(gtk.MessageDialog):

    """Base class for info dialogs."""

    def __init__(self, parent, title, message):

        gtk.MessageDialog.__init__(
            self,
            parent,
            FLAGS,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            title
        )

        self.format_secondary_text(message)


class QuestionDialog(gtk.MessageDialog):

    """Base class for question dialogs."""

    def __init__(self, parent, title, message):

        gtk.MessageDialog.__init__(
            self,
            parent,
            FLAGS,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_NONE,
            title
        )

        self.format_secondary_text(message)


class WarningDialog(gtk.MessageDialog):

    """Base class for warning dialogs."""

    def __init__(self, parent, title, message):

        gtk.MessageDialog.__init__(
            self,
            parent,
            FLAGS,
            gtk.MESSAGE_WARNING,
            gtk.BUTTONS_NONE,
            title
        )

        self.format_secondary_text(message)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestDialog(Test):

        def test_init(self):

            args = gtk.Window(), 'test', 'test'
            ErrorDialog(*args)
            InfoDialog(*args)
            QuestionDialog(*args)
            WarningDialog(*args)

    TestDialog().run()
