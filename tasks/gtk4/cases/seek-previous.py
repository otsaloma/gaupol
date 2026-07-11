"""
Seek previous: with the video paused at 10 s, seeking should jump to the
start of the last subtitle that ends before that position (row 3, at 4.635 s).
"""

import aeidon
import _video

def setup(application):
    _video.load_video(application)

def verify(application):
    page = application.get_current_page()
    pos = application.player.get_position(aeidon.modes.SECONDS)
    target = page.project.subtitles[3].start_seconds
    assert abs(pos - target) < 0.3
