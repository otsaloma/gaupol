Gaupol 0.28
===========

 * [X] Add target in the position shift dialog to shift subtitles
       from selection to end ([#734198][])
 * [X] Center tab labels
 * [X] Fix mouse use in the cell text editor to not cause losing focus
       and thus cancelling editing
 * [X] Fix bookmarks not being cleared when a file with bookmarks
       is closed ([#740481][])
 * [X] Remove buggy `text-shadow` use from CSS ([#740527][])
 * [X] Use markdown for documentation files (`README` etc.)
 * [X] Update Spanish translation (Carlos Mella)

[#734198]: https://bugzilla.gnome.org/show_bug.cgi?id=734198
[#740481]: https://bugzilla.gnome.org/show_bug.cgi?id=740481
[#740527]: https://bugzilla.gnome.org/show_bug.cgi?id=740527

Gaupol 1.0
==========

 * Use CSS for zebra colors (public named colors added in GTK+ 3.14!)
     * http://bugzilla.gnome.org/show_bug.cgi?id=709617#c1
     * http://git.gnome.org/browse/gtk+/tree/gtk/theme/Adwaita
 * Apply new GNOME goals and migrate away from deprecated widgets
   - http://wiki.gnome.org/Initiatives/GnomeGoals/PortToGMenu
   - http://wiki.gnome.org/Initiatives/GnomeGoals/PortToGtkApplication
   - http://wiki.gnome.org/HowDoI/
 * Get rid of unnecessary dialog action areas
 * Allow using multiple dictionaries for spell-check
 * Add a GStreamer-based audio waveform display
