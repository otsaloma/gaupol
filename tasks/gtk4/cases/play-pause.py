"""
Play/pause: from the paused baseline, activating should toggle the player
into the playing state.
"""

import _video

def setup(application):
    player = _video.load_video(application)
    global _playing_before
    _playing_before = player.is_playing()

def verify(application):
    assert application.player.is_playing() != _playing_before
