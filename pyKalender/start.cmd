@echo off
setlocal

set current=%~dsp0
set gitdir="C:\Users\pc\Documents\portable\git"
set path=%gitdir%\cmd;%path%
git config core.editor notepad

rem set HOME=%cd%/home
rem git --cd-to-home

rem git config --global user.name "Joe Sixpack"
rem git config --global user.email joe.sixpack@g_mail.com

echo "Konfiguration speichern im GIT-Ordner...."
git config --system user.name "vbprofi"
git config --system user.email vb-profi@mail.ru
git config --system core.autocrlf true

rem Passe diesen Pfad an, wenn sich Python an einem anderen Ort befindet
set "PYTHON_PATH=C:\Users\pc\AppData\Local\Programs\Python\Python312"

rem Füge den Python-Installationspfad zur PATH-Umgebungsvariable hinzu
set "PATH=%PYTHON_PATH%;%PATH%"

rem Optional: Setze die PYTHONHOME-Umgebungsvariable
set "PYTHONHOME=%PYTHON_PATH%"

rem Optional: Füge den Python-Scripts-Ordner zur PATH-Umgebungsvariable hinzu
set "PATH=%PYTHON_PATH%\Scripts;%PATH%"

rem Hier kannst du Python-Code ausführen, um sicherzustellen, dass alles funktioniert
python --version

echo Python-Umgebungsvariablen wurden erfolgreich gesetzt.


REM Git Version anzeigen
git --version
echo.

REM Zeige den letzten Commit (kurzer Log-Eintrag)
echo Letzter Commit:
git log -1 --pretty=format:"%%s %%n %%h %%n %%ad"
echo.

REM Zeige die zuletzt bearbeiteten Dateien
echo Zuletzt bearbeitete Dateien:
git show --name-only --pretty=format:"" HEAD
echo.

REM Letzter Tag-Eintrag anzeigen (Tag, Tag-Nachricht und Datum)
echo Letzter Tag-Eintrag:
git describe --tags --abbrev=0
git log --pretty=format:"%%s %%n %%ad" --date=short -1 --tags
echo.

REM Anzahl der Commits anzeigen
echo Anzahl der Commits:
git rev-list --count HEAD
echo.


call .py\Scripts\activate.bat
cmd
