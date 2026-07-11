"""
Insert subtitle at video position: with the video paused at the baseline
position, inserting should grow the subtitle count by one.
"""

import _video

def setup(application):
    _video.load_video(application)
    page = application.get_current_page()
    global _count_before
    _count_before = len(page.project.subtitles)

def verify(application):
    page = application.get_current_page()
    assert len(page.project.subtitles) == _count_before + 1
