# Log

- Run the GUI as `timeout --signal=TERM 8 bin/gaupol
  data/samples/subrip.srt` so it self-terminates (exit 124) instead of
  blocking; the console output is then captured for inspection.

- To see all warnings, set `G_ENABLE_DIAGNOSTIC=1` (forces GTK to emit
  deprecation warnings) and read stderr (`2>&1`); GTK/GLib warnings go
  through the GLib log system, not Python `warnings`, so `pytest` needs
  `-s` to show them. Use `G_DEBUG=fatal-warnings` to turn a warning into
  a fatal error (with traceback) when tracking down its source.

## Deferred

- Migrate or remove the interactive `run_*`/`run_dialog` test helpers
  that rely on `Gtk.main()`/`Gtk.Dialog.run()`/`Gtk.WindowPosition` (~13
  test files); not collected by pytest, so they rot silently.
