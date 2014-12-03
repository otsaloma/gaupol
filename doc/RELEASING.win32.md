Preparing to Build Windows Installers
=====================================

 * Install the latest Python 3.x.
 * Install Python for Windows Extensions (pywin32)
 * Install setuptools
 * Install PyGObject all-in-one for Windows (pygi-aio)
   - Fix GTK+3 theming for Windows
     * .../site-packages/gnome/etc/gtk-3.0/settings.ini

    [Settings]
    gtk-button-images = 0
    gtk-font-name = Verdana 8
    gtk-icon-theme-name = gnome
    gtk-menu-images = 0
    gtk-theme-name = Adwaita

 * Install chardet compatible with Python 3
 * Install PyEnchant
   - Check DLLs for conflicts with those in pygi-aio
 * Install cx_Freeze and Inno Setup

Releasing a New Version for Windows
===================================

 * On a Unix system with proper tools available
   - Remove all po-files since translations are difficult
   - Generate translated data files
     * `python3 setup.py clean install_data -d /tmp`
 * Copy the gaupol directory to a Windows system
 * Run tools/winbuild.bat
 * Run tools/winrun.bat to test that it works
   - If needed, enable a console window to see output
     * winsetup.py: `s/base="Win32GUI"/base=None/`
 * Compile tools/winbuild.iss with Inno Setup
 * Install Gaupol and check that it works
 * On a Unix system, sign (`gpg --detach`) and upload

Known Issues
============

 * Integrated video player needs some Windows-specific work
 * Most fonts look bad; default set to Verdana
 * Links don't open (`Gtk.LinkButton` etc.)
 * The installer contains a whole lot of unnecessary stuff
