@echo off
REM Double-click this file to run the project
cd /d "%~dp0"

REM ---------- 1. Find Python on this computer ----------
set PY=
py --version >nul 2>nul && set PY=py
if not defined PY python --version >nul 2>nul && set PY=python
if not defined PY (
    echo ERROR: Python is not installed on this computer.
    echo Install it from https://www.python.org and tick "Add python.exe to PATH".
    pause
    exit /b
)

REM ---------- 2. Create a virtual environment (first time only) ----------
REM If the folder was copied from another computer, it is rebuilt automatically
"venv\Scripts\python.exe" --version >nul 2>nul
if errorlevel 1 (
    echo Creating virtual environment, please wait...
    %PY% -m venv --clear venv
)

REM ---------- 3. Install libraries ----------
echo ==========================================
echo  Installing libraries (first time needs internet)...
echo ==========================================
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install libraries. Check the internet connection.
    pause
    exit /b
)

REM ---------- 3b. Windows security fix ----------
REM Some lab PCs block SQLAlchemy's compiled (.pyd) files.
REM If that happens, switch SQLAlchemy to its pure-Python version.
"venv\Scripts\python.exe" -c "import sqlalchemy.orm" >nul 2>nul
if errorlevel 1 (
    echo Applying Windows security fix for SQLAlchemy...
    powershell -NoProfile -Command "Get-ChildItem 'venv\Lib\site-packages\sqlalchemy' -Recurse -Filter '*_cy.*.pyd' | Rename-Item -NewName { $_.Name + '.blocked' }"
)

REM ---------- 4. Start the server ----------
echo.
echo ==========================================
echo  Starting server...
echo  Open in browser:  http://127.0.0.1:8000
echo  Do NOT close this window. Stop server: CTRL + C
echo ==========================================
"venv\Scripts\python.exe" -m uvicorn main:app --reload

pause
