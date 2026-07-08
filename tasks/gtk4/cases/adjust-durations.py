"""
Adjust durations: activating opens the duration adjust dialog. Cancelling
it should leave the subtitles unchanged.
"""

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    page = application.get_current_page()
    global _durations
    _durations = [x.duration_seconds for x in page.project.subtitles]

def verify(application):
    page = application.get_current_page()
    durations = [x.duration_seconds for x in page.project.subtitles]
    assert durations == _durations
