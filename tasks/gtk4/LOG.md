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

- Switched `gi.require_version` to Gdk/Gtk 4.0. GStreamer namespaces
  stay at 1.0 (the only GIR version there is). `import aeidon` works;
  `import gaupol` still fails on removed GTK-3 APIs used at module level
  (first hit: `Gtk.ToolbarStyle` in `gaupol/enums.py`) — that's the next
  step, migrating removed APIs one by one.

- Disabled Gspell entirely: it's GTK-3-only and merely importing its
  typelib loads Gtk 3.0 into the process, which conflicts with GTK 4
  (`import aeidon` before requiring Gtk 4.0 would make the whole app
  fail to start). Imports commented out in `aeidon/spell.py`,
  `gaupol/spell.py` and `aeidon/__init__.py`; `SpellChecker.available()`
  now returns False so all spell-check UI disables itself gracefully.

- Updated README and CI workflow packages: `gir1.2-gtk-3.0` →
  `gir1.2-gtk-4.0`, `gstreamer1.0-gtk3` → `gstreamer1.0-gtk4`, dropped
  `gir1.2-gspell-1`, GTK requirement now ≥ 4.0 (tighten later to
  whatever 4.x version we end up needing symbols from).

- Bumped README dependency floors: Python ≥ 3.10, PyGObject ≥ 3.38
  (first release with GTK-4 support) and GStreamer ≥ 1.18 (contemporary
  of GTK 4.0, September vs. December 2020). If the final GTK floor ends
  up ≥ 4.14, raise GStreamer to its contemporary 1.24.

- Migrated all `GtkWidget` event signals to event controllers and
  gestures. Notable details:

  - Main window and text assistant now save maximization via
    `notify::maximized` instead of `window-state-event`; the main
    window's `delete-event` quit hook is now `close-request`; the search
    dialog uses `Gtk.Window.set_hide_on_close` instead of a
    `delete-event` handler returning True.

  - The right-click popup menus (view, tab, column header) had to be
    converted from `Gtk.Menu` to `Gtk.PopoverMenu` in the same go,
    because the `Gtk.Menu.popup` calls depended on the event object. The
    popover is created per click, parented to the clicked widget and
    unparented (idle) on close. This covers part of the "GtkMenu is
    gone" migration item; the rest of `menu.py` (undo/redo button menus,
    recent menus, and their `enter/leave-notify-event` handlers on
    `Gtk.MenuItem`s) was deliberately left untouched for that item, as
    it all gets rewritten together.

  - The `populate-popup` signal is gone (GTK 4 uses `extra-menu` models
    on `Gtk.Text`/`Gtk.TextView`). Removed the "Italic" context menu
    item of the text cell editor and the `_in_editor_menu` guards that
    kept focus-out from ending cell editing while a context menu was
    open. See Deferred.

  - Key controllers were added in the capture phase where the old
    handlers relied on running before the widget's own handling (cell
    editors' Enter/Escape, TimeEntry's Backspace/Delete, view's
    Ctrl+PageUp/Down block). See Deferred for a runtime check.

  - `gaupol.View` uses `Gdk.keyval_to_unicode(keyval)` in place of the
    removed `event.string` for toggling interactive search.

  - `FloatingLabel.register_hide_event(widget, event)` now takes
    "button-press", "key-press" or "scroll" and adds a capture-phase
    controller; controllers are removed again when the label hides.

  - Reconnected the search dialog text view's focus-out saving of edits
    (dropped earlier with the `.ui` conversion) via
    `Gtk.EventControllerFocus`; clears the earlier Deferred item.

## Deferred

- Reimplement spell-check without Gspell (GTK-3-only, now disabled): the
  aeidon `SpellChecker` backend (`Gspell.Checker`), inline spell-check
  in text views (`gaupol/spell.py`), and
  `gaupol/util.py:get_gspell_version` (debug dialog). Candidate:
  libspelling (`gir1.2-spelling-1`, in Debian as libspelling-1-2 0.4.x);
  check it covers both the word-checker API and inline GtkTextView
  checking. Until then `aeidon/test/test_spell.py` and
  `gaupol/test/test_spell.py` fail (they assume availability), and
  README/CI no longer list a spell-check dependency — re-add one when
  reimplemented.

- Switch `gaupol/player.py` from `gtksink` to `gtk4paintablesink` +
  `Gtk.Picture` during the code migration; README/CI already point to
  `gstreamer1.0-gtk4`.

- Migrate or remove the interactive `run_*`/`run_dialog` test helpers
  that rely on `Gtk.main()`/`Gtk.Dialog.run()`/`Gtk.WindowPosition` (~13
  test files); not collected by pytest, so they rot silently.

- The multi-save dialog's `GtkFileChooserButton` (removed in GTK 4) is
  now a plain `GtkButton` with the same id `filechooser_button`, but
  non-functional: reimplement folder selection in `multi_save.py`
  (`get_filename`/`set_filename` calls, dialog title "Select A Folder")
  with a file chooser dialog during the code migration.

- Reimplement the "Italic" context menu item of the multiline cell
  editor with `Gtk.TextView.set_extra_menu` when doing the GtkMenu
  migration (Ctrl+I still works). Also verify that opening the default
  context menu in cell editors (text and time) doesn't cancel editing
  via the focus controller's "leave" — the old `populate-popup` +
  `_in_editor_menu` guard against that was removed.

- Verify at runtime that Ctrl+Page_Up/Down switches notebook tabs while
  the view has focus: the view's capture-phase key controller consumes
  those keys to block TreeView's paging bindings, which assumes GTK-4
  handles application accelerators at the window before the focus
  widget's controllers. If tab switching broke, rethink.

- `TimeEntry.set_text` triggers a `g_value_get_int: assertion
  'G_VALUE_HOLDS_INT (value)' failed` warning: PyGObject can't marshal
  the in-out position argument of the "insert-text" signal that
  `gaupol/entries.py` connects to. Harmless noise in GTK-3; fix as part
  of the GTK-4 rework of TimeEntry ("key-press-event" and GtkEditable
  handling change anyway).
