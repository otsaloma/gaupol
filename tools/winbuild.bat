:: -*- coding: us-ascii-dos -*-
cd "%~dp0\.."
set GAUPOL_FREEZING=1
set PATH=%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;
set PYTHON=C:\Python33\python.exe
del /s /q build build.log
%PYTHON% setup.py install_data -d build\usr
%PYTHON% winsetup.py build > winsetup.log
:: Remove some of the biggest fucking junk included
:: in the all-one package, but not needed by gaupol.
del /s /q build\exe.win32-3.3\lib\gegl* ^
          build\exe.win32-3.3\lib\gstreamer* ^
          build\exe.win32-3.3\lib\libgda* ^
          build\exe.win32-3.3\lib\gedit ^
          build\exe.win32-3.3\lib\goffice* ^
          build\exe.win32-3.3\share\fonts ^
          build\exe.win32-3.3\share\gtk-doc ^
          build\exe.win32-3.3\share\gtksourceview* ^
          build\exe.win32-3.3\share\libgda* ^
          build\exe.win32-3.3\share\libwmf ^
          build\exe.win32-3.3\share\locale ^
          build\exe.win32-3.3\share\poppler ^
          build\exe.win32-3.3\share\gedit ^
          build\exe.win32-3.3\share\webkitgtk-3.0 ^
          build\exe.win32-3.3\libchamplain*.dll ^
          build\exe.win32-3.3\libclutter*.dll ^
          build\exe.win32-3.3\libgda*.dll ^
          build\exe.win32-3.3\libgedit*.dll ^
          build\exe.win32-3.3\libgegl*.dll ^
          build\exe.win32-3.3\libgoffice*.dll ^
          build\exe.win32-3.3\libgst*.dll ^
          build\exe.win32-3.3\libgucharmap*.dll ^
          build\exe.win32-3.3\libpoppler*.dll ^
          build\exe.win32-3.3\libtelepathy*.dll ^
          build\exe.win32-3.3\libwebkitgtk*.dll ^
          build\exe.win32-3.3\libwmf*.dll

pause
