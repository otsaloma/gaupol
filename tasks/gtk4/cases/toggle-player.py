"""
Toggle player: with the player loaded and its box visible, activating
should hide the player box (flip its visibility).
"""

import _video

def setup(application):
    _video.load_video(application)
    global _visible_before
    _visible_before = application.player_box.get_visible()

def verify(application):
    assert application.player_box.get_visible() != _visible_before
