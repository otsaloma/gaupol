2020-04-10: Gaupol 1.8
======================

* Add action set start from video position (#148)
* Add and fix English spell-check special cases
* Add and fix OCR spell-check special cases
* Add Interlingue translation (OIS)
* Add Portuguese translation (Hugo Carvalho)
* Update translations

2019-08-04: Gaupol 1.7
======================

* New app icon, as full-color and symbolic SVGs (#119)
* Better initial preview experience (#136)
* Disable loading of problematic gstreamer-vaapi (#79)
* Use gspell for spell-check instead of PyEnchant and GtkSpell (#12)
* Use the reverse domain name "io.otsaloma.gaupol" for desktop file,
  appdata file and icons

2019-06-08: Gaupol 1.6
======================

* Add text correction pattern to unpack ligatures
* Don't show video files in recent file menus (#130)
* Update translations

2019-02-03: Gaupol 1.5
======================

* Add support for building a Flatpak
* Highlight changed parts in "Correct Texts" (#34)
* Add keybinding Ctrl+I for toggling italic (#118)
* Add keybinding Ctrl+I for toggling italic while editing (#118)
* Change keybinding for Invert Selection to Ctrl+J
* When opening multiple files, skip ones already open
* Adapt to various GTK deprecations
* Add 64x64 and 128x128 icons
* Update AppData XML file
* Bump iso-codes dependency to >= 3.67
* Update translations

2018-07-07: Gaupol 1.4.1
========================

* Fix TypeErrors due to video player pipeline queries failing (#78)
* Make 'setup.py --record' include compiled extensios as well (#91)

2018-05-01: Gaupol 1.4
======================

* Update the `--video-file` argument to not just select the video
  file, but also load it in the internal video player (#75)
* Fix subtitles with special characters not being displayed by
  the internal video player (#74)
* Fix seeking to selection start if at less than one second (#76)
* Fix pasting texts from outside Gaupol, e.g. from a text editor
* Update checks for required GStreamer elements (#73)
* Update translations

2017-11-12: Gaupol 1.3.1
========================

* Fix pattern file syntax to not be corrupted by msgfmt (#70)

2017-11-11: Gaupol 1.3
======================

* Use gtksink instead of autovideosink with the integrated video
  player, making it work on Wayland too (#60)
* Add a hidden preference to disable autoplay (#57)
* Allow loading video by drag-and-drop (#59)
* Fix missing icon in GNOME shell on Wayland (#62)
* Fix unhandled exception when adding recent menu items
* Fix video player actions being sensitive when playback
  initialization fails (#52)
* Fix Gaupol freezing after changing audio track (#58)
* Fix error quitting if a file is still being loaded (#54)
* Fix duplicate tags when decoding MPL2 (devcompl, #68)
* Install appdata XML file under /usr/share/metainfo
* Prefer iso-codes JSON files over XML files (#10)
* Bump GStreamer dependency ≥ 1.6
* Drop build dependency on intltool (use gettext instead, #13)
* Add donate button to about dialog
* Update translations

2017-04-23: Gaupol 1.2
======================

* Add support for the WebVTT file format (#46)
* Add support for the LRC file format (#39)

2017-03-18: Gaupol 1.1
======================

* Fix error when using the Save All As dialog to save all time-based
  format documents as frame-based or vice versa
* Fix unhandled exception when trying to write non-numeric data into
  integer or float cells
* Add Icelandic translation (Sveinn í Felli)
* Remove severely incomplete Catalan, Polish and Swedish translations
* Update translations

2016-10-29: Gaupol 1.0
======================

* Fix size of custom font with GTK 3.22 (#40)
* Show an error dialog if the integrated video player fails
  to initialize playback due to e.g. missing codecs
* Fix error trying to undo more actions than exist when holding down
  Ctrl+Z (#38)

2016-08-20: Gaupol 0.92
=======================

* Fix error saving document from a time-based format to a
  frame-based or vice versa ([#28][])
* Fix error clicking undo or redo button dropdown arrow when no
  document is yet open ([#29][])
* Fix action states after subtitle cell editing cancelled ([#30][])
* Fix recent file menu states to update correctly ([#31][])
* Fix save as dialog to always add filename extension ([#32][])
* Update AppData file
* Update translations

[#28]: https://github.com/otsaloma/gaupol/issues/28
[#29]: https://github.com/otsaloma/gaupol/issues/29
[#30]: https://github.com/otsaloma/gaupol/issues/30
[#31]: https://github.com/otsaloma/gaupol/issues/31
[#32]: https://github.com/otsaloma/gaupol/issues/32

2016-07-16: Gaupol 0.91
=======================

* Use header bars for dialogs
* Migrate from deprecated `Gtk.UIManager`, `Gtk.Action` etc.
  to `Gtk.Application`, `Gio.Action` etc.
* Add mpv for preview with precise seek (`--hr-seek=yes`)
* Make mpv the default preview video player on non-Windows systems
  and set the default preview offset to one second
* Make seek length configurable in the preferences dialog
* Add find and replace to the toolbar
* Have both Ctrl+F and Ctrl+H open the find and replace dialog
* Have both Ctrl++, Ctrl+- and numpad equivalents control volume
* Remove external video player output window (if you want to see
  that output, start Gaupol from a terminal)
* Use a monospace editing font by default
* Add support for IBM273, IBM1125, KOI8-T and KZ1048 character
  encodings (whether these are actually available depends on your
  version of Python)
* Drop the bookmarks extension
* Fix Cancel button behaviour when quitting Gaupol by closing the
  main window and having unsaved changes ([#14][])
* Fix line length measure em to be narrower ([#763589][])
* Have the text view right-click spell-check language menu
  set the language permanently
* Don't show the "Use Shift+Return for line-break" help message
  if it's likely to overlap with the text being edited
* Only force theme variant if `dark_theme` in config file is
  `true`, thus respecting any global settings ([#753315][])
* Make `GTK_THEME=Adwaita:dark gaupol` work correctly
* Move web pages to <http://otsaloma.io/gaupol/>
* Move releases to <https://github.com/otsaloma/gaupol/releases>
* Move bug tracker to <https://github.com/otsaloma/gaupol/issues>
* Move documentation to <https://github.com/otsaloma/gaupol/tree/master/doc>
* Close mailing lists, use Gitter instead: <https://gitter.im/otsaloma/gaupol>
* Use Transifex for translations: <http://www.transifex.com/otsaloma/gaupol/>
* Update AppData file
* Bump GTK dependency to ≥ 3.12
* Bump PyGObject dependency to ≥ 3.12
* Drop optional dependencies on PT fonts
* Add Serbian translation (Miroslav Nikolić)
* Update French translation (Jean van Kasteel)

[#14]: https://github.com/otsaloma/gaupol/issues/14
[#753315]: https://bugzilla.gnome.org/show_bug.cgi?id=753315
[#763589]: https://bugzilla.gnome.org/show_bug.cgi?id=763589

2015-05-16: Gaupol 0.28.2
=========================

* Fix text view size in spell check dialog

2015-05-09: Gaupol 0.28.1
=========================

* Have the spell-check dialog remember its size
* Work around a destructive override in gst-python that broke
  Gaupol's built-in video player ([#748813][])
* Update Hungarian translation (Andrássy László)
* Update French translation (RyDroid)
* Update Brazilian Portuguese translation (Rafael Ferreira, Felipe Braga)
* Update Czech translation (Pavel Fric)

[#748813]: http://bugzilla.gnome.org/show_bug.cgi?id=748813

2014-12-08: Gaupol 0.28
=======================

* Add target in the position shift dialog to shift subtitles
  from selection to end ([#734198][])
* Center tab labels
* Fix mouse use in the cell text editor to not cause losing focus
  and thus cancelling editing
* Fix bookmarks not being cleared when a file with bookmarks
  is closed ([#740481][])
* Remove buggy `text-shadow` use from CSS ([#740527][])
* Use markdown for documentation files (`README` etc.)
* Update Spanish translation (Carlos Mella)

[#734198]: http://bugzilla.gnome.org/show_bug.cgi?id=734198
[#740481]: http://bugzilla.gnome.org/show_bug.cgi?id=740481
[#740527]: http://bugzilla.gnome.org/show_bug.cgi?id=740527

2014-10-27: Gaupol 0.27
=======================

* Hide tabs when only one tab is open
* Expand tabs to fill window width, use 24 characters at minimum
* Fix dialog paddings with GTK 3.14
* Fix text view line length display with GTK 3.14
* Pack video player toolbar and seekbar horizontally
* Avoid column resizing upon opening file
* Fix `IndexError: list index out of range` when undoing or redoing
  by holding Ctrl+(Shift)+Z pressed
* Remove use of deprecated stock items, `Gtk.Alignment`,
  `gi.types.Boxed.__init__` and non-transient dialogs
* Update Spanish translation (Carlos Mella)

2014-06-21: Gaupol 0.26
=======================

* Update file selection dialogs to work better with GTK 3.12
* Default toolbar style to icons only (due to `gtk-toolbar-style`
  being deprecated since GTK 3.10)
* Allow using the dark GTK theme variant (you need to edit
  `~/.config/gaupol/gaupol.conf` to enable this)
* Fix errors and lack of updates in multiline text cells and their
  line length calculation and display (#728575)
* Fix initially incorrect row heights after opening a file
* Fix updating subtitle numbers when inserting or removing subtitles
* Fix overlapping column header right-click menus
* Fix saving enumeration values to configuration file
* Use `Gtk.render_layout` instead of deprecated `Gtk.paint_layout` to
  render line length margin in text views
* Remove header editing dialog
* Remove non-functional speech recognition menu item
  (see <http://www.mail-archive.com/gaupol-list@gna.org/msg00069.html>)
* Drop support for the MPsub format
* Add GTK (3.2 or greater) to list of dependencies in the `README`
  file (GTK has always been a dependency, its explicit mention was
  just forgotten when migrating from PyGTK to PyGObject)
* Update Brazilian Portuguese translation (Rafael Ferreira)
* Update Czech translation (Pavel Fric)

2014-02-08: Gaupol 0.25
=======================

* Depend on GtkSpell 3.0.0 or later instead of pygtkspellcheck
  for inline spell-check
  - http://gtkspell.sourceforge.net/
* Clarify GStreamer dependency as "at least the core,
  gst-plugins-base and gst-plugins-good; and for good container and
  codec support preferrably each of gst-plugins-bad, gst-plugins-ugly
  and gst-libav" (#710138)
* Check that required GStreamer elements can be found and
  print error messages if not (#710138)
* Filter open recent menu items by mimetype
* Fix search dialog "Ignore case" option
* Fix text correction assistant layout with GTK 3.10
* Fix newline handling on Windows (Python 3 does implicit conversions
  that were not accounted for)
* Fix preview error dialog on Windows (#651675)
* Fix video selection dialog on Windows (#654523)
* Fix miscellaneous small Windows-specific issues
* Rewrite Windows installer build scripts (thanks to TumaGonx Zakkum
  for pygi-aio binaries and Gian Mario Tagliaretti for a template
  cx\_Freeze setup script)
* Update Spanish translation (Carlos Mella)

2013-10-06: Gaupol 0.24.3
=========================

* Fix preferences dialog subtitle and time overlay connections

2013-10-06: Gaupol 0.24.2
=========================

* Make AppData file translatable
* Fix broken string formatting in the French translation that caused
  `KeyError`s handling encoding names (#709335)

2013-09-22: Gaupol 0.24.1
=========================

* Possibly fix floating status label colors on non-Adwaita themes
* Add an AppData XML file
  - http://people.freedesktop.org/~hughsient/appdata/
* Add French translation (RyDroid)
* Update Czech translation (Pavel Fric)

2013-07-22: Gaupol 0.24
=======================

* Add action to set the end time from video position
  (see also <https://wiki.gnome.org/Apps/Gaupol/CreatingSubtitles>)
* Use a floating label for the statusbar
* Show search dialog messages in a floating label
  in the search dialog
* Use inline toolbars in the preferences dialog
  - https://wiki.gnome.org/Design/HIG/InlineToolbars
* Apply GNOME Goal: Add keywords to application desktop files
  - https://wiki.gnome.org/GnomeGoals/DesktopFileKeywords
* Hide translation text column by default and show only when a
  translation file is opened or the column is explicitly selected
  to be shown
* Remove video toolbar (video file and framerate selectors)
* Add a framerate selector to save dialogs (shown only when
  converting from a time-based file format to a frame-based
  or vice versa)
* Change a couple keybindings
* Move "Select Video" from the file menu to the tools menu (below
  "Preview") to clarify that it relates to the external preview
* Add Galician translation (Leandro Regueiro)
* Update Spanish translation (Carlos Mella)

2013-06-26: Gaupol 0.23
=======================

* Add a built-in GStreamer-based video player
* Add a not-required, but recommended dependency on PT fonts
  (PT Sans Caption and PT Mono) used by default for video player's
  subtitle and timecode overlays
  - http://www.paratype.com/public/
* Bump PyGObject dependency to version 3.6.0 or later
* Fix `KeyError` tearing down extension on quit (#702518)
* Update Spanish translation (Carlos Mella)

2013-04-09: Gaupol 0.22
=======================

* Restore drop-down arrows on undo and redo toolbar buttons for those
  using PyGObject 3.7.90 or greater (#686608)
* Restore almost proper keeping track of recent files for those using
  PyGObject 3.7.4 or greater (#678401, #695970)
* Restore zebra-stripes, which were previously discarded by some
  GTK themes
* Mostly fix cell rendering speed issues with GTK 3.6 and later
* Add Czech translation (Pavel Fric)

2013-01-13: Gaupol 0.21.1
=========================

* Fix error disconnecting text view's line length margin handler
  (`AttributeError: 'TextView' object has no attribute
  'gaupol_ruler_handler_id'`)
* Fix atomic file writing in weird cases where the subtitle file to
  be written and its backup in the same directory would be on
  different filesystems (Florian Léger, Osmo Salomaa)
* Fix speed issues updating subtitle list selection (e.g. when doing
  a search-and-replace-all with a alot of matches)
* Speed up action sensitivity updates

2012-12-02: Gaupol 0.21
=======================

* Restore inline spell-check, replace the previous GtkSpell
  dependency with a dependency on pygtkspellcheck
  - http://koehlma.github.com/projects/pygtkspellcheck.html
* Add partial support for fancy Unicode dashes, ellipses and
  quotation marks in text correction patterns and "Toggle dialogue
  dashes" action
* Fix search dialog mnemonics
* Apply GNOME Goal: Remove markup in translatable messages

2012-11-11: Gaupol 0.20.1
=========================

* Fix crash on startup on newer versions of PyGObject and/or GTK
  resulting from setting tool item types (#686608)
* Fix side pane header menu (#686312)
* Disable "Join or Split Words" task in the text correction assistant
  if no spell-check dictionaries are available (#686340)
* Use a stock GTK close icon for tab close buttons if
  "window-close-symbolic" is not found
* Fix behaviour of spell-check dialog's "Replace with" entry

2012-10-14: Gaupol 0.20
=======================

* Migrate to Python 3, GTK 3, GStreamer 1.0, PyGI and GNOME 3
* Bump Python dependency to 3.2 or greater
* Replace PyGTK dependency with PyGObject 3.0.0 or greater
* Bump optional GStreamer dependency to 1.0 or greater
* Disable inline spell-checking while waiting for introspection
  support to be added to GtkSpell
  - https://bugzilla.redhat.com/show_bug.cgi?id=675504
* Disable speech recognition while waiting for pocketsphinx to be
  ported to GStreamer 1.0
  - https://sourceforge.net/projects/cmusphinx/forums/forum/5471/topic/5497616
* Rewrite line-breaking algorithm to use a Knuth-Plass-style flexible
  system of penalties and a versatile measure of goodness
* Write subtitle files in a proper atomic manner (on Windows this
  is fully atomic only with Python 3.3 or later)
* Ellipsize tab labels in the middle (#686099)
* Remove `-c`/`--config-file` option (you're better off setting `XDG_*`
  environment variables if you're doing something weird)
* Add 48x48 and 256x256 pixel PNG icons and remove SVG icon
* Fix bug in saving a temporary file for preview (#685706)
* Fix signatures of decorated functions in API documentation
* Use filename extension `.extension` for extension metadata files
  (instead of previous `.gaupol-extension`)
* Use filename extension `.bookmarks` for bookmark files written by
  the bookmarks extension (instead of previous `.gaupol-bookmarks`)
* Release source tarballs only compressed as `tar.xz` (instead
  of the previous `tar.gz` and `tar.bz2`)
* Update Brazilian Portuguese translation
  (Átila Camurça, Darlildo Lima)
* Update Hungarian translation (Andrássy László)
* Update Spanish translation (Carlos Mella)

2011-11-26: Gaupol 0.19.2
=========================

* Allow preview of unsaved documents (#661242)
* Use subtitles from selected range if applicable in the Transform
  Positions dialog (#663158)
* Fix mplayer preview command to work if gaupol was started as a
  background process (with &) from a terminal window (#660035)
* Fix `TypeError` when speech recognition stopped in the middle of a
  subtitle
* Fix `IndexError` when speech recognition finished with no speech
  detected (#659411)
* Fix `UnicodeDecodeError` when reading configuration file (#661123)
* Rename `manifest` directory in source tarball to avoid clashes with
  `MANIFEST` file on case-insensitive filesystems

2011-09-07: Gaupol 0.19.1
=========================

* Fix gettext initialization in aeidon package to not make global
  changes (Olivier Aubert, Osmo Salomaa, Debian bug #639668)
* Fix speech recognition advance length handling so that subtitles
  don't start too early
* Update Russian translation (Alexandre Prokoudine)

2011-07-17: Gaupol 0.19
=======================

* Add speech recognition to allow generating subtitles from video
  - http://wiki.gnome.org/Apps/Gaupol/SpeechRecognition
* Fix installation of custom-framerates extension
* Add optional dependency on gst-python (this also implies a
  dependency on one or more of gst-plugins-base, gst-plugins-good,
  gst-plugins-ugly, gst-plugins-bad, gst-ffmpeg depending on what
  video and audio formats are being used)
  - http://gstreamer.freedesktop.org/
* Add optional dependency on pocketsphinx
  - http://cmusphinx.sourceforge.net/
* Add gaupol-i18n mailing list for translators
* Update Spanish translation (Carlos Mella)
* Update Hungarian translation (Andrássy László)

2011-05-30: Gaupol 0.18
=======================

* Add extension that allows use of custom framerates (#637503)
* Add "Get more extensions" button to the preferences dialog
* Relax SubRip file parsing in unambiguous cases (#634129)
* Fix saving of last used directory in file dialogs with "paths that
  cannot be represented as a local filename" (#649347)
* Add Brazilian Portuguese translation (Átila Camurça,
  Darlildo Souza)
* Update German translation (Chris Leick)

2011-04-10: Gaupol 0.17.2
=========================

* Add framerate 24.0 fps found on Blu-rays and use three decimals for
  all framerates (#580345)
* Fix broken inheritance of action classes, which caused Gaupol to
  fail to start with recent versions of (Py)GTK (#643958)
* Fix previewing of changes in position shift and transformation
  dialogs
* Fix eternal loop when opening translation files and having
  existing zero-duration subtitles
* Fix names of filetype filters in open dialog
* Update author email address
* Move development repository from Gitorious to GitHub
  (https://github.com/otsaloma/gaupol)
* Abandon use of Transifex for translations
* Add Turkish translation (Koray Löker and Çağlar Kilimci)

2010-11-07: Gaupol 0.17.1
=========================

* Fix search dialog replace button to change sensitivity without
  delay to avoid concurrent replacements (#626976)
* Save text assistant window size
* Show line lengths in text assistant confirmation page
* Hopefully fix spell-check not working on Windows (#623864)
* Build Windows installer without UI translations to avoid a partly
  translated mess (especially due to pygtk bug #574520)
* Add Hebrew translation (Yaron Shahrabani)
* Update Hungarian translation (Andrássy László)
* Update Spanish translation (Carlos Mella)

2010-07-05: Gaupol 0.17
=======================

* Add "Save All As" (under the Projects menu) to save all open
  documents with selected properties (fixes #595685)
* Add an inline spell-check for editable multiline text fields (off
  by default, can be activated in the preferences dialog)
* Add support for milliseconds (field `$MILLISECONDS`) in preview
  commands. Allows use of Media Player Classic for preview.
* Add help button in the preferences dialog, clickable in the
  preview tab to launch web browser to view wiki documentation
* Use reading speed (characters per second) instead of optimal
  duration (seconds per character) in duration adjust dialog
* Fix writing subtitle file headers with chosen newlines
* Fix reading and writing extension configurations
* Fix minor i18n issues with individual strings
* Add optional dependency of PyGtkSpell (part of gnome-python-extras)
* Add `--mandir` global option to `setup.py` to allow installation of
  man pages to somewhere else than `.../share/man` (fixes #620665)
* Add Finnish translation

2010-06-22: Gaupol 0.16.2
=========================

* Fix "Quit" and Close All" to ask to save unsaved changes
* Update Russian translation (Алекс)
* Update Hungarian translation (Andrássy László)

2010-06-09: Gaupol 0.16.1
=========================

* Add support for a variant of the TMPlayer format with two-digit
  hours, i.e. time strings of form HH:MM:SS:
* Fix cropped close icons on tabs
* Fix `AttributeError` related to locale functions on Windows
* Fix launching web browser on Windows
* Clarify dependencies of aeidon and gaupol in `README.aeidon`
* Add Russian translation (Алекс)

2010-06-03: Gaupol 0.16
=======================

* Split general-purpose, user-interface-independent subtitle editing
  code to a separate Python package called "aeidon" while keeping the
  GTK user interface code under the package "gaupol". Allow
  installation of these two packages separate of one another.
  Developers and packagers are encouraged to read `./setup.py --help`
  message and the file `README.aeidon`. (Fixes #595809 and should
  allow fixing the likes of Debian bug #569983.)
* Save menu item keybindings to a GtkAccelMap rc-file in the user's
  configuration directory
* Have the interactive search look for times instead of subtitle
  numbers if the search string contains a colon (fixes #609176)
* Add miscellaneous Latin common error corrections patterns
* Add help menu item to browse wiki documentation at
  <http://wiki.gnome.org/Apps/Gaupol>
* Increase size of line length superscripts shown in list cells
* Fix focus changing when pasting subtitles
* Use `gtk.RecentAction` for recent file menus (fixes #615372 and
  probably #608951)
* Work around a subprocess error launching video player on Windows
  systems, which resulted in `TypeError: environment can only contain
  strings` (fixes #605805)
* Fix handling of Unicode BOMs that broke as a result of a hasty fix
  for subtitle file reading functions for 0.15.1
* Fix hearing impaired text removal pattern "Speaker before a colon"
  to not remove too much (fixes #618529)
* Apply GNOME Goal: Correct Desktop Files
* Migrate from Glade to GtkBuilder
* Use attributes instead of markup in GtkBuilder files
* Fix GtkBuilder constructed buttons to respect user preferences
  regarding whether or not to show icons in buttons
* Use Python's JSON module instead of ConfigObj and Validate for
  reading and writing configuration files
* Use enchant's user spell-check dictionaries (usually stored in
  `$HOME/.config/enchant`) instead gaupol-specific ones
* Use copies of iso-codes XML files shipped with gaupol only as a
  fallback if they are not found under `/usr/share/xml/iso-codes`
* Add global options `--with-iso-codes` and `--without-iso-codes` to
  `setup.py` to control whether or not to install iso-codes XML files
  (This means that packagers can use `--without-iso-codes` and mark the
  iso-codes package as a hard dependency to avoid duplicate files)
* Probably fix i18n issues with Unicode ellipses of menu items
* Fix i18n issues with locale codes and their fallbacks used in
  pattern files for "Name" and "Description" fields
* Raise Python dependency to 2.6
* Raise PyGTK dependency to 2.16
* Raise PyEnchant dependency to 1.4.0

2010-03-24: Gaupol 0.15.1
=========================

* Fix complete breakage of opening subtitle files due to a change in
  newline handling of `codecs.open` in Python 2.6.5
* Use existing subtitle file mime-types instead of text/plain when
  adding files to the recent files database
* Add German translation (Chris Leick)
* Add Hungarian translation (László Andrássy)

2009-05-15: Gaupol 0.15
=======================

* Add text correction task to split joined words or to join split
  words using spell-check suggestions (#572667)
* Show duration in time mode as seconds
* Merge Latin and French common error text correction patterns from
  subtitleeditor (kitone)
* Allow pasting times with comma as a decimal separator (#580339)
* Allow bookmarks to be added or removed by double-clicking or
  pressing enter in the bookmark column (#580346)
* Add validation for character encoding given as an argument on the
  command line using the `-e` option
* Fix handling of Unicode BOMs (#568906)
* Add UTF-8-SIG character encoding for opening and saving files
  with a UTF-8 signature/BOM
* Fix incorrect handling of common error patterns that at worst
  caused gaupol to hang due to an eternal loop (#581003)
* Abort installation if an `intltool-merge` or `msgfmt` call fails
* Add messages for raised exceptions

2009-04-13: Gaupol 0.14
=======================

* Add an extension system (documentation to follow later)
* Add two extensions: side pane and bookmarks
* Adher to the home directory part of freedesktop.org's
  XDG Base Directory Specification
* Handle reading and writing files with a UTF-8 BOM (#556956)
* Save SSA and ASS files with `\N` linebreaks instead of `\n`
* Resize columns after running text corrections
* Make removing a large amount of subtitles significantly faster
* Fix `GtkWarning: GtkSpinButton: setting an adjustment with
  non-zero page size is deprecated`
* Remove deprecated Encoding-field from desktop file
* Fix search dialog to not modify obsolete data (#572676)
* Fix character count error with Unicode text
* Fix updating of filenames in the projects menu
* Fix erroneous cleaning of SubRip markup after removing hearing
  impaired subtitles
* Fix open dialog file filter to list files with upper- and mixed
  case extensions as well
* Fix AssertionError when installing multiple times
* Switch version-control systems from subversion to git

2008-09-17: Gaupol 0.13.1
=========================

* Fix error saving subtitle files when trying to quit with unsaved
  changes in multiple documents (#552129)
* Add all open projects as a target to the position shift dialog
* Remove redundant tags with the SubRip format when doing automatic
  text corrections, e.g. removing hearing impaired texts

2008-08-30: Gaupol 0.13
=======================

* Raise PyGTK dependency to 2.12 or greater
* Remove misuse of assertions that broke some parts of Gaupol, when
  used with Python's optimization (`-O` switch)
* Preserve additional fields in SSA/ASS files
* Preserve coordinate fields in extended SubRip format
* By default always use UTF-8 character encoding for preview
  (#522868, Beni Cherniavsky, Osmo Salomaa)
* Allow reordering of columns
* Resize columns when their visibility is toggled
* Allow comments (starting with number signs) in pattern files
* Allow grouping of correction patterns under the same name
* Improve commmon error patterns for spaces around quote marks
* Fix error with encoding auto-detection (#10278)
* Fix error starting spell-check if no dictionary (#10526)
* Fix preview error dialog if video player not found (#518981)
* Fix subtitle number search after subtitle removals or inserts
* Fix error displaying right-click menu in cells (kitone)
* Fix IndexError with multiline tags in text cells (#547170)
* Fix window type and transientness for preferences dialog
* Fix error closing the search dialog from the window titlebar
* Fix updating of Alt+NUM shortcut keys
* Fix color markup tag conversions with various formats
* Fix conversions of font tags with the SubRip format
* Replace `--adapt-translation` option with `--align-method`
* Replace `--debug` option with using environment variable
  `GAUPOL_DEBUG`
* Add GenericName field to the desktop file
* Add mimetypes application/x-subrip, text/x-microdvd,
  text/x-mpsub, text/x-ssa and text/x-subviewer to the desktop file
* Fix spell-check language listing with recent versions of Enchant
* Run `update-desktop-database` in `setup.py` if `--root` not given
* Move profile directory on Windows to `%APPDATA%/Gaupol`

The five digit bug numbers refer to the old bug tracker at Gna
and the six digit ones to the new bug tracker at GNOME Bugzilla.

2007-11-03: Gaupol 0.12.3
=========================

* Fix error in splitting frame-based subtitle projects (#10200)
* Fix `UnboundLocalError` with preview (#10203)

2007-10-20: Gaupol 0.12.2
=========================

* Fix tag conversions that removed text (#10140)
* Fix spacing issues in open and save dialogs

2007-10-02: Gaupol 0.12.1
=========================

* Fix text correction assistant's capitalization task
* Fix remaining `NameError`s with function arguments (#10034)

2007-09-29: Gaupol 0.12
=======================

* Add a capitalization task to the text correction assistant
* Add "All supported files" filter to the open dialog
* Fix error saving after splitting project (#10041)
* Fix `NameError`s with lambda functions (#10034)
* Fix error opening SubRip file if the first line is blank (#10054)
* Fix markup tooltip hack to work with (Py)GTK 2.12
* Remove license page from the Windows installer
* Include iso-codes with the Windows installer

2007-09-14: Gaupol 0.11
=======================

* Add a line-break task to the text correction assistant
* Add menu-items and keybindings for extending the current
  selection up to the first or the last subtitle without moving
  focus or scrolling (#9895)
* Add missing "Auto-detected" encoding entry in the file dialogs
* Save search history to `$HOME/.gaupol/search` instead of the
  configuration file to avoid quoting problems
* Enable rubber-banding (selection of multiple rows by dragging
  the mouse) in the subtitle list
* Add support for creating a Windows `.exe` with py2exe and a
  Windows installer with Inno Setup

2007-08-20: Gaupol 0.10
=======================

* Add a common error correction task for the text assistant
* Fix default values of two configuration variables
* Fix a selection bug in the text assistant confirmation page
* Fix tag parsing error with multiple sets of tags on one line
* Fix text cell renderer font sizes on Windows
* Fix web browser launch on Windows
* Fix recent file URI handling on Windows
* Fix preview on Windows
* Fix temporary file removals on Windows

2007-08-07: Gaupol 0.9
======================

* Raise Python dependency to 2.5.1 or greater (#9685, this
  should have been done already for 0.8.)
* Add a text correction assistant (Tools / Correct Texts)
* Add a hearing impaired text removal task for the text
  correction assistant
* Fix notification issue, which caused at least that in some cases
  the tab labels and the window title didn't update
* Add quoting for number signs in the configuration file to avoid
  them being misinterpreted as in-line comments
* For reading and writing non-xml files in `$HOME/.gaupol`, always
  try the locale encoding first and if it fails, use UTF-8

2007-07-09: Gaupol 0.8
======================

* Python dependency raised to 2.5 or greater
* PyGTK dependency raised to 2.10 or greater
* License changed to GPL v3 or later
* Configuration file backend and syntax changed; old configurations
  are discareded
* Line lengths optionally shown on all text elements
* Allow negative values in time and frame cells
* Better (more preserving) handling of blank lines as well as
  leading and trailing spaces when opening files
* Fixed numerous bugs with find and replace, especially when
  searching for zero-length regular expressions
* Notify of invalid regular expressions when searching (#6690)
* Regular expression searches are now always MULTILINE and DOTALL
* Search notifications moved to main window's statusbar
* Migrated to `gtk.RecentManager` and `gtk.RecentChooser`
* Added a menu for recent translation files
* Added "Text" menu to replace "Format", "Search" and part of "Edit"
* Simplified and changed several keycombos
* Tabs can now be freely reordered
* Added more informative tooltips on tabs
* Fixed cropped close button images on tabs
* Redesigned search and spell-check dialogs
* Redesigned position tranformation dialog to be less tall
* Faster updates when inserting and removing subtitles
* Subtitle number search now starts only on numeric key-presses
* Use per-stream options (`:option` instead of `--option`) in default
  VLC preview command
* Subtitle file and video file paths in preview commands are now
  automatically escaped and quoted
* Use exact framerates in calculations (e.g. 24000/1001) and rounded
  integers in the user interface (e.g. 24)
* Splitting a subtitle no longer duplicates texts
* Position shift amount now always defaults to zero
* Fixed a bug in the time entry validation
* Fixed sensitivity of "Adjust Positions..." menu item (#7255)
* Show confirmation dialog when closing a file that no longer exists
* Applied GNOME Goal #3: Remove "Application" category from
  desktop files
* Changed icon colors have a bit more contrast
* SRTX support dropped
* Added `--config-file`, `--debug`, `--encoding`, `--list-encodings`,
  `--translation-file`, `--adapt-translation`,  `--video-file` and
  `+[NUM]` options
* Added a manual page to document all options
* Fixed translatable strings with multiple arguments in python files
  to use named fields and mappings
* Source code directory structure changed
* Uninstallation feature removed

2006-09-18: Gaupol 0.7.1
========================

* Fixed cell renderers to work with GTK and PyGTK 2.10
* Fixed MicroDVD tag conversion errors (Bug #6938)
* Fixed issue of disappearing tags when converting case
* Polish (pl)

2006-07-11: Gaupol 0.7.0
========================

* Append file
* Split project
* Fixed error opening file if no locale encoding set (bug #6319)
* Catch `OSError` in case saving file fails and temporary backup copy
  is restored (bug #6316)
* Fixed error launching preview if no column focused
* Improved blank line handling of subtitle merge
* `setup.py`: `AUTHORS`, `COPYING` and `README` files no longer
  installed

2006-07-07: Gaupol 0.6.0
========================

* Subtitle split and merge
* Smarter translation file opening
* Show `.srtx` files as images
* Support TMPlayer subtitle file format
* Copy-paste now works from one project to another
* Fixed target radio button defaults in case of no selection
* Changed some keybindings
* `setup.py`: Fixed paths module generation in case `--root` option
  given with a trailing directory separator

2006-06-28: Gaupol 0.5.0
========================

* Find and replace, including regular expressions
* Character encoding auto-detection
* Support MPlayer's MPsub subtitle file format
* New icon, as both PNG and SVG
* Applied GNOME Goal 2.1: Install theme-friendly icons
* Icon field in the desktop file no longer contains extension
* Warning dialog displayed if opening unsorted file
* Separate, locally overridable, header template files
* Support MicroDVD headers ("{DEFAULT}{}{...}" lines)
* Time decimal changed from comma (",") to period (".")
* Framerate conversion available for time-based subs as well
* Dialogs are again resizable to be smaller
* Fixed spell-check recursion bugs
* Fixed bug #6235: double-click on subtitle item cause exception
* "Unselect All" menu item removed
* "Save A Copy..." menu items removed
* Unified target specifications in dialogs
* Spell-check suggestion list now scrolls to top with new word
* Gaupol no longer hangs if video player not closed before exit
* Debug dialog no longer fails to start if PyEnchant not installed
* Video selection dialog's file filter now defaults to video
* Support default browsers on KDE and Mac OSX as well
* Better video player defaults on Windows
* Testing framework made compatible with py.test
* Desktop file strings are now translated in .po files
* Developer-specific options to gaupol made into separate scripts
* `setup.cfg` no longer specifies prefix or optimization
* Added clean command to `setup.py`
* General polish here and there
* Psyco no longer used
* New optional dependency of Universal Encoding Detector (chardet)
* Polish (pl)

2006-05-04: Gaupol 0.4.1
========================

* #5880: Framerate conversion returns an error
* Miguel Latorre: Spanish (es)

2006-03-10: Gaupol 0.4.0
========================

* Time shift
* Time adjustment
* Duration adjustment
* Framerate conversion
* Partial support for SSA & ASS formats
* Various errors in Micro DVD tag conversions
* Newline counted as a character in text length statusbar
* Rounding errors when undoing after having edited in unnative mode
* Template header not written when converting to SubViewer 2.0 format
* Distutils commands `sdist` and `bdist_*` broken
* Gil Forcada: Catalan (ca)

2006-01-22: Gaupol 0.3.4
========================

* Support SubViewer 2.0 format
* Start-up fails if PyEnchant is not installed
* Spell-check "Join Forward" button does not work

2006-01-20: Gaupol 0.3.3
========================

* Preview current data instead of saved file
* Allow selecting arbitrary video file
* New toolbar for video
* New window for video player output
* Pre-configured commands for more than one video player
* Spell-check not working with new PyEnchant releases 1.1.4 and 1.1.5
* File marked unchanged after saving a copy of it
* Overwrite dialog not always presented when saving
* Open button on the main toolbar missing tooltip
* Open dialog not always defaulting to directory of last opened file

2006-01-12: Gaupol 0.3.2
========================

* #5046: MPlayer freezes in preview

2006-01-11: Gaupol 0.3.1
========================

* Save file before preview only if the file is changed
* Have the spell-check dialog use the customizable editor font

2006-01-10: Gaupol 0.3.0
========================

* Preview function
* Smarter dialog sizes
* Spell-check menu- and toolbar items grayed out when shouldn't
* Unexpected exits return value 0
* Exception not raised when version check fails on `IOError`
* Toggling dialog lines fails if document is unsaved
* Italicization menu item not grayed out when document is unsaved

2006-01-02: Gaupol 0.2.0
========================

* Spell-check
* Debug dialog
* Ability to try multiple character encodings when opening a file
* Opening multiple files at once with the open dialog
* Moving to edit an adjacent cell with Alt+Arrow keys
* Smarter uninstallation
* PyGTK dependency raised to 2.8
* Introduced PyEnchant 1.1.3 dependency
* Introduced optional iso-codes dependency
* Finnish (fi) translation removed

Lots of code has been redesigned and rewritten. Most importantly the
undo/redo system, the configuration module and all GUI building and updating
functions have been rewritten. Separation between base and gtk modules is now
far more sensible and should better suit possible alternative user
interfaces.

2005-08-27: Gaupol 0.1.1
========================

* Bug #2816: Settings not being saved.
* Write correct version number to config file.

2005-08-25: Gaupol 0.1.0
========================

Initial release.
