@echo off
rem NBS Mapping Studio update rollback. No administrator rights or internet needed.
setlocal
cd /d "%~dp0"
title NBS Mapping Studio update rollback
set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY where py >nul 2>nul && set "PY=py -3"
if not defined PY (
  echo Python 3.10 or newer is required. It is the same Python that runs NBS Mapping Control.
  echo Install it for the current user from https://www.python.org/downloads/ and tick "Add python.exe to PATH".
  pause
  exit /b 1
)
%PY% "%~dp0patch_engine.py" rollback %*
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" echo Rollback did not complete - see the messages above and the backup folder named there.
if "%RC%"=="0" echo Finished. The log is in the application folder under patch_logs.
pause
exit /b %RC%
