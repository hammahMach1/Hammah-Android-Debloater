@echo off
echo ============================================
echo   Android Tools Setup for Chinese Debloater
echo ============================================
echo.

REM Create tools directory
set TOOLS_DIR=C:\AndroidTools
if not exist "%TOOLS_DIR%" (
    echo Creating directory: %TOOLS_DIR%
    mkdir "%TOOLS_DIR%"
)

echo Checking current tool availability...
echo.

REM Check ADB
adb version >nul 2>&1
if not errorlevel 1 (
    echo [OK] ADB is already installed and accessible
    adb version | findstr "Android Debug Bridge"
) else (
    echo [MISSING] ADB not found
    set NEED_PLATFORM_TOOLS=1
)

echo.

REM Check AAPT
aapt version >nul 2>&1
if not errorlevel 1 (
    echo [OK] AAPT is already installed and accessible
    aapt version | findstr "Android Asset Packaging Tool"
) else (
    echo [MISSING] AAPT not found
    set NEED_BUILD_TOOLS=1
)

echo.
echo ============================================

if defined NEED_PLATFORM_TOOLS (
    echo.
    echo ADB is required for device communication.
    echo.
    echo To install Android SDK Platform Tools:
    echo 1. Go to: https://developer.android.com/studio/releases/platform-tools
    echo 2. Download 'SDK Platform-Tools for Windows'
    echo 3. Extract to %TOOLS_DIR%\platform-tools\
    echo 4. Add %TOOLS_DIR%\platform-tools to your PATH
    echo.
    
    set /p download_adb="Would you like me to open the download page? (y/n): "
    if /i "!download_adb!"=="y" (
        start https://developer.android.com/studio/releases/platform-tools
        echo Download page opened in your browser.
        echo.
        echo After downloading:
        echo 1. Extract the zip file to %TOOLS_DIR%\platform-tools\
        echo 2. Run this script again to add to PATH
    )
)

if defined NEED_BUILD_TOOLS (
    echo.
    echo AAPT provides better app analysis but is optional.
    echo The Chinese Debloater can work without it using alternative methods.
    echo.
    echo To install Android SDK Build Tools (optional):
    echo 1. Install Android Studio from: https://developer.android.com/studio
    echo 2. Or download command-line tools and install build-tools
    echo.
    
    set /p download_studio="Would you like me to open Android Studio download page? (y/n): "
    if /i "!download_studio!"=="y" (
        start https://developer.android.com/studio
        echo Android Studio download page opened.
    )
)

REM Check if platform-tools exists and offer to add to PATH
if exist "%TOOLS_DIR%\platform-tools\adb.exe" (
    echo.
    echo Found platform-tools in %TOOLS_DIR%\platform-tools\
    
    REM Check if already in PATH
    echo %PATH% | findstr /i "platform-tools" >nul
    if errorlevel 1 (
        echo Platform-tools not in PATH. Adding it now...
        
        REM Add to user PATH
        for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "UserPath=%%B"
        if not defined UserPath set "UserPath="
        
        REM Check if already contains platform-tools
        echo !UserPath! | findstr /i "platform-tools" >nul
        if errorlevel 1 (
            if defined UserPath (
                set "NewPath=!UserPath!;%TOOLS_DIR%\platform-tools"
            ) else (
                set "NewPath=%TOOLS_DIR%\platform-tools"
            )
            
            reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "!NewPath!" /f >nul
            echo [OK] Added platform-tools to PATH
            echo.
            echo IMPORTANT: Restart your command prompt or computer for PATH changes to take effect.
        )
    ) else (
        echo [OK] Platform-tools already in PATH
    )
)

echo.
echo ============================================
echo Current Status:
echo.

REM Re-check after potential installation
adb version >nul 2>&1
if not errorlevel 1 (
    echo [OK] ADB is accessible
) else (
    echo [PENDING] ADB needs installation or PATH update
)

aapt version >nul 2>&1
if not errorlevel 1 (
    echo [OK] AAPT is accessible
) else (
    echo [INFO] AAPT not available (optional - app will use alternative method)
)

echo.
echo ============================================
echo.

if not defined NEED_PLATFORM_TOOLS if not defined NEED_BUILD_TOOLS (
    echo All tools are ready! You can now use Chinese Debloater.
) else (
    echo Setup instructions provided above.
    echo After installing the tools, restart your command prompt and run Chinese Debloater again.
)

echo.
echo Press any key to exit...
pause >nul
