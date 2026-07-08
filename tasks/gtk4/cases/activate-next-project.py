"""
Activate next project: with a second project open and the first one active,
activating should switch to the next (second) tab.
"""

import gaupol
import os

SECOND = os.path.join(os.path.dirname(gaupol.__file__),
                      "..", "data", "samples", "subviewer2.sub")

def setup(application):
    application.open_main(os.path.abspath(SECOND))
    application.set_current_page(application.pages[0])

def verify(application):
    page = application.get_current_page()
    assert application.pages.index(page) == 1
