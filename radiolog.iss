; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!


#define MyAppName "RadioLog"
#define MyAppVersion "3.11.3"
#define MyAppPublisher "Nevada County Sheriff's Search and Rescue"
#define MyAppURL "https://www.nevadacountysar.org"
#define MyAppExeName "RadioLog.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{1A8B41F6-3C88-41A6-B46D-5B51A4C5AE34}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf}\{#MyAppName}
UsePreviousAppDir=no
DisableProgramGroupPage=yes
LicenseFile=dist\radiolog\LICENSE.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=dist\
OutputBaseFilename=radiolog-{#MyAppVersion}-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
;PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\radiolog\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\radio.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\radio.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep:TSetupStep);
begin
	if CurStep = ssPostInstall then
		if not RegKeyExists(HKLM,'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Acrobat.exe') then
			MsgBox('PDF Print Notice'+#13#10#13#10+'It looks like Adobe Acrobat is not installed.'+#13#10#13#10+'PDF files will still be generated and saved by RadioLog, but a default PDF viewer application, other than a web browser, must be installed in order to send those generated PDF files to a printer.'+#13#10#13#10+'Adobe Acrobat Reader is just one option.  It can be installed from get.adobe.com/reader.'+#13#10#13#10+'If you do have Acrobat or a different PDF viewer application installed, please try printing from RadioLog to confirm.',mbInformation,MB_OK);
end;