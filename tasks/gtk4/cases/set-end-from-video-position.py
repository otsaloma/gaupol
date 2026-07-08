"""
Set end from video position: with the video paused at 10 s and a single row
selected, the subtitle's end should move to the player position. Row 4 (9.606
--> 13.736) is used so the new end stays after its start.
"""

import aeidon
import _video

def setup(application):
    _video.load_video(application)
    page = application.get_current_page()
    page.view.select_rows([4])
    global _end_before
    _end_before = page.project.subtitles[4].end_seconds

def verify(application):
    page = application.get_current_page()
    pos = application.player.get_position(aeidon.modes.SECONDS)
    end = page.project.subtitles[4].end_seconds
    assert abs(end - pos) < 0.2
    assert abs(end - _end_before) > 0.1
