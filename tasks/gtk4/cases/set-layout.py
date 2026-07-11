"""
Set layout: activating with the opposite orientation as target should flip
the application window layout. A video is loaded first, since the action is
only enabled once a player exists.

This is a radio action, so the harness activates it with ACTIVATE_TARGET (the
enum member name of the orientation to switch to, chosen opposite to the
current).
"""

import gaupol
import _video

def ACTIVATE_TARGET(application):
    layout = gaupol.conf.application_window.layout
    if layout == gaupol.orientation.VERTICAL:
        return "HORIZONTAL"
    return "VERTICAL"

def setup(application):
    _video.load_video(application)
    global _layout_before
    _layout_before = gaupol.conf.application_window.layout

def verify(application):
    try:
        assert gaupol.conf.application_window.layout != _layout_before
    finally:
        gaupol.conf.application_window.layout = _layout_before
