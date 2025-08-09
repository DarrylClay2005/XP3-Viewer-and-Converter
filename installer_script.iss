
[Setup]
AppName=XP3 Viewer and Converter
AppVersion=1.0.2
DefaultDirName={pf}\XP3 Viewer and Converter
DefaultGroupName=XP3 Viewer and Converter
UninstallDisplayIcon={app}\XP3_Viewer_Converter.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=XP3_Viewer_Converter_v1.0.2_Setup

[Files]
Source: "dist\XP3_Viewer_Converter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "xp3_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XP3 Viewer and Converter"; Filename: "{app}\XP3_Viewer_Converter.exe"; WorkingDir: "{app}"; IconFilename: "{app}\xp3_icon.ico"
Name: "{group}\Uninstall XP3 Viewer and Converter"; Filename: "{uninstallexe}"
Name: "{commondesktop}\XP3 Viewer and Converter"; Filename: "{app}\XP3_Viewer_Converter.exe"; WorkingDir: "{app}"; IconFilename: "{app}\xp3_icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\XP3_Viewer_Converter.exe"; Description: "Launch XP3 Viewer and Converter"; Flags: nowait postinstall skipifsilent
