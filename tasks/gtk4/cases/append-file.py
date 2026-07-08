"""
Append file: activating opens a file chooser to append subtitles.
Cancelling it should leave the subtitle count unchanged.
"""

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    page = application.get_current_page()
    global _count_before
    _count_before = len(page.project.subtitles)

def verify(application):
    page = application.get_current_page()
    assert len(page.project.subtitles) == _count_before
