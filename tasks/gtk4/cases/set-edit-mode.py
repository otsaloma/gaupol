"""
Set edit mode: activating with the opposite mode as target should switch
the current page between time and frame based positions.

This is a radio action, so the harness activates it with ACTIVATE_TARGET (the
enum member name of the mode to switch to, chosen opposite to the current).
"""

import aeidon
import gaupol

def ACTIVATE_TARGET(application):
    mode = application.get_current_page().edit_mode
    return "FRAME" if mode == aeidon.modes.TIME else "TIME"

def setup(application):
    global _mode_before, _conf_before
    _mode_before = application.get_current_page().edit_mode
    _conf_before = gaupol.conf.editor.mode

def verify(application):
    page = application.get_current_page()
    try:
        assert page.edit_mode != _mode_before
    finally:
        gaupol.conf.editor.mode = _conf_before
