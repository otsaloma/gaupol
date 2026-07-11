"""
Activate previous project: with a second project open and active,
activating should switch to the previous (first) tab.
"""

import gaupol
import os

SECOND = os.path.join(os.path.dirname(gaupol.__file__),
                      "..", "data", "samples", "subviewer2.sub")

def setup(application):
    application.open_main(os.path.abspath(SECOND))

def verify(application):
    page = application.get_current_page()
    assert application.pages.index(page) == 0
