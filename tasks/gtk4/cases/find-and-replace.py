"""
Find and replace: activating should create and show the (non-modal) search
dialog. It is shown rather than run through run_dialog, so it is not
intercepted by the harness dialog script.
"""

def setup(application):
    pass

def verify(application):
    # The dialog lives on the search agent, reached via its activate callback.
    agent = application._on_find_and_replace_activate.__self__
    assert agent._search_dialog is not None
