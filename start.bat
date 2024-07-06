@echo off
setlocal

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

echo Running main.py...
python src\main.py
if %errorlevel% neq 0 (
    color %RED%
    echo Failed to run main.py. Please check the script and try again.
    color %RESET%
    pause
    exit /b 1
)
color %GREEN%
echo main.py executed successfully.
color %RESET%

echo.
echo Execution complete!
echo.

endlocal
pause
