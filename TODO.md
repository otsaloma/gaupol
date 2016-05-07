Gaupol 1.0
==========

* [ ] Use header bars for dialogs
* [x] Add mpv for preview with precise seek (`--hr-seek=yes`)
* [x] Make mpv the default preview video player on non-Windows systems
      and set the default preview offset to one second
* [x] Only force theme variant if `dark_theme` in config file is
      `true`, thus respecting any global settings [#753315][]
* [x] Update AppData file
* [x] Remove external video player output window (if you want to see
      that output, start Gaupol from a terminal)
* [x] Add support for IBM273, IBM1125, KOI8-T and KZ1048 character
      encodings (whether these are actually available depends on your
      version of Python)
* [x] Bump GTK+ dependency to 3.12 or greater
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
* Test mpv
* Use CSS instead of `modify_font`
* Fix remaining deprecations (see `python3 -Wd bin/nfoview`)
* Use margin-start instead of deprecated margin-left
* Set the default font to monospace?
* https://wiki.gnome.org/Projects/gspell

Infrastructure:

* Move web pages otsaloma.io
* Close GNOME Bugzilla
* Move release to GitHub
* Use Travis CI
* Use Transifex
* Use Gitter
* Remove GNOME wiki pages
* Close mailing lists
