"""
Configure spell check: activating opens the language dialog. Cancelling it
should leave the spell-check language config unchanged (assumes libspelling is
available).
"""

import gaupol

from gi.repository import Gtk

DIALOG_SCRIPT = [Gtk.ResponseType.CANCEL]

def setup(application):
    global _language_before
    _language_before = gaupol.conf.spell_check.language

def verify(application):
    assert gaupol.conf.spell_check.language == _language_before
