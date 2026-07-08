"""
Select next from video position: with the video paused at 10 s, selecting
should land on the first subtitle that starts after that position (row 5, which
starts at 14.445 s).
"""

import _video

def setup(application):
    _video.load_video(application)

def verify(application):
    page = application.get_current_page()
    assert page.view.get_selected_rows() == (5,)
