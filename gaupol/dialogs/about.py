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

"""Dialog for displaying credits and information."""

import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("AboutDialog",)


class AboutDialog(Gtk.AboutDialog):

    """Dialog for displaying credits and information."""

    def __init__(self, parent):
        """Initialize an :class:`AboutDialog` instance."""
        GObject.GObject.__init__(self)
        self.set_title(_("About Gaupol"))
        self.set_transient_for(parent)
        self.set_artists(("Osmo Salomaa <otsaloma@iki.fi>",))
        self.set_authors(("Osmo Salomaa <otsaloma@iki.fi>",))
        self.set_comments(_("Subtitle editor"))
        self.set_copyright("Copyright © 2005–2020 Osmo Salomaa")
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_logo_icon_name("io.otsaloma.gaupol")
        self.set_program_name("Gaupol")
        # TRANSLATORS: This is a special message that shouldn't be translated
        # literally. It is used in the about dialog to give credits to the
        # translators. Thus, you should translate it to your name and email
        # address. You can also include other translators who have contributed
        # to this translation; in that case, please write them on separate
        # lines seperated by newlines (\n).
        self.set_translator_credits(_("translator-credits"))
        self.set_version(gaupol.__version__)
        self.set_website(gaupol.HOMEPAGE_URL)
        self.set_website_label(_("Gaupol Website"))
        self.set_wrap_license(True)
