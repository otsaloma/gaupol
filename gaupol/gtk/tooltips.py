# Copyright (C) 2007 Osmo Salomaa
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


"""Tooltips with markup labels."""


import gtk

from gaupol.gtk import util


class Tooltips(gtk.Tooltips):

    """Tooltips with markup labels."""

    @util.asserted_return
    def __init__(self):

        # pylint: disable-msg=E1101
        gtk.Tooltips.__init__(self)
        self.force_window()
        label = self.tip_label
        assert label is not None
        label.set_use_markup(True)
        callback = self._on_label_notify_use_markup
        label.connect("notify::use-markup", callback)

    def _on_label_notify_use_markup(self, label, *args):
        """Reset label to use markup."""

        label.set_use_markup(True)
