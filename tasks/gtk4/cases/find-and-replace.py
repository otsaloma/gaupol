"""
Find and replace: activating should create and show the (non-modal) search
dialog. It is shown rather than run through run_dialog, so it is not
intercepted by the harness dialog script.
"""

def setup(application):
    pass

def verify(application):
    assert application._search_dialog is not None
