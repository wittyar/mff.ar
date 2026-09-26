; Instalador de TA GUIANAEL MFF (Inno Setup 6).
;
; Lo arma el workflow publicar.yml en Windows, después de `python desktop/construir.py programa`:
;   iscc /DAppVersion=X.Y.Z desktop\instalador.iss
;
; Se instala en la carpeta del usuario (%LOCALAPPDATA%\Programs\TA GUIANAEL MFF), sin pedir
; permisos de administrador: así los parches de versión pueden reemplazar el programa. Los
; datos (capa.json, respaldos, datos del juego, imágenes) van aparte, en
; %LOCALAPPDATA%\TA GUIANAEL MFF, y desinstalar no los toca.
;
; AppId no cambia nunca: es lo que hace que una versión nueva se instale encima de la anterior.

#ifndef AppVersion
  #error Falta /DAppVersion=X.Y.Z
#endif
#define AppName "TA GUIANAEL MFF"

[Setup]
AppId={{AF76651F-DF0F-413F-9497-DAEEF15D1557}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher=wittyar
AppPublisherURL=https://github.com/wittyar/mff.ar
VersionInfoVersion={#AppVersion}
PrivilegesRequired=lowest
DefaultDirName={autopf}\{#AppName}
DisableProgramGroupPage=yes
DisableDirPage=yes
OutputDir=..\dist
OutputBaseFilename=TA-GUIANAEL-MFF-{#AppVersion}
SetupIconFile=mff.ico
UninstallDisplayIcon={app}\desktop\mff.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "escritorio"; Description: "Crear un acceso directo en el escritorio"

[Files]
Source: "..\dist\programa\*"; DestDir: "{app}"; Excludes: "__pycache__"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userprograms}\{#AppName}"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\desktop\lanzador.py"""; WorkingDir: "{app}"; IconFilename: "{app}\desktop\mff.ico"
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\desktop\lanzador.py"""; WorkingDir: "{app}"; IconFilename: "{app}\desktop\mff.ico"; Tasks: escritorio

[Run]
Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\desktop\lanzador.py"""; WorkingDir: "{app}"; Description: "Abrir {#AppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Lo que Python y los parches dejan en la carpeta del programa (__pycache__, archivos nuevos).
Type: filesandordirs; Name: "{app}"
