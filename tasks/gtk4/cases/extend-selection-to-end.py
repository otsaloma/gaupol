"""
Extend selection to end: from a single selected row, the selection should
grow to cover every row from that one up to the last.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([5])

def verify(application):
    page = application.get_current_page()
    count = len(page.project.subtitles)
    assert page.view.get_selected_rows() == tuple(range(5, count))
