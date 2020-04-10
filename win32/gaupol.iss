; -*- conf -*-

[Setup]
AppName=Gaupol
AppVerName=Gaupol 1.8
AppPublisher=Osmo Salomaa
AppPublisherURL=https://otsaloma.io/gaupol/
DefaultDirName={pf}\Gaupol
DefaultGroupName=Gaupol
AllowNoIcons=yes
OutputDir=".."
OutputBaseFilename=gaupol-1.8-win32
Compression=lzma
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\build\exe.win32-3.4\*"; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commonprograms}\Gaupol"; Filename: "{app}\gaupol.exe"
Name: "{commondesktop}\Gaupol"; Filename: "{app}\gaupol.exe"; Tasks: desktopicon
