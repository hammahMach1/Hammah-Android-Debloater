@echo off
echo Building Chinese Debloater executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is available
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build the executable
echo Building executable...
python -m PyInstaller --onefile --windowed --name "ChineseDebloater_v2" ChineseDebloater.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo Build complete! Executable is in the 'dist' folder.
echo File: dist\ChineseDebloater_v2.exe
echo.

REM Check if ADB is available
echo Checking for ADB...
adb version >nul 2>&1
if errorlevel 1 (
    echo WARNING: ADB not found in PATH
    echo Please ensure Android SDK Platform Tools are installed
    echo and ADB is accessible from command line
) else (
    echo ADB found - ready to use!
)

echo.
echo IMPORTANT SETUP NOTES:
echo 1. Ensure Android SDK Platform Tools are installed
echo 2. Add platform-tools directory to your PATH
echo 3. Enable USB Debugging on your Vivo X200S
echo 4. Connect device and authorize computer when prompted
echo.

pause
