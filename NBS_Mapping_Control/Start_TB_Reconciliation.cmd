@echo off
rem NBS Mapping Control - whole-TB migration reconciliation (Windows). No administrator rights or internet needed.
cd /d "%~dp0"
where python >nul 2>nul || (echo Python 3.10 or newer is required: https://www.python.org/downloads/ - install for the current user and tick Add to PATH. & pause & exit /b 1)
python -c "import flask, openpyxl, lxml" >nul 2>nul && goto run
set "WHEELS=%~dp0wheels"
if not exist "%WHEELS%" set "WHEELS=%~dp0exports\transfer\wheels"
echo Installing Flask, openpyxl and lxml for the current user from "%WHEELS%" (offline) ...
python -m pip install --user --no-index --find-links "%WHEELS%" -r requirements.txt
python -c "import flask, openpyxl, lxml" >nul 2>nul && goto run
echo Offline install did not cover this Python version. Trying the internet / configured mirror ...
python -m pip install --user -r requirements.txt
python -c "import flask, openpyxl, lxml" >nul 2>nul || (echo Packages could not be installed. See TB_RECON_GUIDE.md section 1. & pause & exit /b 1)
:run
echo Opening http://127.0.0.1:8765/tb  - keep this window open while you work.
start "" "http://127.0.0.1:8765/tb"
python -m nbs_control serve --port 8765
