; -*- conf -*-

[Setup]
AllowNoIcons=yes
AppName=Gaupol
AppPublisher=Osmo Salomaa
AppPublisherURL=http://otsaloma.io/gaupol/
AppVerName=Gaupol 0.90.20160708
Compression=lzma
DefaultDirName={pf}\Gaupol
DefaultGroupName=Gaupol
OutputBaseFilename=gaupol-0.90.20160708-win32
OutputDir=".."
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\build\exe.win32-3.4\*"; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commonprograms}\Gaupol"; Filename: "{app}\gaupol.exe"
Name: "{commondesktop}\Gaupol"; Filename: "{app}\gaupol.exe"; Tasks: desktopicon
