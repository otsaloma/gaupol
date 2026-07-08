"""
Convert framerate: activating opens the framerate convert dialog (enabled
because the project has a main file). Cancelling it should leave the subtitle
positions unchanged.
"""

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    page = application.get_current_page()
    global _starts
    _starts = [x.start_seconds for x in page.project.subtitles]

def verify(application):
    page = application.get_current_page()
    starts = [x.start_seconds for x in page.project.subtitles]
    assert starts == _starts
