"""
Edit preferences: activating should create and show the (non-modal)
preferences dialog. It is shown rather than run through run_dialog, so it is
not intercepted by the harness dialog script.
"""

def setup(application):
    pass

def verify(application):
    # The dialog lives on the edit agent, reached via its activate callback.
    agent = application._on_edit_preferences_activate.__self__
    assert agent._pref_dialog is not None
