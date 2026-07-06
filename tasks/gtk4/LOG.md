# Log

- Run the GUI as `timeout --signal=TERM 8 bin/gaupol
  data/samples/subrip.srt` so it self-terminates (exit 124) instead of
  blocking; the console output is then captured for inspection.

- To see all warnings, set `G_ENABLE_DIAGNOSTIC=1` (forces GTK to emit
  deprecation warnings) and read stderr (`2>&1`); GTK/GLib warnings go
  through the GLib log system, not Python `warnings`, so `pytest` needs
  `-s` to show them. Use `G_DEBUG=fatal-warnings` to turn a warning into
  a fatal error (with traceback) when tracking down its source.

- Run standalone verification scripts with the repository on
  `PYTHONPATH`: Python puts the script's directory, not the working
  directory, on `sys.path`, so a script run by path outside the repo
  imports the GTK-3 gaupol 1.16 installed under `/usr/local` and
  "verifies" the wrong code (it can even hang, since the GTK-3 app
  blocks in main loops that ignore SIGTERM). The repo version is bumped
  to 1.99, so `assert gaupol.__version__ == "1.99"` catches any mixup.
  `python3 -c` and `pytest` run from the repo root resolve correctly,
  as they put the working directory on `sys.path`.

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

- gtk_widget_destroy removal: a no-op. Every `.destroy()` call in the
  codebase is on a toplevel window (dialogs, main window, TextAssistant,
  the text-assistant pages' throwaway wrapper window) and
  `Gtk.Window.destroy` exists in GTK-4 (since 4.0); nothing destroys
  non-window widgets. The `destroy_with_parent` window property is
  unchanged too.

- GtkStyleContext: `get_style_context().add_class(...)` with our custom
  CSS classes replaced by `Gtk.Widget.add_css_class` (in GTK since 4.0)
  in player, page, floatlabel and `style.py` `use_font`;
  `get_zebra_color` drops the state argument from `get_color()` (gone in
  GTK-4). The `Gtk.STYLE_CLASS_*` constants are gone: the
  `add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)` lines in the preferences
  dialogs (gaupol + custom-framerates extension) were dropped entirely —
  those toolbars are already GtkBoxes with the "toolbar" CSS class from
  the `.ui` conversion, and GTK-4 has no "inline-toolbar" styling (minor
  visual change: standard toolbar look instead of GTK-3's
  attached-to-tree-view inline look). Left for their own items:
  `application.py` `_init_main_toolbar`'s STYLE_CLASS_PRIMARY_TOOLBAR
  (GtkToolbar item, whole method gets rewritten) and `ruler.py`'s
  `Gtk.render_layout(style, ...)` (GtkWidget::draw item).
  `Gtk.StyleContext.add_provider_for_display` in `style.py` stays: it
  exists since 4.0 and is not deprecated (only the instance API is).

- GtkCssProvider: `style.py` now uses `load_from_string` (in GTK since
  4.12 — the first symbol pushing our GTK floor above 4.0, README
  updated to ≥ 4.12; `load_from_data` exists since 4.0 but with a
  changed signature and deprecated since 4.12). Also resolved the
  `_get_editor_font_css` font-size unit hack flagged earlier:
  `Gtk.check_version(3, 22, 0)` is non-None under GTK-4 (major
  mismatch), so the unit had silently flipped to "px"; now hardcoded to
  "pt". Verified empirically that "pt" is correct: GTK-4 CSS resolves
  pt using gtk-xft-dpi (13pt → 13 × dpi/72 px), the same way Pango
  resolves the point sizes that font choosers produce, so pt tracks the
  desktop text-scaling-factor while px would ignore it; libadwaita does
  the same, emitting `--document-font-size: %dpt` when converting the
  GNOME font settings to CSS. Verified provider load + reload with the
  generated CSS in a standalone script.

- GtkShadowType/GtkRelief: scrolled windows' `set_shadow_type` became
  `set_has_frame` (in GTK since 4.0): ETCHED_IN → True, and the NONE
  calls (encoding, text-edit dialogs) were dropped since GTK-4
  ScrolledWindow defaults to no frame. The tab close button's
  `set_relief(NONE)` became `set_has_frame(False)` — needed explicitly,
  GTK-4 buttons default to has-frame True. Any GTK-3 vs. GTK-4 frame
  drawing differences (ETCHED_IN vs. flat border) are up to the theme.
  Also fixed two `scroller.add()` calls (preview-error and text-edit
  dialogs) that the GtkContainer migration in commit a9e46e22 missed;
  now `set_child`.

- Size requests: all `get_preferred_width/height()[1]` calls (util,
  view, ruler, page) became `measure(orientation, -1).natural` (in GTK
  since 4.0), following nfoview. All call sites wanted the natural size
  of an unrooted throwaway label (or the tab image / tree view
  scroller), so semantics are unchanged; verified the measure-based
  sizing returns sensible values in a standalone script. Nothing used
  the removed `::size-allocate` signal or baseline API.

- Visible by default: dropped all `show_all` calls (removed in GTK-4)
  and the redundant `show()` calls on non-toplevels (measurement labels,
  header labels, cell editors). Everything that must start or turn
  hidden was already handled by explicit `set_visible`/`hide` calls that
  run regardless (e.g. the floating status label is hidden by
  `show_message(None)`/`set_text(None)` right after the GTK-3 `show_all`
  sites), and the search dialog's `.ui` has explicit `visible=0` where
  needed, so no new hiding was added. Left as-is: `menu.py` `show_all`
  (GtkMenu item), `dialogs/open.py`/`save.py` `show_all` (their
  `_init_extra_widget` is built on the removed `set_extra_widget` and
  gets rewritten wholesale in the GtkFileChooser item — same goes for
  their `vbox.add`/`get_parent().remove` GtkContainer leftovers), and
  toplevel/dynamic `show()`/`hide()` calls, which exist in GTK-4 and are
  only deprecated since 4.10 (evaluate in the later deprecations pass).

- GtkWidget::draw + GtkTextView border windows (both removed in GTK-4,
  both used only by `ruler.py`): the line-length margin is now a
  `Gtk.Widget` subclass that draws in `do_snapshot` and is placed with
  `Gtk.TextView.set_gutter(RIGHT)` (in GTK since 4.0; Graphene added to
  the `gi.require_version` calls for `Gtk.Snapshot.translate`). Notable
  details:

  - GTK-4 caches the gutter's render node and does not redraw it on
    scrolling or typing (verified empirically), so the margin widget
    queues its own redraws on buffer "changed" and vadjustment
    "value-changed"; the adjustment is tracked via `notify::vadjustment`
    because the cell editor's text view has no scrolled window and the
    text edit dialog gets its scroller only after `prepare_text_view`.

  - Each length number is now positioned from its buffer line's real
    coordinates (`get_iter_location` + `buffer_to_window_coords`),
    replacing the old single joined layout and its "XXX: Lines overlap
    if we don't set a spacing!?" hack; numbers stay aligned regardless
    of line spacing and wrapping. Text color comes from
    `Gtk.Widget.get_color` (since 4.10, under our 4.12 floor). Verified
    visually with a standalone demo script; `test_ruler.py` can't run
    until `import gaupol` works again (blocked on the GtkToolbar item).

- Zebra stripes: `get_zebra_color` now returns the tree view's
  foreground color at 8% alpha (`Gtk.Widget.get_color`, since 4.10) and
  lets rendering composite it over the actual row background, instead of
  arithmetically blending 8% foreground into
  `lookup_color("theme_base_color")`. This drops the deprecated
  GtkStyleContext color API (clears the "revisit" note from the
  GtkStyleContext item) and stripes now work also on themes that don't
  define `theme_base_color`; the function no longer returns None.
  Verified visually in a standalone demo that `cell-background-rgba`
  respects alpha, on both light and dark themes.

- Icon sizes: the tab close button image now uses `Gtk.IconSize.NORMAL`
  (GTK-4 only has INHERIT/NORMAL/LARGE; NORMAL is the text-like size
  that MENU effectively was). The `set_icon_size(MENU)` calls on the
  preferences-dialog and custom-framerates inline toolbars were dropped:
  those "toolbars" are plain GtkBoxes since the `.ui` conversion and
  their symbolic button icons default to NORMAL anyway (ExtensionPage's
  `_init_toolbar` became empty and was removed). The two remaining
  `set_icon_size` calls (main toolbar, player toolbar) are real
  GtkToolbar API on win32-only paths and go away with the GtkToolbar
  rewrite item.

- GtkEntry/GtkSpinButton: only `TimeEntry` needed work. Its edit
  blocking moved from stopping the GtkEditable `insert-text`/
  `delete-text` signals to a `Gtk.EntryBuffer` subclass whose
  `do_insert_text`/`do_delete_text` vfuncs reject anything not
  explicitly allowed: the signals still exist and are stoppable in
  GTK-4, but PyGObject cannot marshal their in-out position argument,
  which would have printed the `g_value_get_int` assertion warning on
  every keystroke (this also clears the old TimeEntry warning from
  Deferred). The `cut-clipboard`/`toggle-overwrite` keybinding signals
  moved from GtkEntry to its GtkText delegate
  (`Gtk.Editable.get_delegate`, since 4.0). All TimeEntry behaviors
  (validation, overwrite typing, separator skip, digit zeroing, blocked
  delete, cut→copy redirect) verified in a standalone GTK-4 script;
  `pytest` remains blocked on `import gaupol` (GtkToolbar item). The
  SpinButton API we use is unchanged in GTK-4 and GtkSearchEntry is not
  used at all.

- Menubar + main toolbar: the menubar needed no code changes — GTK-4's
  `GtkApplicationWindow` renders the `Gtk.Application.set_menubar` model
  as a `GtkPopoverMenuBar` automatically when `show-menubar` is set, so
  the existing `menubar.ui` + `GMenu` section updates all keep working.
  The main toolbar (GtkToolbar, removed in GTK-4) was replaced with a
  GNOME HIG style `GtkHeaderBar` set as the window titlebar, with the
  menubar below it. Notable details:

  - Header bar contents: an Open split button (folder icon + arrow
    MenuButton whose menu is the *same* `GMenu` section object as File →
    Open Recent), a save button, a linked undo/redo pair, the default
    title widget (shows the window title, which `update.py` already
    maintains as filename/"Gaupol"), and find-and-replace + preview icon
    buttons on the right; window controls come automatically. Cut from
    the old toolbar: Insert, Remove and Video toggle — all still in the
    menubar.

  - The undo/redo history dropdowns are gone (the hover-highlight
    multi-undo UI can't be done with popover menus); undo/redo now flash
    "Undo: <action description>" via the FloatingLabel so it's clear
    what was reverted. All the `Gtk.Menu`/`Gtk.MenuItem` code in
    `agents/menu.py` went away with them.

  - Recent files are now listed by querying `Gtk.RecentManager` directly
    (filter by application + format mime types, MRU by modified time,
    honor `recent.show_not_found`, limit 10), replacing
    `GtkRecentChooserMenu` for both the split button and the two menubar
    sections. This also clears the "GtkRecentChooserMenu is gone" item.

  - A header bar can't be hidden like the toolbar could, so the View →
    Toolbar menu item, `toggle-main-toolbar` action, conf options
    `show_main_toolbar` and `toolbar_style`, and the `toolbar_styles`
    enum (built on removed `Gtk.ToolbarStyle`) were all removed. Stale
    keys in old config files are discarded on the next write; an old
    `toolbar_style` line prints a harmless one-time parse warning. The
    notebook separator, whose visibility was tied to the toolbar, was
    dropped too.

  - Verified visually (screenshot via `Gtk.WidgetPaintable` with the
    still-unmigrated notebook DnD calls stubbed out): header bar, linked
    groups, title and menubar all render correctly. Full runtime
    verification blocked on the remaining items (DnD, GtkIconTheme). The
    player toolbar in `agents/video.py` is still GtkToolbar — it's the
    remaining half of the "GtkToolbar has been removed" item.

- Player toolbar: now a `GtkBox` with the "toolbar" CSS class (the
  migration guide's replacement; an OSD overlay was considered and
  rejected — auto-hiding controls suit immersive playback, not editing,
  and would cover the subtitle overlay at the bottom of the video). Same
  buttons and order, separators dropped (the "toolbar" class spacing
  suffices), seekbar expands via `hexpand`. Completes the GtkToolbar
  item. Notable details:

  - Icon names switched to `-symbolic` variants out of necessity, not
    just style: current adwaita-icon-theme ships only symbolic icons and
    GTK-4 does *not* fall back from a plain name to its symbolic variant
    (verified: "media-playback-start" resolves to image-missing). The
    media icon base names are all freedesktop naming spec names and
    Adwaita has `-rtl` variants, so seek/skip icons flip automatically
    in RTL. See Deferred for auditing the remaining non-symbolic icon
    names elsewhere.

  - `volume_button.props.use_symbolic = False` dropped: broken for the
    same no-fullcolor-icons reason, and the property is deprecated since
    4.10 (GTK-4 default is True).

  - Verified visually with a standalone script that calls the real
    `_init_player_toolbar` on a stub master; in-app verification blocked
    on the deferred gtksink → gtk4paintablesink switch.

- Drag-and-drop: the notebook's URI drop (open dragged files) is now a
  `Gtk.DropTarget` (since 4.0) receiving `Gdk.FileList` (since 4.6,
  under our 4.12 floor); GTK deserializes `text/uri-list` drags into it,
  so drops from file managers keep working. The handler gets `Gio.File`s
  and uses `get_path()`, filtering out non-local files (the old code
  would have produced garbage paths for those anyway). This was the only
  DnD in the codebase (notebook tab reordering is internal to
  GtkNotebook). `import gaupol` works again as of this commit's
  predecessor state; runtime drop verification blocked on the next item
  (`Gtk.IconTheme.get_default` crashes app startup).

- GtkIconTheme: no `Gtk.IconTheme.get_for_display` port was needed — all
  three `get_default()` sites existed only to fall back from symbolic to
  non-symbolic icon names, which is backwards in GTK-4 (current Adwaita
  ships only symbolic icons; plain names are the broken ones and themes
  inherit Adwaita anyway). `gaupol/util.py` `get_icon_image` was removed
  and the tab close button creates its symbolic `Gtk.Image` directly;
  the `_init_toolbar` has_icon-fallback methods in
  `dialogs/preferences.py` and the custom-framerates extension were
  deleted, keeping the symbolic names from the `.ui` files. This clears
  the Python half of the deferred non-symbolic icon audit. Milestone:
  `bin/gaupol FILE` now starts and runs with zero console errors or
  warnings.

- GtkFileChooser API changes: moved to the GFile-based API —
  `set_current_folder`/`set_file` take a `Gio.File`, and the agents read
  `get_file()`/`get_files()`, converting with `get_path()` (non-local
  files filtered out where multiple can be selected). Notable details:

  - Decision: no `Gtk.FileChooserNative` (or 4.10's `Gtk.FileDialog`)
    anywhere. The open/save dialogs need real extra widgets (encoding/
    format combos with change handlers), which neither supports
    (`add_choice` is string-only with no signals), and FileChooserNative
    was seen broken in nfoview on GTK 4.10. For consistency, all file
    choosers stay `Gtk.FileChooserDialog` subclasses.

  - `set_extra_widget` is gone: the open/save dialogs' combo grids are
    appended to the dialog's content area, below the file chooser
    widget (verified visually). The throwaway `GtkWindow` wrappers in
    `open-dialog.ui`/`save-dialog.ui` were dropped — `main_vbox` is now
    a top-level builder object carrying its own 12px margins, which
    settles these dialogs' borders (part of the deferred border item).

  - Overwrite confirmation is automatic in GTK-4. The save dialog's
    hack of adding a missing filename extension before confirmation
    moved from the removed generic "event" signal on the save button
    (which crashed dialog init, see the cleared Deferred item) to a
    capture-phase `Gtk.GestureClick` on the same button. The Enter-key
    path adds the extension only in the response handler, after GTK's
    confirmation has checked the extensionless name — the same loophole
    existed in GTK-3, whose `stop_emission` + re-`response` dance also
    bypassed re-confirmation; that dance was dropped.

  - In SAVE mode, GTK-4's file chooser dialog automatically creates a
    header bar holding the name entry and moves the response buttons
    into it. Just a look change, everything keeps working, including
    `get_widget_for_response`.

  - `SaveDialog.set_name` with a path to a nonexistent file now sets
    only the basename; GTK-3 `set_current_name` received the full path
    and displayed it verbatim in the name entry.

  - Construction, extra-widget rendering and the set_name → format
    change → extension-adding → `get_file` flow verified with a
    standalone script (dialogs render correctly, screenshots checked);
    the full response flow through the agents is still blocked on
    `Gtk.Dialog.run` (the next, blocking-dialogs item). All dialog and
    agent unit tests pass. The whole GtkFileChooser family is
    deprecated since 4.10 in favor of `Gtk.FileDialog`; that's a
    case for the later deprecations pass, hampered by the extra widget
    need.

- Follow-up to the GtkFileChooser item: `open-dialog.ui` and
  `save-dialog.ui` were dropped and the extra widgets are now built in
  code in `_init_extra_widget`. The files contained only a static grid
  of labels and empty combos (all combo contents were already built in
  Python), and loading a fragment with a second `Gtk.Builder` into a
  foreign dialog was an odd pattern. Label strings are identical, so
  existing translations keep matching (`tools/extract-translations`
  globs both `.py` and `.ui`, no file lists to update). Rendering
  verified identical via screenshots; dialog tests pass.

- Blocking dialogs: `Gtk.Dialog.run` is gone; rather than rewriting all
  ~50 synchronous call sites (and the `gaupol.Default` exception
  unwinding built on their return values) into "response"-callback
  style, `gaupol.util.run_dialog` now blocks in a nested `GLib.MainLoop`
  until the "response" signal, preserving GTK-3 `run()` semantics. The
  async rewrite was rejected as an application-wide architecture change
  — and moot, since GtkDialog is deprecated since 4.10 and the dialog
  story gets revisited in the deprecations pass anyway. Notable details:

  - GTK-4 GtkDialog emits response `DELETE_EVENT` when the window is
    closed (verified empirically), so cancel-on-close keeps working. An
    "unrealize" handler also quits the loop, so it cannot hang if a
    dialog is destroyed mid-run without a response (the "destroy" signal
    is useless for this: it only fires once Python drops its reference).
    Handlers are disconnected after each run, so re-running the same
    dialog (open.py's retry loops) doesn't accumulate them.

  - `BuilderDialog.run` was removed; everything, including the ~24
    interactive `run_dialog` test helpers that called `dialog.run()`
    directly (mechanically converted), now goes through
    `gaupol.util.run_dialog`. `show_exception` now uses `flash_dialog`.

  - `flash_dialog(AboutDialog)` remains broken: GTK-4 GtkAboutDialog is
    not a GtkDialog and has no "response" signal — that's the next item,
    "Adapt to GtkAboutDialog API changes".

  - Verified with scripts: response/close/destroy semantics standalone,
    a BuilderDialog run twice through the shim, and the real in-app
    close-confirmation flow (MultiCloseDialog inside
    `application.close`: CANCEL keeps the page via `gaupol.Default`, NO
    closes it). App starts and runs with a clean console. This also
    clears the deferred item on the `run_dialog`-based test helpers.

- GtkAboutDialog: derives from GtkWindow in GTK-4, so it can't go
  through `flash_dialog`/`run_dialog` (no "response" signal). The help
  agent now keeps a single AboutDialog instance and `present`s it, with
  `set_hide_on_close(True)` — the same pattern as the search dialog and
  nfoview. All the `set_*` calls in `AboutDialog.__init__` exist
  unchanged in GTK-4; the init was just reordered to match nfoview.
  Verified the present/close-hides/re-present flow in-app with a script
  (after first testing the wrong code, see the `PYTHONPATH` note at the
  top of this file).

- MessageDialog: `format_secondary_text` is gone in GTK-4 (a removal not
  covered by the guide, found because every confirmation flow builds on
  the message dialogs); the four message dialog base classes now set the
  `secondary-text` property instead. This unbroke all
  Error/Info/Question/WarningDialog construction and their tests.

- GtkFileChooserButton: the multi-save dialog's folder selector is now
  the plain `GtkButton` left behind by the `.ui` conversion, renamed
  `directory_button` and made functional: its label shows the selected
  folder's basename and clicking opens a `Gtk.FileChooserDialog` in
  SELECT_FOLDER mode (per the earlier decision, no
  FileChooserNative/FileDialog) through
  `gaupol.util.run_dialog`, with the selected path kept in a
  `_directory` attribute. Minor look change: a regular centered button
  label instead of GtkFileChooserButton's icon + left-aligned text.
  Verified the click → select → label update and cancel-keeps-selection
  flows plus rendering (screenshot) with standalone scripts; dialog
  tests pass.

- Fixed a flaky `ValueError` in the search dialog's `replace()` (seen as
  an intermittent `test_replace` failure): the `page_changing` decorator
  set `_handle_page_changes` back to True unconditionally on exit, so
  when the text view's focus-leave handler (also decorated) ran nested
  inside `replace()` — dispatched from `iterate_main` in page.py's
  main-texts-changed handler — it re-enabled page-change handling early
  and the subsequent "page-changed" emission reset the match state
  mid-replace. GTK-4's `EventControllerFocus` delivers leave events via
  the main context (GTK-3 focus-out was synchronous at `grab_focus`
  time), which is what made the nesting possible. The decorator now
  saves and restores the previous flag value with try/finally.

- Fixed the test suite segfaulting under Wayland (GTK 4.22.4):
  destroying a window whose focus is in a `GtkText`, with no other
  window left in the process, and then showing a new window crashes in
  GTK's Wayland text-input code when a late input-method event arrives
  for the freed widget (first seen as `test_assistants.py` crashing in
  teardown after `TestLineBreakOptionsPage`, whose spin button entry
  holds focus). A new root `conftest.py` sets
  `GTK_IM_MODULE=gtk-im-context-simple` for tests, bypassing the Wayland
  text-input protocol. The app itself is not affected — its main window
  outlives all dialogs (verified: destroying a dialog with a focused
  entry while the main window persists is fine). Arguably a GTK bug,
  worth reporting upstream with the minimal reproduction.

- Milestone: full `pytest` run is stable and green apart from the
  spell-check failures covered by the Deferred item (4 failures + 26
  errors, all assume a working `SpellChecker`); `bin/gaupol` with one or
  several files runs with zero console output even under
  `G_ENABLE_DIAGNOSTIC=1`.

## Deferred

- Dialog borders were lost in the `.ui` conversion (`border_width` is
  gone in GTK-4): categorically, all dialogs should get GNOME
  HIG-compliant 18px borders, set as margins on the first child of the
  content area. Same for the sub-containers that carried their own 12px
  border: the preferences dialog's per-tab boxes and the search dialog's
  stack page boxes. It's the same four `set_margin_*` lines repeating,
  so probably warrants a `gaupol.util` function; the Python-built
  dialogs (encoding, multi-close, debug) should use it too. The open
  and save dialogs' extra widgets got their margins with the
  GtkFileChooser item; the multi-save dialog is a regular
  BuilderDialog and gets borders with the rest. The text-assistant
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

- Reimplement the "Italic" context menu item of the multiline cell
  editor with `Gtk.TextView.set_extra_menu` when doing the GtkMenu
  migration (Ctrl+I still works). Also verify that opening the default
  context menu in cell editors (text and time) doesn't cancel editing
  via the focus controller's "leave" — the old `populate-popup` +
  `_in_editor_menu` guard against that was removed.

- Audit the remaining non-symbolic icon names: current Adwaita ships
  only symbolic icons and GTK-4 doesn't fall back from plain names, so
  these likely render as image-missing. Remaining case: the
  `preferences-desktop`/`help-contents`/`help-about` icons in
  `preferences-dialog.ui` (the Python-side fallbacks were removed with
  the GtkIconTheme item).

- Rename `FloatingLabel` to Toast and restyle it with CSS to match the
  GNOME HIG toast look (rounded, floating at the bottom):
  <https://developer.gnome.org/hig/patterns/feedback/toasts.html> and
  <https://gnome.pages.gitlab.gnome.org/libadwaita/doc/1-latest/class.Toast.html>
  — without using libadwaita itself. Undo/redo now flash messages
  through it, so it's more visible than before.

- Verify at runtime that Ctrl+Page_Up/Down switches notebook tabs while
  the view has focus: the view's capture-phase key controller consumes
  those keys to block TreeView's paging bindings, which assumes GTK-4
  handles application accelerators at the window before the focus
  widget's controllers. If tab switching broke, rethink.
