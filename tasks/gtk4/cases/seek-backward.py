"""
Seek backward: with the video paused at 10 s and a 5 s seek length, seeking
should move the position back by roughly that amount.
"""

import aeidon
import gaupol
import _video

def setup(application):
    _video.load_video(application)
    gaupol.conf.video_player.seek_length = 5.0
    global _pos_before
    _pos_before = application.player.get_position(aeidon.modes.SECONDS)

def verify(application):
    pos = application.player.get_position(aeidon.modes.SECONDS)
    assert abs(pos - (_pos_before - 5.0)) < 0.6
