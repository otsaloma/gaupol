# -*- coding: utf-8 -*-

import os

# Avoid segfaults with GTK 4.22 under Wayland: destroying a window
# whose focus is in a text entry, with no other window left, and then
# showing a new window crashes in GTK's Wayland text-input code when
# a late input-method event arrives for the freed widget. Tests create
# and destroy windows like that constantly; the app itself keeps its
# main window alive and is not affected. The simple input method
# bypasses the Wayland text-input protocol entirely.
os.environ["GTK_IM_MODULE"] = "gtk-im-context-simple"

def pytest_configure(config):
    # Silence the shitload of warnings about GTK deprecations.
    # We'll probably clear these only once bumping the major GTK version.
    config.addinivalue_line("filterwarnings", r"ignore:Gtk\..* is deprecated:DeprecationWarning")
    config.addinivalue_line("filterwarnings", r"ignore::gi.PyGIDeprecationWarning")
