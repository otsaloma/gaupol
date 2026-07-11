"""
Volume up: from a mid-level volume, activating should raise the player
volume.
"""

import _video

def setup(application):
    player = _video.load_video(application)
    player.volume = 0.5

def verify(application):
    assert application.player.volume > 0.5
