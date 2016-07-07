Gaupol 0.91
===========

* [x] Use header bars for dialogs
* [x] Migrate from deprecated `Gtk.UIManager`, `Gtk.Action` etc.
      to `Gtk.Application`, `Gio.Action` etc.
* [x] Add mpv for preview with precise seek (`--hr-seek=yes`)
* [x] Make mpv the default preview video player on non-Windows systems
      and set the default preview offset to one second
* [x] Make seek length configurable in the preferences dialog
* [x] Add find and replace to the toolbar
* [x] Have both Ctrl+F and Ctrl+H open the find and replace dialog
* [x] Have both Ctrl++, Ctrl+- and numpad equivalents control volume
* [x] Remove external video player output window (if you want to see
      that output, start Gaupol from a terminal)
* [x] Use a monospace editing font by default
* [x] Add support for IBM273, IBM1125, KOI8-T and KZ1048 character
      encodings (whether these are actually available depends on your
      version of Python)
* [x] Drop the bookmarks extension
* [x] Fix Cancel button behaviour when quitting Gaupol by closing the
      main window and having unsaved changes (#14)
* [x] Fix line length measure em to be narrower [#763589][]
* [x] Have the text view right-click spell-check language menu
      set the language permanently
* [x] Only force theme variant if `dark_theme` in config file is
      `true`, thus respecting any global settings [#753315][]
* [x] Make `GTK_THEME=Adwaita:dark gaupol` work correctly
* [ ] Move web pages to <http://otsaloma.io/gaupol/>
* [x] Move releases to <https://github.com/otsaloma/gaupol/releases>
* [x] Move bug tracker to <https://github.com/otsaloma/gaupol/issues>
* [ ] Move documentation to <https://github.com/otsaloma/gaupol/tree/master/doc>
* [x] Close mailing lists, use Gitter instead: <https://gitter.im/otsaloma/gaupol>
* [x] Update AppData file
* [x] Bump GTK+ dependency to ≥ 3.12
* [x] Bump PyGObject dependency to ≥ 3.12
* [x] Drop optional dependencies on PT fonts
* [x] Add Serbian translation (Miroslav Nikolić)
* [x] Update French translation (Jean van Kasteel)

[#14]: https://github.com/otsaloma/gaupol/issues/14
[#753315]: https://bugzilla.gnome.org/show_bug.cgi?id=753315
[#763589]: https://bugzilla.gnome.org/show_bug.cgi?id=763589
