# Dialog Look & Feel & Layout Modernization

## Guidelines

Follow the GNOME Settings style: sections as cards, built with
`GtkListBox` using the `rich-list` style class.

Some of our dialogs are excessive in providing keyboard accelerator
labels, explanatory labels etc. As part of modernization, simplify
where we can: drop caption labels, mnemonics and other chrome that
don't pull their weight when the controls are self-explanatory in
context (see the insert dialog: just a spin button and an Above/Below
toggle pair, no labels).

### Sections

- A section is a bold title label plus a `GtkFrame` whose child is a
  `GtkListBox` with `selection_mode=none`, `show_separators=1` and the
  `rich-list` style class. This replaces both `GtkTreeView` lists and
  the old indented-box sections (bold label + `margin_start` box).

- 12px spacing between the title and the frame, and between sections;
  18px margins around the dialog content. No `margin_start` indents.

- Drop separators (`show_separators`) if they don't pull their weight,
  e.g. between a control group and a closely related trailing row.

### Rows

- Rows are `GtkListBoxRow` with `activatable=0` and `selectable=0`; the
  actual control inside handles interaction.

- Label + control rows: the row child is a plain `GtkBox` with a caption
  label (`halign=start`, usually `hexpand=1`) pushing right-aligned
  controls to the end at their natural size. The theme's `.rich-list >
  row > box { border-spacing: 12px }` provides internal spacing — no
  explicit `spacing` needed on the row box.

- Caption labels: no trailing colons, normal color. Use `dim-label` for
  secondary *content* (e.g. displayed subtitle text), not for captions.
  Keep mnemonics (`use_underline`, `mnemonic_widget`).

- Radio/check groups: one `GtkCheckButton` per row, `hexpand=1`,
  `focusable=1`. Radios via the `group` property.

- Buttons inside rows: icon-only symbolic icon (e.g.
  `media-playback-start-symbolic`) with a translatable `tooltip_text`,
  `valign=center`, at the end of the row.

### Lists Built in Code

- For dynamic lists (e.g. languages), build the rows in Python in an
  `_init_*` method. Attach identifying data directly to the widget as a
  Python attribute (e.g. `radio.gaupol_locale = locale`) instead of
  keeping a parallel list; read it back in the signal handler.

### Sizing and Scrolling

- Prefer natural sizes; avoid fixed pixel sizes and
  `scale_to_content`-style sizing.

- If content can grow tall, wrap the content box in a
  `GtkScrolledWindow` (`hscrollbar_policy=never`,
  `propagate_natural_width/height=1`) and cap `max_content_height` in
  Python from a measured reference column plus the content box's
  top/bottom margins (see `LanguageDialog._init_scroller`).

- Entries: set `max_width_chars` alongside `width_chars` — otherwise the
  natural width is GTK's default of roughly 150 px regardless of
  `width_chars`. Center-align fixed-format values (times, frames) with
  `set_alignment(0.5)`.

### CSS

- App-wide tweaks go in `data/ui/gaupol.css`, e.g. the gap between a
  check/radio indicator and its label in rich-lists (6px, with
  `:dir(ltr)`/`:dir(rtl)` variants since GTK CSS has no logical margin
  properties).

- The `rich-list` styling itself comes from GTK's built-in Default
  (Adwaita) theme and works in light, dark and high-contrast variants.

- `gaupol.css` is loaded by `gaupol.Application`, so plain dialog
  construction (unit tests!) doesn't load it. Dialog tests must call
  `gaupol.style.load_css(self.dialog)` in `setup_method` so that
  pytest-based visual inspection matches the real app.

### Verification

- The user handles visual inspection themselves. Only do
  screenshot-based visual inspection if really necessary for the task
  at hand, not categorically or just in case.

### Naming

- Give descriptive ids to widgets referenced from Python (`content_box`,
  not `vbox2`). Purely structural containers can keep their generated
  names until touched.

## Progress

- [ ] gaupol/assistants.py
- [x] gaupol/dialogs/about.py
- [x] gaupol/dialogs/append.py
- [x] gaupol/dialogs/debug.py
- [x] gaupol/dialogs/duration_adjust.py
- [x] gaupol/dialogs/encoding.py
- [x] gaupol/dialogs/file.py
- [x] gaupol/dialogs/framerate_convert.py
- [x] gaupol/dialogs/insert.py
- [x] gaupol/dialogs/language.py
- [x] gaupol/dialogs/message.py
- [x] gaupol/dialogs/multi_close.py
- [ ] gaupol/dialogs/multi_save.py
- [x] gaupol/dialogs/open.py
- [x] gaupol/dialogs/position_shift.py
- [x] gaupol/dialogs/position_transform.py
- [ ] gaupol/dialogs/preferences.py
- [ ] gaupol/dialogs/preview_error.py
- [x] gaupol/dialogs/save.py
- [ ] gaupol/dialogs/search.py
- [ ] gaupol/dialogs/spell_check.py
- [x] gaupol/dialogs/split.py
- [x] gaupol/dialogs/text_edit.py
- [x] gaupol/dialogs/video.py
