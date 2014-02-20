# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010,2012 Osmo Salomaa
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

"""Dialog for displaying credits and information."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("AboutDialog",)

_license = """
Gaupol is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

Gaupol is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gaupol. If not, see <http://www.gnu.org/licenses/>.

""".replace("\n", " ").replace("  ", "\n\n").strip()


class AboutDialog(Gtk.AboutDialog):

    """Dialog for displaying credits and information."""

    def __init__(self, parent):
        """Initialize an :class:`AboutDialog` instance."""
        GObject.GObject.__init__(self)
        self.set_transient_for(parent)
        self.set_title(_("About Gaupol"))
        self.set_program_name("Gaupol")
        self.set_version(gaupol.__version__)
        self.set_copyright("Copyright © 2005-2013 Osmo Salomaa")
        self.set_comments(_("Subtitle editor"))
        self.set_license(_license)
        self.set_wrap_license(True)
        self.set_website(gaupol.HOMEPAGE_URL)
        self.set_website_label(_("Gaupol Website"))
        self.set_authors(("Osmo Salomaa <otsaloma@iki.fi>",))
        self.set_artists(("Osmo Salomaa <otsaloma@iki.fi>",))
        self.set_logo_icon_name("gaupol")
        # Translators: This is a special message that shouldn't be translated
        # literally. It is used in the about dialog to give credits to the
        # translators. Thus, you should translate it to your name and email
        # address. You can also include other translators who have contributed
        # to this translation; in that case, please write them on separate
        # lines seperated by newlines (\n).
        self.set_translator_credits(_("translator-credits"))
