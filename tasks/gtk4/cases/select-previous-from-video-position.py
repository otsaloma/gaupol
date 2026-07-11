"""
Select previous from video position: with the video paused at 10 s,
selecting should land on the last subtitle that starts before that position
(row 4, which starts at 9.606 s).
"""

import _video

def setup(application):
    _video.load_video(application)

def verify(application):
    page = application.get_current_page()
    assert page.view.get_selected_rows() == (4,)
