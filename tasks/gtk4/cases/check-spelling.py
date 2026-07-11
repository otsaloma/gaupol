"""
Check spelling: with the spell-check language set to "en", activating opens
the spell-check dialog. Closing it should leave the subtitles unchanged
(assumes an "en" dictionary is available).
"""

import gaupol

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CLOSE]

def setup(application):
    gaupol.conf.spell_check.language = "en"
    page = application.get_current_page()
    global _count_before
    _count_before = len(page.project.subtitles)

def verify(application):
    page = application.get_current_page()
    assert len(page.project.subtitles) == _count_before
