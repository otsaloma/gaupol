"""
Invert selection: the rows that were selected become unselected and vice
versa.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([0, 1])

def verify(application):
    page = application.get_current_page()
    count = len(page.project.subtitles)
    assert page.view.get_selected_rows() == tuple(range(2, count))
