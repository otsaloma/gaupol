"""
Set start from video position: with the video paused at 10 s and a single
row selected, the subtitle's start should move to the player position. Row 4
(9.606 --> 13.736) is used so the new start stays before its end.
"""

import aeidon
import _video

def setup(application):
    _video.load_video(application)
    page = application.get_current_page()
    page.view.select_rows([4])
    global _start_before
    _start_before = page.project.subtitles[4].start_seconds

def verify(application):
    page = application.get_current_page()
    pos = application.player.get_position(aeidon.modes.SECONDS)
    start = page.project.subtitles[4].start_seconds
    assert abs(start - pos) < 0.2
    assert abs(start - _start_before) > 0.1
