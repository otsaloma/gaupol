"""
Seek to selection start: with a row selected, seeking should move the
player to that subtitle's start, less the context-length offset (1 s by
default).
"""

import aeidon
import gaupol
import _video

def setup(application):
    _video.load_video(application)
    page = application.get_current_page()
    page.view.select_rows([6])

def verify(application):
    page = application.get_current_page()
    pos = application.player.get_position(aeidon.modes.SECONDS)
    offset = gaupol.conf.video_player.context_length
    target = page.project.subtitles[6].start_seconds - offset
    assert abs(pos - target) < 0.3
