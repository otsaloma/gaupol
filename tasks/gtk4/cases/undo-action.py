"""
Undo action: after removing a subtitle in setup, undoing should restore the
original subtitle count and text.
"""

def setup(application):
    page = application.get_current_page()
    global _count_before, _first_text
    _count_before = len(page.project.subtitles)
    _first_text = page.project.subtitles[0].main_text
    page.project.remove_subtitles([0])

def verify(application):
    page = application.get_current_page()
    subtitles = page.project.subtitles
    assert len(subtitles) == _count_before
    assert subtitles[0].main_text == _first_text
