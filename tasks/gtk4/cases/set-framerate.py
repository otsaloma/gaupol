"""
Set framerate: activating with a different framerate as target should
change the current project's framerate (enabled because the project has a main
file).

This is a radio action, so the harness activates it with ACTIVATE_TARGET (the
enum member name of the framerate to switch to, chosen different from the
current).
"""

import aeidon
import gaupol

def ACTIVATE_TARGET(application):
    current = application.get_current_page().project.framerate
    if current != aeidon.framerates.FPS_25_000:
        return "FPS_25_000"
    return "FPS_30_000"

def setup(application):
    global _framerate_before, _conf_before
    _framerate_before = application.get_current_page().project.framerate
    _conf_before = gaupol.conf.editor.framerate

def verify(application):
    page = application.get_current_page()
    try:
        assert page.project.framerate != _framerate_before
    finally:
        gaupol.conf.editor.framerate = _conf_before
