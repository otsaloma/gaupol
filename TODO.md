Gaupol 1.0
==========

* [x] Add mpv for preview with precise seek (`--hr-seek=yes`)
* [x] Make mpv the default preview video player on non-Windows systems
      and set the default preview offset to one second
* [x] Only force theme variant if `dark_theme` in config file is
      `true`, thus respecting any global settings [#753315][]
* [x] Update AppData file
* [x] Add Serbian translation (Miroslav Nikolić)
* [x] Update French translation (Jean van Kasteel)

[#753315]: https://bugzilla.gnome.org/show_bug.cgi?id=753315

XXX:

* Restore speech recognition (#757743)
* Make `GTK_THEME=Adwaita:dark gaupol` work correctly
* Have the text view right-click spell-check language menu
  set the language permanently
* Move the "Use Shift+Return for line-break" instruction so that
  it doesn't obstruct what is being edited
* Add seek length to preferences dialog? (or something else)
* Apply new GNOME goals and migrate away from deprecated widgets
    - <http://wiki.gnome.org/HowDoI/>
* Resolve or move open bugs
* Profile opening a subtitle file
* Remove GNOME wiki pages
* Test mpv

Gaupol 2.0
==========

* Allow using multiple dictionaries for spell-check
* Add a GStreamer-based audio waveform display
