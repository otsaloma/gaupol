"""
Save main document as: activating opens a save file chooser. Cancelling it
should leave the project's main file (and its path) unchanged.
"""

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    page = application.get_current_page()
    global _path
    _path = page.project.main_file.path

def verify(application):
    page = application.get_current_page()
    assert page.project.main_file.path == _path
