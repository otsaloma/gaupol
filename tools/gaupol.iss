[Setup]
AllowNoIcons=yes
AppName=Gaupol
AppPublisher=Osmo Salomaa
AppPublisherURL=http://home.gna.org/gaupol/
AppVerName=Gaupol 0.16.1
Compression=lzma
DefaultDirName={pf}\Gaupol
DefaultGroupName=Gaupol
OutputBaseFilename=gaupol-0.16.1-win32
OutputDir=".."
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\*"; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Gaupol"; Filename: "{app}\gaupol.exe"
Name: "{group}\{cm:UninstallProgram,Gaupol}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Gaupol"; Filename: "{app}\gaupol.exe"; Tasks: desktopicon
