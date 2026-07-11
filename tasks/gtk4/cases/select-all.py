"""
Select all: every subtitle row should end up selected.
"""

def setup(application):
    page = application.get_current_page()
    page.view.select_rows([0])

def verify(application):
    page = application.get_current_page()
    count = len(page.project.subtitles)
    assert page.view.get_selected_rows() == tuple(range(count))
