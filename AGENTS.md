# AGENTS.md

## Architecture

We have two packages of Python code: `aeidon` and `gaupol`. `aeidon` is
the user-interface independent part and `gaupol` is the GTK application
user interface. The split into two packages was an afterthought and the
separation is not perfect. In all changes, consider this separation and
try to find the right place for any new code.

## Environment

See `README.md` for which versions of Python, GTK, etc. we're currently
targeting. Regarding operating systems, we currently target only Linux,
but try to avoid any OS-specific code. On Linux, we want to support all
relevant desktops and display servers, but GNOME + Wayland is whose
conventions we want to follow closest.

## Subtitle File Formats

We support many subtitle file formats and want to keep it that way.
However, in practice, SubRip is by far the most common and the most
important. SubRip is the format that needs to work well and other
formats are fine to be just partially supported.

## GTK Documentation

Documentation for GTK and associated libraries is available as GIR files
under `/usr/share/gir-1.0`. Grep those for any symbols you need.

- `/usr/share/gir-1.0/Gdk-4.0.gir`
- `/usr/share/gir-1.0/Gio-2.0.gir`
- `/usr/share/gir-1.0/GLibUnix-2.0.gir`
- `/usr/share/gir-1.0/GObject-2.0.gir`
- `/usr/share/gir-1.0/Gtk-4.0.gir`

A GTK-3 to GTK-4 migration guide is available in Markdown format. We
have done the migration, but noting this guide because we might have
some regressions left over from it and some deprecated (not removed)
widgets remain unmigrated.

- `tasks/gtk4/migrating-3to4.md`

Make sure you can access all these documentation in full; abort if not.
Never guess how the API works, always check from the documentation. Keep
in mind that we use Python and some of the documentation has been
written for C. You'll need adapt what you see there, for example:

- `GTK_ALIGN_CENTER` → `Gtk.Align.CENTER`
- `gtk_box_new(...)` → `Gtk.Box(...)`
- `gtk_widget_show(widget)` → `widget.show()`

## Validation, Testing

After making changes to Python code, always at minimum run `flake8 ...`
and `pytest ...` against all changed files. After bigger changes, or if
you suspect your changes affect other modules, use `make check` and
`make test` to run the full validation and test suites.

## Running the GUI

You can run the GUI as `timeout --signal=TERM 8 bin/gaupol
data/samples/subrip.srt` so it self-terminates (exit 124) instead of
blocking; the console output is then captured for inspection.

To see all warnings, set `G_ENABLE_DIAGNOSTIC=1` (forces GTK to emit
deprecation warnings) and read stderr (`2>&1`); GTK/GLib warnings go
through the GLib log system, not Python `warnings`, so `pytest` needs
`-s` to show them. Use `G_DEBUG=fatal-warnings` to turn a warning into a
fatal error (with traceback) when tracking down its source.

Note that some previous version of gaupol might be installed under a
system directory, such as `/usr/local`. When running a standalone
verification script, make sure your `PYTHONPATH` or `sys.path` points to
the source repo. Check `gaupol.__file__` in code if unsure.

To screenshot the app, run a standalone script that creates
`gaupol.Application()` and calls `application.open_main(paths)` (the
same calls `applicationman.py` makes), then in a `GLib.timeout_add`
callback (~1500 ms, inside a `GLib.MainLoop`) render the window to PNG:

```python
paintable = Gtk.WidgetPaintable(widget=window)
snapshot = Gtk.Snapshot()
paintable.snapshot(snapshot, paintable.get_intrinsic_width(), paintable.get_intrinsic_height())
texture = window.get_native().get_renderer().render_texture(snapshot.to_node())
texture.save_to_png(path)
```

This captures the window content regardless of the Wayland compositor.
Caveat: the menubar doesn't render, since the script has no
`Gtk.Application` (`gaupol.appman`) to provide the menubar model. The
same recipe works for dialogs (snapshot the dialog widget instead), such
as built via the dialog test classes' `setup_method`.
