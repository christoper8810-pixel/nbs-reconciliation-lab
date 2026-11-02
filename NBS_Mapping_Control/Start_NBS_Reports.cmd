@echo off
cd /d "%~dp0"
start "NBS reports" /b python -m nbs_control serve --port 8767 > data\launcher.log 2>&1
timeout /t 2 /nobreak > nul
start "" "http://127.0.0.1:8767/reports"
