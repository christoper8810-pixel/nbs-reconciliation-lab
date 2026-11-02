@echo off
cd /d "%~dp0"
echo Close the black NBS server window before applying this update.
where py >nul 2>nul
if errorlevel 1 (python "%~dp0apply_update.py") else (py -3 "%~dp0apply_update.py")
pause
