"""
Insert subtitles: with row 0 selected and "Above selection" forced,
accepting the dialog should grow the subtitle count by one and shift the
original first subtitle to row 1.
"""

import gaupol

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.OK]

def setup(application):
    gaupol.conf.subtitle_insert.above = True
    page = application.get_current_page()
    page.view.select_rows([0])
    global _count_before, _text_before
    _count_before = len(page.project.subtitles)
    _text_before = page.project.subtitles[0].main_text

def verify(application):
    page = application.get_current_page()
    subtitles = page.project.subtitles
    assert len(subtitles) == _count_before + 1
    assert not subtitles[0].main_text
    assert subtitles[1].main_text == _text_before
