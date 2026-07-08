"""
New project: creating a new project should add a second, blank page holding
a single subtitle.
"""

def setup(application):
    global _count_before
    _count_before = len(application.pages)

def verify(application):
    assert len(application.pages) == _count_before + 1
    page = application.get_current_page()
    assert len(page.project.subtitles) == 1
