# AGENTS.md

## Architecture

We have two packages of Python code: `aeidon` and `gaupol`. `aeidon` is
the user-interface independent part and `gaupol` is the GTK application
user interface. The split into two packages was an afterthought and the
separation is not perfect. In all changes, consider this separation and
try to find the right place for any new code.

## Environment

See `README.md` for dependency versions. Target Linux and *BSD; avoid
OS-specific code. Preserve existing Windows conditionals, but don't
account for Windows in new features. Support relevant Linux desktops and
display servers, following GNOME + Wayland conventions most closely.

## Subtitle File Formats

We support many subtitle file formats and want to keep it that way.
However, in practice, SubRip is by far the most common and the most
important. SubRip is the format that needs to work well and other
formats are fine to be just partially supported.

## GTK Documentation

Documentation for GTK and associated libraries is available as GIR files
under `/usr/share/gir-1.0`. Grep those for any symbols you need. Make
sure you can access that GIR documentation; abort if not. Never guess
how the API works, always check from the documentation. Keep in mind
that we use Python and some of the documentation has been written for C.
You'll need adapt what you see there, for example:

- `GTK_ALIGN_CENTER` → `Gtk.Align.CENTER`
- `gtk_box_new(...)` → `Gtk.Box(...)`
- `gtk_widget_show(widget)` → `widget.show()`

## Validation, Testing

After making changes to Python code, always at minimum run `flake8 ...`
and `pytest ...` against all changed files. After making changes to
GtkBuilder `.ui` files, run `gtk4-builder-tool validate ...`. After
bigger changes, or if you suspect your changes affect other modules, use
`make check` and `make test` to run the full validation and test suites.

## Running the GUI

Run a brief GUI check with diagnostics enabled: `G_ENABLE_DIAGNOSTIC=1
timeout 5 bin/gaupol data/samples/subrip.srt 2>&1`. Exit 124 is expected
on timeout. Use `pytest -s` to expose GTK/GLib warnings in tests, and
`G_DEBUG=fatal-warnings` to stop on warnings when debugging.

Standalone scripts must import aeidon and gaupol from this checkout, not
an installed copy. Set `PYTHONPATH` or `sys.path` accordingly; verify
`aeidon.__file__` and `gaupol.__file__` if unsure.

## Screenshots

For unattended screenshots, render the app's own widgets to PNG using
`Gtk.WidgetPaintable`, `Gtk.Snapshot` and the widget's native renderer
(`render_texture`, then `save_to_png`). This avoids Wayland screenshot
permissions.

Use a standalone script running the app and its GTK main loop; capture
after the target window is visible and has rendered. Capture dialogs
separately; existing dialog test setup methods can help construct them.
