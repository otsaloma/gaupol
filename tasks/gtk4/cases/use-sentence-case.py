"""
Use sentence case: with the main text column focused and the first row
selected, the subtitle's main text should be recased to sentence case. The
row's text is primed to upper case first, since the sample text is already in
sentence case and would otherwise not change.
"""

def setup(application):
    page = application.get_current_page()
    col = page.view.columns.MAIN_TEXT
    page.view.set_focus(0, col)
    page.view.select_rows([0])
    doc = page.text_column_to_document(col)
    page.project.set_text(0, doc, "HELLO WORLD")
    global _text
    _text = "HELLO WORLD"

def verify(application):
    page = application.get_current_page()
    text = page.project.subtitles[0].main_text
    assert text != _text
    assert text.lower() == _text.lower()
