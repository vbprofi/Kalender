@echo off
setlocal

set current=%~dsp0
set upx=C:\Users\pc\Documents\portable\upx\upx-3.96-win64

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

rem https://stackoverflow.com/questions/14624245/what-does-a-version-file-look-like

call .py\Scripts\activate.bat
::pyinstaller --onedir --noconsole --windowed --strip --upx-dir=%upx% main.py --version-file version.txt
pyinstaller --onefile --noconsole --windowed --strip --upx-dir=%upx% main.py --version-file version.txt
pause