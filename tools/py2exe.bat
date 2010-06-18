:: Build a Windows distribution of Gaupol and include
:: all necessary dependencies in that distribution.
cd "%~dp0\.."
rmdir /S /Q build dist
set GTKDIR=%SYSTEMDRIVE%\gtk+
set PYDIR=%SYSTEMDRIVE%\python26
%PYDIR%\python.exe winsetup.py py2exe
xcopy %GTKDIR%\etc dist\etc /s /i /y
xcopy %GTKDIR%\lib\*.dll dist\lib /s /i /y
xcopy %GTKDIR%\lib\*.dll.a dist\lib /s /i /y
xcopy %GTKDIR%\share\icons\hicolor\*.theme dist\share\icons\hicolor /i /y
xcopy %GTKDIR%\share\locale dist\share\locale /s /i /y
xcopy %GTKDIR%\share\themes dist\share\themes /s /i /y
xcopy %PYDIR%\Lib\site-packages\enchant\libenchant*.dll dist /i /y
xcopy %PYDIR%\Lib\site-packages\enchant\lib dist\lib /s /i /y
xcopy %PYDIR%\Lib\site-packages\enchant\share dist\share /s /i /y
pause
