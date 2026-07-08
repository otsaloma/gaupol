"""
Save translation document as: activating opens a save file chooser.
Cancelling it should leave the project without a translation file.
"""

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    pass

def verify(application):
    page = application.get_current_page()
    assert page.project.tran_file is None
