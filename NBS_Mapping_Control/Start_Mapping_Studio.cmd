@echo off
rem NBS Mapping Studio (Windows). Uses the bundled portable Python when present. No administrator rights or internet needed.
cd /d "%~dp0"
set "PY="
set "PYARGS="
for %%P in ("%~dp0portable\python.exe" "%~dp0..\portable\python.exe" "%~dp0..\..\portable\python.exe" "%~dp0..\..\..\portable\python.exe") do if not defined PY if exist %%P set "PY=%%~P"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY where py >nul 2>nul && set "PY=py" && set "PYARGS=-3"
if not defined PY (echo Python 3.10 or newer is required: https://www.python.org/downloads/ & pause & exit /b 1)
"%PY%" %PYARGS% -c "import flask, openpyxl" >nul 2>nul && goto run
set "WHEELS=%~dp0wheels"
if not exist "%WHEELS%" set "WHEELS=%~dp0exports\transfer\wheels"
echo Installing Flask and openpyxl for the current user from "%WHEELS%" (offline) ...
"%PY%" %PYARGS% -m pip install --user --no-index --find-links "%WHEELS%" -r requirements.txt
"%PY%" %PYARGS% -c "import flask, openpyxl" >nul 2>nul || (echo Packages could not be installed. See MAPPING_STUDIO_GUIDE.md. & pause & exit /b 1)
:run
echo Opening http://127.0.0.1:8765/studio  - keep this window open while you work.
start "" "http://127.0.0.1:8765/studio"
"%PY%" %PYARGS% -m nbs_control.studio_app --port 8765
