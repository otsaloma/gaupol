# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Dialog to display information about Gaupol."""


from gettext import gettext as _

import gtk

from gaupol.base.util import wwwlib
from gaupol           import __version__


name     = 'Gaupol'
copyrght = u'Copyright \xa9 2005 Osmo Salomaa'
comments = _('Subtitle editor')
website  = 'http://home.gna.org/gaupol'
authors  = ['Osmo Salomaa <otsaloma@cc.hut.fi>']

# Translators: This is a special message that shouldn't be translated
# literally. It is used in the about dialog to give credits to the translators.
# Thus, you should translate it to your name and email address.  You can also
# include other translators who have contributed to this translation; in that
# case, please write them on separate lines seperated by newlines (\n).
translators = _('translator-credits')

lisense = \
'''Gaupol is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Gaupol is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gaupol; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA'''


class AboutDialog(gtk.AboutDialog):

    """Dialog to display application information."""

    def __init__(self, parent):

        gtk.AboutDialog.__init__(self)

        self.set_name(name)
        self.set_version(__version__)
        self.set_copyright(copyrght)
        self.set_comments(comments)
        self.set_license(lisense)

        gtk.about_dialog_set_url_hook(self._on_url_clicked)
        self.set_website_label(website)

        self.set_authors(authors)
        if translators != 'translator-credits':
            self.set_translator_credits(translators)

        self.set_transient_for(parent)

    def _on_url_clicked(self, *args):
        """Open website in browser when user clicks on URL."""

        wwwlib.open_url(website)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestAboutDialog(Test):

        def test_init(self):

            AboutDialog(gtk.Window())

    TestAboutDialog().run()
