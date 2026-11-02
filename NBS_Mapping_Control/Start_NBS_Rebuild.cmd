@echo off
rem NBS mapping control - start (Windows). Works without internet access.
cd /d "%~dp0"
where python >nul 2>nul || (echo Python 3.10 or newer is required: https://www.python.org/downloads/ & pause & exit /b 1)

rem Packages: use what is installed, else the bundled offline copies in .\wheels, else the internet.
python -c "import flask, openpyxl, lxml" >nul 2>nul
if errorlevel 1 (
  echo Installing Flask, openpyxl and lxml from the bundled wheels folder ^(no internet needed^) ...
  python -m pip install --user --no-index --find-links "%~dp0wheels" -r requirements.txt
  python -c "import flask, openpyxl, lxml" >nul 2>nul
  if errorlevel 1 (
    echo Offline install did not cover this Python version. Trying the internet ...
    python -m pip install --user -r requirements.txt
  )
)
python -c "import flask, openpyxl, lxml" >nul 2>nul || (echo Packages could not be installed. See INSTALL.md, section "No internet / proxy". & pause & exit /b 1)

rem First start: open the Sources page to choose your files; afterwards open the rebuild home page.
if exist data\bank_20260930.sqlite (set PAGE=nbs) else (set PAGE=nbs/load)
echo Opening http://127.0.0.1:8765/%PAGE%  - keep this window open while you use the tool.
start "" "http://127.0.0.1:8765/%PAGE%"
python -m nbs_control serve --port 8765
