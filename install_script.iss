; Script Inno Setup para o instalador do App Caderneta

[Setup]
AppName=App Caderneta
AppVersion=1.1
DefaultDirName={autopf}\App Caderneta
DefaultGroupName=App Caderneta
OutputDir=.
OutputBaseFilename=Instalador_Caderneta
Compression=lzma
SolidCompression=yes
SetupIconFile=foto_icone.ico

[Files]
Source: "app_cardeneta.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "foto_fundo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "foto_icone.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "alerta.png"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\App Caderneta"; Filename: "{app}\app_cardeneta.exe"; IconFilename: "{app}\foto_icone.ico"
Name: "{group}\Desinstalar App Caderneta"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\app_cardeneta.exe"; Description: "Executar App Caderneta"; Flags: nowait postinstall skipifsilent