"""
Remove subtitles: removing the single selected first row should drop the
subtitle count by one and promote the original second subtitle to row 0.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([0])
    global _count_before, _second_text
    _count_before = len(page.project.subtitles)
    _second_text = page.project.subtitles[1].main_text

def verify(application):
    page = application.get_current_page()
    subtitles = page.project.subtitles
    assert len(subtitles) == _count_before - 1
    assert subtitles[0].main_text == _second_text
