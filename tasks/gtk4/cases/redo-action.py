"""
Redo action: after removing a subtitle and undoing it in setup, redoing
should re-apply the removal and drop the subtitle count by one.
"""

def setup(application):
    page = application.get_current_page()
    global _count_before
    _count_before = len(page.project.subtitles)
    page.project.remove_subtitles([0])
    page.project.undo()

def verify(application):
    page = application.get_current_page()
    assert len(page.project.subtitles) == _count_before - 1
