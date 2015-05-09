Gaupol 0.28.1
=============

 * [X] Have the spell-check dialog remember its size
 * [X] Work around a destructive override in gst-python that broke
       Gaupol's built-in video player ([#748813][])
 * [X] Update Hungarian translation (Andrássy László)
 * [X] Update French translation (RyDroid)
 * [X] Update Brazilian Portuguese translation (Rafael Ferreira, Felipe Braga)
 * [X] Update Czech translation (Pavel Fric)

 [#748813]: http://bugzilla.gnome.org/show_bug.cgi?id=748813

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
