"""
End earlier: with a single row selected, the end position should move to an
earlier value while the subtitle count stays the same.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([3])
    global _end_before, _count_before
    _end_before = page.project.subtitles[3].end_seconds
    _count_before = len(page.project.subtitles)

def verify(application):
    page = application.get_current_page()
    subtitles = page.project.subtitles
    assert len(subtitles) == _count_before
    assert subtitles[3].end_seconds < _end_before
