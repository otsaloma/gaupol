; -*- conf-windows -*-
[Setup]
AllowNoIcons=yes
AppName=Gaupol
AppPublisher=Osmo Salomaa
AppPublisherURL=http://home.gna.org/gaupol/
AppVerName=Gaupol 0.24.3.20131111
Compression=lzma
DefaultDirName={pf}\Gaupol
DefaultGroupName=Gaupol
OutputBaseFilename=gaupol-0.24.3.20131111-win32
OutputDir=".."
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\build\exe.win32-3.3\*"; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commonprograms}\Gaupol"; Filename: "{app}\gaupol.exe"
Name: "{commondesktop}\Gaupol"; Filename: "{app}\gaupol.exe"; Tasks: desktopicon
