@echo off
setlocal EnableDelayedExpansion

rem =========== Metadata ===========
set VERSION=v0.0.1
set AUTHOR=Sukarna Jana
set LAST_UPDATE=06-07-2024
set LICENSE=GNU

rem =========== Colors ===========
set "RED=0C"
set "GREEN=0A"
set "YELLOW=0E"
set "BLUE=0B"
set "RESET=07"

rem =========== Main Execution ===========
cls

echo.
echo ================================
echo Version: %VERSION%
echo Author: %AUTHOR%
echo Last Update: %LAST_UPDATE%
echo License: %LICENSE%
echo ================================
echo.

echo Checking internet connection...
nslookup google.com >nul 2>&1
if %errorlevel% neq 0 (
    color %RED%
    echo No internet connection. Please check your connection and try again.
    color %RESET%
    pause
    exit /b 1
)
color %GREEN%
echo Internet connection verified.
color %RESET%

echo Checking for Python 3.7.0...
python --version 2>nul | find "Python 3.7.0" >nul
if %errorlevel% neq 0 (
    python3 --version 2>nul | find "Python 3.7.0" >nul
    if %errorlevel% neq 0 (
        color %RED%
        echo Python 3.7.0 is not installed. Please install Python 3.7.0 and try again.
        color %RESET%
        pause
        exit /b 1
    )
)
color %GREEN%
echo Python 3.7.0 is installed.
color %RESET%

echo Checking for pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    pip3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        color %RED%
        echo pip is not installed. Please install pip and try again.
        color %RESET%
        pause
        exit /b 1
    )
)
color %GREEN%
echo pip is installed.
color %RESET%

echo Installing requirements...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    color %RED%
    echo Failed to install requirements. Please check requirements.txt and try again.
    color %RESET%
    pause
    exit /b 1
)
color %GREEN%
echo Requirements installed successfully.
color %RESET%

echo Running start.bat...
start start.bat
if %errorlevel% neq 0 (
    color %RED%
    echo Failed to run start.bat. Please check the file and try again.
    color %RESET%
    pause
    exit /b 1
)
color %GREEN%
echo start.bat executed successfully.
color %RESET%

echo.
echo Installation complete!
echo.

endlocal
pause
