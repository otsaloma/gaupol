"""
Extend selection to beginning: from a single selected row, the selection
should grow to cover every row from the first up to that one.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([3])

def verify(application):
    page = application.get_current_page()
    assert page.view.get_selected_rows() == (0, 1, 2, 3)
