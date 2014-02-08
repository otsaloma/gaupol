:: -*- coding: us-ascii-unix -*-
cd "%~dp0\.."
set GAUPOL_FREEZING=1
set PATH=%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;
set PYTHON=C:\Python33\python.exe
del /s /q build winsetup.log
%PYTHON% setup.py install_data -d build\usr
%PYTHON% winsetup.py build > winsetup.log
:: Remove translations and gstreamer for now.
del /s /q build\exe.win32-3.3\share\locale
del /s /q build\exe.win32-3.3\lib\gstreamer*
del /s /q build\exe.win32-3.3\libgst*.dll
pause
