"""
Copy texts: with the main text column focused and the first row selected,
copying should place that subtitle's text on the project clipboard while
leaving the subtitle itself unchanged.
"""

def setup(application):
    page = application.get_current_page()
    page.view.set_focus(0, page.view.columns.MAIN_TEXT)
    page.view.select_rows([0])
    global _text
    _text = page.project.subtitles[0].main_text

def verify(application):
    page = application.get_current_page()
    assert page.project.subtitles[0].main_text == _text
    assert page.project.clipboard.get_texts() == [_text]
