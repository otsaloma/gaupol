"""
Split project: activating opens the split dialog (enabled because the
project has more than one subtitle). Cancelling it should leave the open pages
untouched.
"""

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    global _count_before
    _count_before = len(application.pages)

def verify(application):
    assert len(application.pages) == _count_before
