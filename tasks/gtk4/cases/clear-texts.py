"""
Clear texts: with the main text column focused and the first row selected,
clearing should blank that subtitle's main text.
"""

def setup(application):
    page = application.get_current_page()
    page.view.set_focus(0, page.view.columns.MAIN_TEXT)
    page.view.select_rows([0])

def verify(application):
    page = application.get_current_page()
    assert not page.project.subtitles[0].main_text
