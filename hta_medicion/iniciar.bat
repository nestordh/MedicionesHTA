@echo off
setlocal

set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

if exist "%APP_DIR%venv\Scripts\pythonw.exe" (
    start "" "%APP_DIR%venv\Scripts\pythonw.exe" "%APP_DIR%iniciar.pyw"
) else (
    start "" pythonw.exe "%APP_DIR%iniciar.pyw"
)
