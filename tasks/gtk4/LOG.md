# Log

- Run the GUI as `timeout --signal=TERM 8 bin/gaupol
  data/samples/subrip.srt` so it self-terminates (exit 124) instead of
  blocking; the console output is then captured for inspection.

- To see all warnings, set `G_ENABLE_DIAGNOSTIC=1` (forces GTK to emit
  deprecation warnings) and read stderr (`2>&1`); GTK/GLib warnings go
  through the GLib log system, not Python `warnings`, so `pytest` needs
  `-s` to show them. Use `G_DEBUG=fatal-warnings` to turn a warning into
  a fatal error (with traceback) when tracking down its source.

- Retested CSS `:nth-child` zebra stripes (the XXX comment in
  `gaupol/util.py` `get_zebra_color`): still not viable, GtkTreeView has
  no per-row CSS nodes, the selector matches the whole widget. Real
  per-row CSS only comes with the GtkListView family.

- `get_zebra_color` now uses `lookup_color("theme_base_color")`; if a
  theme doesn't define that color, it returns None and zebra stripes are
  simply not drawn. `lookup_color` and `get_color` exist in GTK 4 but
  are deprecated since 4.10 — revisit with the TreeView question.

- `show_uri` now uses `Gio.AppInfo.launch_default_for_uri` instead of
  any of the churning `Gtk.show_uri*` variants; no GTK API involved
  anymore, portal-aware under Flatpak.

- Removed deprecated `rules_hint` from the `.ui` files: dialog tree
  views (preferences, spell-check, language, text assistant) lose
  theme-drawn zebra stripes already under GTK-3. `margin_left` →
  `margin_start` in the same files, no visual change.

- The `PyGIDeprecationWarning: GLib.unix_signal_add_full` warning at
  import is internal to PyGObject 3.56 (it registers the alias as
  deprecated twice in `gi/overrides/GLib.py`); nothing to fix on our
  side, ignore it.

- Converted all 26 `.ui` files to GTK-4 format with `gtk4-builder-tool
  simplify --3to4` plus manual fixes for what the tool only warns about;
  all files now pass `gtk4-builder-tool validate`. The app and the
  dialog tests are broken (segfault, even) under GTK-3 until the GTK-4
  switch. Notable changes beyond the mechanical ones:

  - Dropped `border_width` (12px) from all dialogs and assistant pages:
    dialog content padding is lost, review spacing visually under GTK 4
    and add margins where needed.

  - `GtkButtonBox` → `GtkBox`: buttons in a box are no longer
    homogeneous in size by default (spell-check dialog's button column
    is the most visible case); set homogeneous if it looks off. Also
    deleted the empty leftover `action_area` boxes.

  - The two `GtkArrow`s in the position transform dialog are now
    `GtkImage`s with `go-next-symbolic` (also flips in RTL, unlike
    GtkArrow's fixed direction).

  - The preferences dialog `GtkToolbar` became a `GtkBox` with the
    `toolbar` CSS class, `GtkToolButton`s became `GtkButton`s (all done
    by the tool).

  - `translatable="yes"` became `translatable="1"`: verified OK for
    string extraction, the gettext GtkBuilder ITS rules accept both.

## Deferred

- Migrate or remove the interactive `run_*`/`run_dialog` test helpers
  that rely on `Gtk.main()`/`Gtk.Dialog.run()`/`Gtk.WindowPosition` (~13
  test files); not collected by pytest, so they rot silently.

- The multi-save dialog's `GtkFileChooserButton` (removed in GTK 4) is
  now a plain `GtkButton` with the same id `filechooser_button`, but
  non-functional: reimplement folder selection in `multi_save.py`
  (`get_filename`/`set_filename` calls, dialog title "Select A Folder")
  with a file chooser dialog during the code migration.

- Removed the `focus-out-event` signal (GTK 4 has no event signals) from
  `search-dialog.ui`: `_on_text_view_focus_out_event` in `search.py` is
  now never called, reconnect it in code via `Gtk.EventControllerFocus`
  during the code migration.

- `TimeEntry.set_text` triggers a `g_value_get_int: assertion
  'G_VALUE_HOLDS_INT (value)' failed` warning: PyGObject can't marshal
  the in-out position argument of the "insert-text" signal that
  `gaupol/entries.py` connects to. Harmless noise in GTK-3; fix as part
  of the GTK-4 rework of TimeEntry ("key-press-event" and GtkEditable
  handling change anyway).
