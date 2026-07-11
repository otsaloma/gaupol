"""
Merge subtitles: merging two adjacent selected subtitles should reduce the
subtitle count by one.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([0, 1])
    global _count_before
    _count_before = len(page.project.subtitles)

def verify(application):
    page = application.get_current_page()
    assert len(page.project.subtitles) == _count_before - 1
