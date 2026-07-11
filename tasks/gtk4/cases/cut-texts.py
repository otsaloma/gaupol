"""
Cut texts: with the main text column focused and the first row selected,
cutting should blank the subtitle's main text and place it on the project
clipboard.
"""

def setup(application):
    page = application.get_current_page()
    page.view.set_focus(0, page.view.columns.MAIN_TEXT)
    page.view.select_rows([0])
    global _text
    _text = page.project.subtitles[0].main_text

def verify(application):
    page = application.get_current_page()
    assert not page.project.subtitles[0].main_text
    assert page.project.clipboard.get_texts() == [_text]
