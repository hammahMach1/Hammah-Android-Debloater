@echo off
echo Chinese Debloater - ADB Setup Helper
echo =====================================
echo.

REM Check if ADB is already available
adb version >nul 2>&1
if not errorlevel 1 (
    echo ADB is already installed and accessible!
    echo Version information:
    adb version
    echo.
    echo Testing device connection...
    adb devices
    echo.
    echo If your device appears in the list above, you're ready to go!
    echo If not, ensure USB Debugging is enabled and device is connected.
    goto :end
)

echo ADB not found in PATH. 
echo.
echo To set up ADB (Android Debug Bridge):
echo.
echo 1. Download Android SDK Platform Tools from:
echo    https://developer.android.com/studio/releases/platform-tools
echo.
echo 2. Extract the downloaded zip file to a folder like:
echo    C:\platform-tools\
echo.
echo 3. Add the platform-tools folder to your system PATH:
echo    - Right-click 'This PC' ^> Properties
echo    - Click 'Advanced system settings'
echo    - Click 'Environment Variables'
echo    - Under 'System Variables', find and select 'Path'
echo    - Click 'Edit' and then 'New'
echo    - Add the path to your platform-tools folder
echo    - Click 'OK' to save
echo.
echo 4. Restart this command prompt and try again
echo.
echo Alternative: Place adb.exe, AdbWinApi.dll, and AdbWinUsbApi.dll
echo in the same folder as ChineseDebloater_v2.exe
echo.

:end
pause
