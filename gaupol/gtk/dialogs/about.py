# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Dialog for displaying credits and information.

Module variables:

    _LICENSE:     Unwrapped license notice
    _LOGO:        Path to logo file
    _TRANSLATORS: Translators' email adresses
"""


import os
from gettext import gettext as _

import gtk

from gaupol import urls, util, __version__
from gaupol.gtk import paths


_LOGO = os.path.join(paths.DATA_DIR, "icons", "logo.png")

# Translators: This is a special message that shouldn't be translated
# literally. It is used in the about dialog to give credits to the translators.
# Thus, you should translate it to your name and email address.  You can also
# include other translators who have contributed to this translation; in that
# case, please write them on separate lines seperated by newlines (\n).
_TRANSLATORS = _("translator-credits")

_LICENSE = \
'Gaupol is free software; you can redistribute it and/or modify it under '   \
'the terms of the GNU General Public License as published by the Free '      \
'Software Foundation; either version 2 of the License, or (at your option) ' \
'any later version.\n\n' \
'Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY ' \
'WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS ' \
'FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more '    \
'details.\n\n' \
'You should have received a copy of the GNU General Public License along '   \
'with Gaupol; if not, write to the Free Software Foundation, Inc., 51 '      \
'Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.'


class AboutDialog(gtk.AboutDialog):

    """Dialog for displaying credits and information."""

    def __init__(self, parent):

        gtk.AboutDialog.__init__(self)
        gtk.about_dialog_set_url_hook(self._on_url_clicked)
        self.set_wrap_license(True)
        self.set_transient_for(parent)

        self.set_name("Gaupol")
        self.set_version(__version__)
        self.set_copyright(u"Copyright \xa9 2005-2007 Osmo Salomaa")
        self.set_comments(_("Subtitle editor"))
        self.set_website(urls.HOMEPAGE)
        self.set_website_label(urls.HOMEPAGE)
        self.set_authors(["Osmo Salomaa <otsaloma@cc.hut.fi>"])
        self.set_artists(["Osmo Salomaa <otsaloma@cc.hut.fi>"])
        self.set_translator_credits(_TRANSLATORS)
        self.set_license(_LICENSE)
        self.set_logo(gtk.gdk.pixbuf_new_from_file(_LOGO))

    def _on_url_clicked(self, *args):
        """Open website in a web browser."""

        util.browse_url(urls.HOMEPAGE)
