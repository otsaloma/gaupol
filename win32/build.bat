:: -*- coding: us-ascii-unix -*-
cd "%~dp0\.."
set PATH=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Python34
python setup.py clean
python setup.py install_data -d build\usr
python winsetup.py build > winsetup.log
del /s /q build\exe.win32-3.4\share\gir-1.0 > NUL
del /s /q build\exe.win32-3.4\share\locale > NUL
