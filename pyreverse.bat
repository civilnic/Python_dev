@echo off
rem Use python to execute the python script having the same name as this batch
rem file, but without any extension, located in the same directory as this
rem batch file
REM set PATH="C:\Program Files (x86)\Graphviz2.38\bin";%PATH%

set dossier_courant=%~dps0

set script_path=C:\Python35-32\Scripts
%script_path%\pyreverse.exe -o png -p BDS -S %dossier_courant%\BDS
%script_path%\pyreverse.exe -o png -p A429 -S %dossier_courant%\A429
%script_path%\pyreverse.exe -o png -p FLOT -S %dossier_courant%\FLOT
%script_path%\pyreverse.exe -o png -p MEXICO -S %dossier_courant%\MEXICO
%script_path%\pyreverse.exe -o png -p FDEF -S %dossier_courant%\FDEF


pause

REM python "%~dpn0" %*
