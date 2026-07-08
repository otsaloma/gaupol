"""
Play selection: with a row selected, activating should start playing the
selected segment.
"""

import _video

def setup(application):
    _video.load_video(application)
    page = application.get_current_page()
    page.view.select_rows([4])

def verify(application):
    assert application.player.is_playing()
