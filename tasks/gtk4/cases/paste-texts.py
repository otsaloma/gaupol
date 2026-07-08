"""
Paste texts: with a known string primed on both the desktop and project
clipboards and the main text column focused, pasting should replace the first
subtitle's main text with that string.

The paste reads the desktop clipboard asynchronously, so the harness main loop
iteration after activation is what lets the paste complete.
"""

def setup(application):
    page = application.get_current_page()
    page.view.set_focus(0, page.view.columns.MAIN_TEXT)
    page.view.select_rows([0])
    application.x_clipboard.set("PASTED")
    page.project.clipboard.set_string("PASTED")

def verify(application):
    page = application.get_current_page()
    assert page.project.subtitles[0].main_text == "PASTED"
