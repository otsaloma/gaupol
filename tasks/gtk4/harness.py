#!/usr/bin/env python3

"""
Drive Gaupol actions in-process and verify results.

Creates a real gaupol.Application, opens a sample file, activates actions the
same way the menubar would and checks the outcome via application state and
screenshots. Dialogs opened through gaupol.util.run_dialog are intercepted:
they get screenshotted and receive a scripted response, so nothing blocks.

Usage: python3 tasks/gtk4/harness.py [OUTDIR]

Run from anywhere; the repository is put on sys.path. Screenshots go to OUTDIR
(default: a new temporary directory). Run with G_ENABLE_DIAGNOSTIC=1 and check
that stderr stays empty.
"""

import glob
import importlib.util
import os
import sys
import tempfile
import traceback

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)

import gaupol
assert gaupol.__version__ == "1.99"

from gi.repository import GLib
from gi.repository import Gtk

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="gaupol-harness-")
SAMPLE = os.path.join(REPO, "data", "samples", "subrip.srt")

def wait(ms=500):
    """Iterate the default main context for `ms` milliseconds."""
    loop = GLib.MainLoop()
    GLib.timeout_add(ms, lambda *args: loop.quit())
    loop.run()

def screenshot(widget, name):
    """Render `widget`'s window content to OUTDIR/`name`.png."""
    # BuilderDialog wraps its Gtk.Dialog rather than subclassing it.
    if not isinstance(widget, Gtk.Widget):
        widget = widget._dialog
    paintable = Gtk.WidgetPaintable(widget=widget)
    snapshot = Gtk.Snapshot()
    paintable.snapshot(snapshot,
                       paintable.get_intrinsic_width(),
                       paintable.get_intrinsic_height())

    texture = widget.get_native().get_renderer().render_texture(snapshot.to_node())
    path = os.path.join(OUTDIR, "{}.png".format(name))
    texture.save_to_png(path)
    print("Screenshot: {}".format(path))

# Intercept gaupol.util.run_dialog (which flash_dialog calls too): keep the
# real nested-main-loop semantics, but schedule a screenshot followed by a
# scripted response so the dialog never blocks the harness. run_case sets
# _dialog_script per case; each dialog opened consumes one entry.
_real_run_dialog = gaupol.util.run_dialog
_dialog_script = []
_case_name = ""

def _intercepted_run_dialog(dialog):
    response = _dialog_script.pop(0)
    def respond():
        screenshot(dialog, "{}-dialog".format(_case_name))
        dialog.emit("response", response)
    GLib.timeout_add(500, lambda *args: respond())
    return _real_run_dialog(dialog)

gaupol.util.run_dialog = _intercepted_run_dialog

def run_case(application, name, setup, dialog_script, verify):
    """Run one action test case, return True if it passed."""
    global _case_name, _dialog_script
    _case_name = name
    _dialog_script = list(dialog_script)
    print("Case: {}".format(name))
    try:
        # Start each case from a pristine page so cases can't affect one
        # another. The window itself is kept alive across cases: destroying
        # and recreating the whole application would risk the Wayland
        # text-input segfault documented in LOG.md.
        while application.pages:
            application.close(application.pages[-1], confirm=False)
        application.open_main(SAMPLE)
        setup(application)
        wait()
        screenshot(application.window, "{}-1-before".format(name))
        action = application.get_action(name)
        assert action.get_enabled(), "action not enabled"
        action.activate()
        wait()
        screenshot(application.window, "{}-2-after".format(name))
        verify(application)
        assert not _dialog_script, "not all scripted dialogs appeared"
        print("Case: {}: PASS".format(name))
        return True
    except Exception:
        traceback.print_exc()
        print("Case: {}: FAIL".format(name))
        return False

# Autodiscover cases from cases/*.py. Each module provides setup(application)
# and verify(application) functions and an optional DIALOG_SCRIPT list of
# responses (empty if the action opens no dialogs). A case's file name is its
# action name, which must match a menubar.ui action (win.insert-subtitles ->
# insert-subtitles.py).

def discover_cases():
    """Generate a list of (name, setup, dialog_script, verify) tuples."""
    pattern = os.path.join(os.path.dirname(__file__), "cases", "*.py")
    for path in sorted(glob.glob(pattern)):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location("case_" + name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        dialog_script = getattr(module, "DIALOG_SCRIPT", [])
        yield (name, module.setup, dialog_script, module.verify)

def main():
    application = gaupol.Application()
    application.open_main(SAMPLE)
    wait(1500)
    cases = list(discover_cases())
    passed = [run_case(application, *case) for case in cases]
    application.window.destroy()
    print("{:d}/{:d} cases passed".format(sum(passed), len(passed)))
    sys.exit(0 if all(passed) else 1)

if __name__ == "__main__":
    main()
