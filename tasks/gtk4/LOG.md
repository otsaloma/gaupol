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
  simply not drawn. `lookup_color` and `get_color` exist in GTK-4 but
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
    dialog content padding is lost. See Deferred for restoring it.

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
  typelib loads Gtk 3.0 into the process, which conflicts with GTK-4
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

  - The `populate-popup` signal is gone (GTK-4 uses `extra-menu` models
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

- Migrated away from the `Gtk.main*` family: `gaupol.util.iterate_main`
  now iterates `GLib.MainContext.default()` (non-blocking), and
  `gaupol.TestCase` got an nfoview-style `main_loop(window)` helper that
  iterates the default main context while the window is visible. The
  interactive `run_*` test helpers (view, entries, spell, floatlabel,
  assistants, renderers) now use it instead of `Gtk.main()` +
  `delete-event`/`main_quit`. Since those helpers were rewritten anyway,
  they were converted fully to GTK-4 (`set_child`, `show`, dropped
  `Gtk.WindowPosition` — also from `test_floatlabel.py`'s
  `setup_method`); the `run_dialog`-based helpers in dialog tests remain
  for the blocking-dialogs item. `TestSpellChecker` base class changed
  from `aeidon.TestCase` to `gaupol.TestCase` to get `main_loop`.
  `TextAssistant`'s run helper relies on the assistant destroying itself
  on apply/cancel to end the loop.

- GdkScreen: only one use, `gaupol/style.py` `load_css` now calls
  `add_provider_for_display(Gdk.Display.get_default(), ...)` (in GTK
  since 4.0), following nfoview. Noticed in the same function:
  `_get_editor_font_css` picks its font-size unit with
  `Gtk.check_version(3, 22, 0)`, which under GTK-4 makes the unit
  silently flip from "pt" to "px"; sort that out with the GtkCssProvider
  migration item.

- Fixed `gaupol/style.py` `_update_css` being a no-op since commit
  75df44d3: `load_css` now installs a single module-level provider for
  the display once and `_update_css` reloads it on font conf changes, so
  open text views again update live (reloading an installed provider
  invalidates styles by itself). The `reset_style` calls in
  `prepare_text_view` relied on `_update_css` working and `reset_style`
  is gone in GTK-4, so those callbacks were removed. Verify live font
  change at runtime once the app starts.

- GdkWindow: only two uses, both trivial. `gaupol/util.py` cursor
  helpers now use `Gtk.Widget.set_cursor_from_name` (in GTK since 4.0),
  which also completes the "cursor API changes" item (no other mouse
  pointer code exists). `gaupol/agents/video.py` paned sizing now uses
  `Gtk.Widget.get_width/get_height` directly; note these return the
  widget's content size rather than the GdkWindow size, an irrelevant
  difference for picking the initial 50% paned position.

- GdkEvent: no direct event field access remains, the event controllers
  migration already moved everything to controller callback arguments;
  the remaining `event` parameters (cell renderers' `do_start_editing`,
  menu.py's deferred `enter/leave-notify-event` handlers) are never
  dereferenced. The "iconified" item was a no-op too, nothing touches
  iconification. One leftover found: the save dialog connects to the
  generic `"event"` signal, deferred to the FileChooser item (see
  Deferred).

- GtkClipboard → GdkClipboard: `x_clipboard` is now
  `Gdk.Display.get_clipboard()` (in GDK since 4.0). Notable details:

  - GdkClipboard has no synchronous read, so pasting is now
    asynchronous: `_on_paste_texts_activate` calls `read_text_async` and
    the actual paste logic moved to a `_paste_texts` callback.
    `test__on_paste_texts_activate` iterates the main context after
    activating so the callback still gets exercised.

  - GdkClipboard has no `set_can_store` equivalent; whether copied text
    persists in the desktop clipboard after quitting Gaupol is now up to
    the session's clipboard manager. Minor, acceptable regression.

  - `Gdk.Clipboard.set_text` is not introspectable; from Python use
    `set(str)` (PyGObject marshals the value). Verified the
    set/read-text roundtrip works in a test script under Wayland.

  - Found more GdkWindow API missed by commit e6b075ef (grep pattern
    missed `get_bin_window`): the paste handler's
    `freeze_updates`/`thaw_updates` around the tree view update. GTK-4's
    frame-based rendering has no update freezing, so they're simply
    dropped; the focus/scroll restoration logic remains.

  - `entries.py`'s `cut-clipboard`/`copy-clipboard` keybinding signal
    connections on TimeEntry are not GtkClipboard API, but they moved
    from GtkEntry to GtkText in GTK-4; left for the GtkEntry item.

- GtkBuilder: `connect_signals` is gone; PyGObject's GTK-4 override
  `Gtk.Builder(scope_object_or_map)` (added in PyGObject 3.40, README
  floor bumped from 3.38) installs a `BuilderScope` that resolves
  handler names on any plain Python object — but eagerly, at
  `add_from_file` parse time. Notable details:

  - `BuilderDialog` passes `self` as scope; the `connect_signals`
    parameter was dropped. Since handlers are now resolved before
    `self._dialog` is assigned, a missing handler would have made
    `__getattr__`'s delegation recurse infinitely; it now raises
    `AttributeError` for `_dialog`, so PyGObject instead prints a clear
    "Handler X not found" traceback and leaves that signal unconnected
    (GTK-3 `connect_signals` warned similarly; not a hard error in
    either case).

  - `PreferencesDialog` connected a callbacks map collected from its
    page objects after loading, which is impossible now (scope precedes
    parsing, pages need the loaded builder). Its `__getattr__` now
    resolves `_on_*` names to placeholder lambdas that look up the real
    handler from a `_callbacks` dict, filled once the pages exist.
    Verified with a standalone script against the real
    preferences-dialog.ui: parse succeeds and signals dispatch to
    late-filled callbacks.

- Focus handling changes: a near no-op. The `.ui` files already got
  `can-focus` → `focusable` in the builder-tool conversion, and nothing
  uses `set_can_focus` or the removed focus adjustments. The one real
  fix: `_on_set_edit_mode_activate` restored view focus by writing
  `props.has_focus`, which is read-only in GTK-4; it now calls
  `grab_focus()` instead.

- Keyboard shortcuts: the only `GtkAccelGroup` use was the search
  dialog's Ctrl+F (focus the pattern entry); it's now a
  `Gtk.ShortcutController` with `Gtk.ShortcutScope.GLOBAL` and a
  `Gtk.CallbackAction` (all in GTK since 4.0). The action accelerators
  in `gaupol/actions/*` go through
  `Gtk.Application.set_accels_for_action`, which is unchanged in GTK-4;
  no `GtkBindingSet`/`GtkAccelMap` usage existed. Verify Ctrl+F in the
  search dialog at runtime once the app starts.

- GtkEventBox: both uses were vestigial wrappers, since all widgets
  receive events in GTK-4. `FloatingLabel` now packs its label directly;
  `Page.tab_widget` is now the plain `Gtk.Box` holding the tab label and
  close button (the tab popup's click gesture already attaches to
  `tab_widget` itself, so it keeps working). The tab widget's
  `show_all()` call went away with the event box; children default to
  visible in GTK-4.

- GtkBox: the `gaupol.util` pack helpers now use `Gtk.Box.append` (in
  GTK since 4.0); `pack_start_expand` sets `hexpand`/`vexpand` on the
  child by box orientation. The unused `padding` parameter was dropped
  and `pack_start_fill` was removed as identical to `pack_start` in
  GTK-4 (children default to fill via `halign`/`valign`; fill only ever
  differed with expand). Caveat from the migration guide: unlike the
  GTK-3 expand child property, `hexpand`/`vexpand` propagate up the
  widget hierarchy, so check for layout surprises at runtime. The raw
  `pack_start` in `gaupol/player.py` is left for the deferred
  gtk4paintablesink switch. The `pack_start(renderer, expand=True)`
  calls elsewhere are Gtk.CellLayout API on combo boxes, not GtkBox;
  they still exist in GTK-4 (deprecated since 4.10, TreeView family).

- GtkWindow: window-size persistence (main window in `close.py`, text
  assistant, spell-check dialog) moved from `resize`/`get_size` to
  `set_default_size`/`get_default_size` (both since 4.0); in GTK-4 the
  default-size properties track user resizes and are the documented
  save-state mechanism. They report the unmaximized size when maximized,
  which all three save sites already guard for anyway. The text
  assistant's `set_position(CENTER_ON_PARENT)` was dropped without
  replacement: `GtkWindowPosition` is gone and placement of a modal
  transient window is up to the compositor. Verify saved sizes restore
  sensibly at runtime (GTK-4 sizes exclude window shadows, so old saved
  conf values may restore slightly differently once).

- GtkStack/GtkAssistant/GtkNotebook: a near no-op. The search dialog's
  `.ui` already got explicit `GtkStackPage` objects in the builder-tool
  conversion, and all the Notebook/Assistant methods we call
  (`append_page`, `set_tab_reorderable`, `reorder_child`,
  `set_page_type`, `set_page_complete`) still exist in GTK-4. The one
  real change: the notebook `tab-expand`/`tab-fill` child properties in
  `gaupol/agents/open.py` are now set on the `Gtk.NotebookPage` meta
  object via `Gtk.Notebook.get_page` (in GTK since 4.0), as
  `child_set_property` went away with GtkContainer.

- GtkContainer removal: generic `add`/`remove` replaced with the
  class-specific API (all in GTK since 4.0): `set_child` on
  Window/Button/ScrolledWindow/Overlay, `append` on Box, and
  `set_start_child`/`set_end_child` on Paned. Notable details:

  - GTK-3 `Paned.add1` implied `resize=False` for the start child while
    GTK-4 defaults both children to resizing, so `video.py` now calls
    `set_resize_start_child(False)` to keep window resizes stretching
    the subtitle view rather than the video player.

  - The edit-mode switch in `agents/view.py` now replaces the view with
    a single `scroller.set_child(new_view)` — GTK-4 setters unparent the
    old child themselves, no separate `remove` needed.

  - `ruler.py` dropped `text_view.get_border_width()` from the margin x
    coordinate: container border width is gone in GTK-4 and nothing ever
    set it on text views, so it was always 0.

  - `test_assistants.py` setups converted like the earlier run helpers
    (`set_child`, `show`, dropped the 12px `set_border_width`).

  - Left for their own items: `Gtk.ToolItem.add` in `agents/video.py`
    (GtkToolbar), `menu.get_children`/`menu.remove` in `agents/menu.py`
    (GtkMenu), and all `show_all` calls (widgets visible by default).

## Deferred

- Dialog borders were lost in the `.ui` conversion (`border_width` is
  gone in GTK-4): categorically, all dialogs should get GNOME
  HIG-compliant 18px borders, set as margins on the first child of the
  content area. Same for the sub-containers that carried their own 12px
  border: the preferences dialog's per-tab boxes and the search dialog's
  stack page boxes. It's the same four `set_margin_*` lines repeating,
  so probably warrants a `gaupol.util` function; the Python-built
  dialogs (encoding, multi-close, debug) should use it too. The file
  chooser dialogs (open, save, multi-save) get reworked in the
  GtkFileChooser item — settle their borders there. The text-assistant
  page files also lost `border_width`, but theirs was on the throwaway
  wrapper window and never applied at runtime, so nothing to restore.

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

- The `Gtk.main()`-based interactive test helpers are migrated, but the
  `run_dialog`/`flash_dialog`-based ones (~28 test files) still rely on
  `Gtk.Dialog.run()`; handle them with the "Stop using blocking dialog
  functions" item and remember they're not collected by pytest, so they
  rot silently. Smoke-test a couple of `run_*` helpers interactively
  once `import gaupol` works again.

- `gaupol/dialogs/save.py` connects the save button to the generic
  `"event"` signal (removed in GTK-4, crashes dialog init) to add a
  missing filename extension before overwrite confirmation. Rework this
  with the "Update to GtkFileChooser API changes" item: the handler and
  `_on_response` are built on `get_filename`/`set_filename`/
  `set_do_overwrite_confirmation`/`stop_emission`, which all go away in
  the same rework.

- The multi-save dialog's `GtkFileChooserButton` (removed in GTK-4) is
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
