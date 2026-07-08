"""
Close all projects: with two (unmodified) projects open, activating should
close every page. Unmodified documents need no save confirmation, so no dialog
appears.
"""

import gaupol
import os

SECOND = os.path.join(os.path.dirname(gaupol.__file__),
                      "..", "data", "samples", "subviewer2.sub")

def setup(application):
    application.open_main(os.path.abspath(SECOND))

def verify(application):
    assert len(application.pages) == 0
