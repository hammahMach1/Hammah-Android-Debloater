# Hammah's Android Debloater

A powerful, user-friendly GUI tool for removing unwanted Chinese apps and system packages from Android devices via ADB. Originally designed for Vivo X200S with OriginOS 5, but compatible with most Android devices.

![Version](https://img.shields.io/badge/version-3.0.2-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Downloads](https://img.shields.io/github/downloads/hammahMach1/Hammah-Android-Debloater/total)

> **Perfect for removing Chinese bloatware from phones purchased from international sellers**

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup Instructions](#setup-instructions)
- [How to Use](#how-to-use)
- [Safety Features](#safety-features)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

## Features

### Core Functionality
- **Dual Scan Modes**: 
  - **Chinese Apps Only**: Specifically targets apps with Chinese characters (safer for beginners)
  - **All System Packages**: Lists all installed packages for advanced users
- **Smart Detection**: Advanced Chinese character detection using comprehensive Unicode ranges
- **Batch Operations**: Select multiple apps for simultaneous removal
- **Real-time Search**: Filter packages instantly as you type

### Safety & Backup
- **Backup and Restore**: Automatically create backups before making changes
- **Multiple Removal Methods**: 
  - **Uninstall**: Completely removes the app (recommended)
  - **Disable**: Disables the app but keeps it installed
  - **Hide**: Hides the app from launcher (least invasive)
- **Smart Warnings**: Alerts for system-critical operations
- **Connection Monitoring**: Real-time ADB connection status

### User Experience
- **Modern GUI**: Clean, intuitive tkinter interface
- **Progress Tracking**: Visual feedback during operations
- **Comprehensive Logging**: Detailed operation logs for troubleshooting
- **Threading**: Non-blocking operations keep the UI responsive

## Screenshots

### Main Interface
```
┌─ Hammah's Android Debloater ─────────────────────────────┐
│ ADB Status: ● Connected to SM-G981B                     │
│ ┌─ Scan Mode ─────────────────────────────────────────┐ │
│ │ ○ Chinese Apps Only    ○ All System Packages       │ │
│ │ [Search] [Scan Devices] [Remove Selected]          │ │
│ └─────────────────────────────────────────────────────┘ │
│ ┌─ Detected Apps (23 Chinese apps found) ────────────┐ │
│ │ ☑ com.android.browser 中文 (Chrome Browser)        │ │
│ │ ☑ com.tencent.mm 中文 (WeChat)                     │ │
│ │ ☑ com.baidu.input 中文 (Baidu Input Method)        │ │
│ │ ☐ com.android.systemui (System UI)                 │ │
│ └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

*The interface shows detected apps with Chinese labels clearly marked, making it easy to identify bloatware.*

## Requirements

### System Requirements
| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10/11 (64-bit recommended) |
| **Python** | 3.7+ (only if running from source) |
| **RAM** | 4GB minimum, 8GB recommended |
| **Storage** | 50MB free space |
| **USB Port** | USB 2.0 or higher |

### Android Device Requirements
| Component | Requirement |
|-----------|-------------|
| **Android Version** | Android 5.0+ (API level 21+) |
| **Developer Options** | Must be enabled |
| **USB Debugging** | Must be enabled |
| **Authorization** | Computer must be authorized on device |
| **Cable** | Quality USB cable (data transfer capable) |

### Required Tools
- **ADB (Android Debug Bridge)**: Essential for device communication
  - Included with Android SDK Platform Tools
  - Must be in system PATH
- **AAPT (Android Asset Packaging Tool)**: Optional but recommended
  - Enhances app detection and metadata retrieval
  - Provides app names and descriptions

## Installation

### Option 1: Download Pre-built Executable (Recommended)
**Easiest method - No setup required**

1. **Download**: Get `ChineseDebloater_v2.exe` from the [Releases](../../releases) page
2. **Run**: Double-click the executable - no installation needed
3. **Done**: The application will launch immediately

```bash
# Quick download with PowerShell (optional)
Invoke-WebRequest -Uri "https://github.com/hammahMach1/Hammah-Android-Debloater/releases/latest/download/ChineseDebloater_v2.exe" -OutFile "ChineseDebloater_v2.exe"
```

### Option 2: Run from Source
**For developers or users who prefer Python**

1. **Clone this repository**:
   ```bash
   git clone https://github.com/hammahMach1/Hammah-Android-Debloater.git
   cd Hammah-Android-Debloater
   ```

2. **Install Python dependencies**:
   ```bash
   # Good news - no additional dependencies required! 
   # Uses only Python standard libraries (tkinter, subprocess, etc.)
   python --version  # Verify Python 3.7+ is installed
   ```

3. **Run the application**:
   ```bash
   python ChineseDebloater.py
   ```

## Setup Instructions

### Step 1: Install Android SDK Platform Tools

**Download**: Get the tools from [Android Developer Website](https://developer.android.com/studio/releases/platform-tools)

#### Windows Installation:
```powershell
# Option A: Manual Installation
# 1. Download platform-tools-latest-windows.zip
# 2. Extract to C:\platform-tools\
# 3. Add to PATH environment variable

# Option B: Using Windows Package Manager (if available)
winget install Google.PlatformTools

# Option C: Using Chocolatey (if available)
choco install adb
```

#### Add to PATH:
1. **Extract** platform-tools to `C:\platform-tools\`
2. **Open** System Properties → Advanced → Environment Variables
3. **Add** `C:\platform-tools` to your PATH
4. **Verify** installation:
   ```cmd
   adb version
   # Should show: Android Debug Bridge version X.X.X
   ```

### Step 2: Enable USB Debugging on Your Device

#### For Vivo X200S (OriginOS 5) - Tested Configuration:
```
Settings → About Phone → Version (tap 7 times)
   ↓
Settings → System → Developer Options
   ↓ 
✅ Enable "USB Debugging"
✅ Enable "USB Debugging (Security Settings)" (if available)
✅ Enable "Install via USB" (recommended)
```

#### For Other Android Devices:
| Device Brand | Path to Developer Options |
|--------------|---------------------------|
| **Samsung** | Settings → About Phone → Software Information → Build Number (tap 7x) |
| **Xiaomi/MIUI** | Settings → About Phone → MIUI Version (tap 7x) |
| **OnePlus** | Settings → About Phone → Build Number (tap 7x) |
| **Huawei** | Settings → About Phone → Build Number (tap 7x) |
| **Generic** | Settings → About Phone → Build Number (tap 7x) |

After enabling Developer Options:
1. **Go to** Settings → Developer Options (or System → Developer Options)
2. **Enable** "USB Debugging"
3. **Enable** "Install via USB" (if available)
4. **Enable** "USB Debugging (Security Settings)" (if available)

### Step 3: Connect and Test Your Device

#### Connection Process:
1. **Connect** your device via USB cable
2. **Select** "File Transfer" or "MTP" mode when prompted on device
3. **Authorize** computer when USB debugging dialog appears
4. **Check** "Always allow from this computer" (recommended)

#### Test Connection:
```cmd
# Check if device is detected
adb devices

# Expected output:
# List of devices attached
# ABC123DEF456    device

# If you see "unauthorized", check your device for authorization dialog
# If you see "no devices", troubleshoot connection
```

#### Quick Connection Test:
```cmd
# Get device information
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release

# These should return your device model and Android version
```

## How to Use

### Quick Start Guide

#### For Beginners (Recommended):
1. **Launch**: Run `ChineseDebloater_v2.exe`
2. **Connect**: Ensure your Android device is connected via USB
3. **Mode**: Select "**Chinese Apps Only**" (safer option)
4. **Scan**: Click "**Scan**" button to detect Chinese apps
5. **Select**: Check boxes next to apps you want to remove
6. **Remove**: Click "**Remove Selected**" → Choose "**Uninstall**"
7. **Done**: Apps are removed safely

#### For Advanced Users:
1. **Launch**: Run the application
2. **Connect**: Verify device connection (green status indicator)
3. **Mode**: Select "**All System Packages**" for full control
4. **Scan**: Click "**Scan**" to list all packages
5. **Filter**: Use search box to find specific packages
6. **Research**: Look up unfamiliar packages before removing
7. **Select**: Carefully choose packages to remove
8. **Backup**: Create backup before major changes
9. **Remove**: Choose appropriate removal method

### Understanding Scan Modes

#### Chinese Apps Only Mode
```
✅ SAFER FOR BEGINNERS
🎯 Targets apps with Chinese characters
🛡️ Reduced risk of system damage
📝 Shows apps marked with "中文" indicator
🧹 Perfect for removing bloatware
```

**Example detected apps:**
- `com.tencent.mm` 中文 (WeChat)
- `com.baidu.input` 中文 (Baidu Input)
- `com.sina.weibo` 中文 (Weibo)

#### All System Packages Mode
```
⚠️ FOR ADVANCED USERS ONLY
📋 Lists ALL installed packages
🔧 Includes critical system components
🎛️ Full control over device packages
⚡ Can break device if misused
```

**Warning**: This mode shows system-critical apps that should NOT be removed unless you know exactly what you're doing.

### Removal Methods Explained

| Method | Effect | Reversible | Use Case |
|--------|--------|------------|----------|
| **Uninstall** | Completely removes app | Partially* | Unwanted apps, bloatware |
| **Disable** | App becomes inactive | Yes | System apps you can't uninstall |
| **Hide** | Hidden from launcher | Yes | Apps you rarely use |

*Can be restored from backup or APK reinstallation

### Search and Filter Features

#### Real-time Search:
```
Search Box: [tencent________]
Results: 
  ✅ com.tencent.mm (WeChat)
  ✅ com.tencent.android.qqdownloader
  ✅ com.tencent.mobileqq
```

#### Filter by Categories:
- **Chinese**: Search "中文" to show only Chinese apps
- **System**: Search "android.system" for system components  
- **Google**: Search "google" for Google services
- **Manufacturer**: Search "vivo", "samsung", etc.

### Step-by-Step: First Time Setup

#### Complete Setup Process:
```
1. Download → ChineseDebloater_v2.exe
2. Install → Android Platform Tools
3. Setup → PATH environment variable
4. Enable → USB Debugging on phone
5. Connect → Phone to computer via USB
6. Test → Run 'adb devices' in command prompt
7. Launch → ChineseDebloater_v2.exe
8. Scan → Start with "Chinese Apps Only"
9. Select → Choose apps to remove
10. Remove → Click "Remove Selected"
```

### Pro Tips

#### Safety First:
- **Start Small**: Remove 2-3 apps at a time initially
- **Backup**: Always create backups before major operations
- **Test**: Check device functionality after each removal
- **Research**: Look up unfamiliar package names online

#### Efficiency Tips:
- **Use Search**: Filter results instead of scrolling through hundreds of apps
- **Batch Select**: Hold Ctrl and click to select multiple apps
- **Refresh**: Click "Refresh" if device disconnects
- **Log Files**: Check logs for detailed operation history

## Safety Features

### Backup and Restore System

#### Automatic Backups:
- **Time-stamped**: Each backup includes date and time
- **Package Lists**: Saves list of removed apps with metadata
- **JSON Format**: Human-readable backup files
- **Location**: Saved in application directory

#### Backup File Structure:
```json
{
  "timestamp": "2025-08-10_14:30:25",
  "device_model": "Vivo X200S",
  "android_version": "14",
  "removed_packages": [
    {
      "package": "com.tencent.mm",
      "name": "WeChat",
      "method": "uninstall",
      "chinese_detected": true
    }
  ]
}
```

#### Restore Process:
1. **Select Backup**: Choose from available backup files
2. **Connect Device**: Ensure same device is connected
3. **Restore**: Apps are automatically reinstalled
4. **Verify**: Check that apps are restored successfully

### Smart Warning System

#### Critical System App Warnings:
```
⚠️  WARNING: System Critical App Detected
Package: com.android.systemui
Name: System UI
Removing this app may cause your device to malfunction!

Recommendations:
✅ Disable instead of uninstall
✅ Create backup before proceeding
✅ Research this package online first

Continue? [Yes] [No] [Learn More]
```

#### App Risk Assessment:
| Risk Level | Description | Apps Included |
|------------|-------------|---------------|
| **Safe** | Bloatware, games, social apps | WeChat, TikTok, games |
| **Caution** | Manufacturer apps, some may be useful | Vivo apps, carrier apps |
| **Risky** | System components with alternatives | Default browsers, keyboards |
| **Critical** | Essential system functions | SystemUI, PackageInstaller |

### Connection Security

#### Real-time Status Monitoring:
```
ADB Status: Connected to SM-G981B
Device: Samsung Galaxy S20
Android: 11 (API 30)
Battery: 85% (Not charging recommended during debloating)
```

#### Auto-reconnection:
- **Detects**: Connection drops automatically
- **Reconnects**: Attempts to restore connection
- **Pauses**: Operations during disconnection
- **Notifies**: User of connection status changes

### Thread Safety

#### Non-blocking Operations:
- **UI Responsive**: Interface remains usable during operations
- **Background Processing**: Scanning and removal run in separate threads
- **Progress Updates**: Real-time progress indicators
- **Cancellable**: Operations can be stopped mid-process

## Troubleshooting

### Common Issues and Solutions

#### "ADB not found in PATH"
```
Problem: Application can't find ADB command
Solutions:
1. Install Android SDK Platform Tools
2. Add platform-tools directory to system PATH
3. Restart application after PATH changes
4. Test: Open CMD and run 'adb version'
```

#### "No devices found"
```
Problem: Device not detected by ADB
Solutions:
1. Check USB cable (ensure data transfer capable)
2. Enable USB Debugging on device
3. Authorize computer on device screen
4. Try different USB port
5. Run 'adb kill-server' then 'adb start-server'
6. Change USB connection mode to "File Transfer"
```

#### "Device unauthorized"
```
Problem: Computer not authorized for debugging
Solutions:
1. Check device screen for authorization dialog
2. Tap "Always allow from this computer"
3. If no dialog: adb kill-server → adb start-server
4. Disconnect and reconnect USB cable
5. Toggle USB Debugging off/on in developer options
```

#### "AAPT not found" warning
```
Problem: AAPT tool missing (optional)
Impact: App names may not display correctly
Solutions:
1. Ignore warning - app will work with fallback method
2. Install Android SDK Build Tools for better detection
3. Add build-tools to PATH for enhanced features
```

#### Apps not appearing after scan
```
Problem: Expected apps don't show in results
Solutions:
1. Try switching between scan modes
2. Verify device connection (green status)
3. Check if apps are hidden from ADB listing
4. Use search function to find specific packages
5. Some apps may be installed as system updates
```

### Advanced Troubleshooting

#### Debug Mode:
```powershell
# Enable verbose ADB logging
set ADB_TRACE=all
adb devices

# Check device properties
adb shell getprop ro.debuggable
adb shell getprop ro.secure
```

#### Log Analysis:
- **Log File**: `android_debloater.log` in app directory
- **Contains**: Detailed operation history, error messages, device info
- **Search**: Look for ERROR or WARNING entries
- **Share**: Include relevant log sections when reporting issues

#### Manual ADB Testing:
```cmd
# Test basic ADB functions
adb devices                                    # List connected devices
adb shell pm list packages | findstr tencent  # Find specific packages
adb shell pm uninstall --user 0 com.example   # Manual uninstall test
adb shell pm disable-user com.example         # Manual disable test
```

### Getting Help

#### If you encounter persistent issues:

1. **Check Logs**: Review `android_debloater.log` for error details
2. **Verify Setup**: Ensure ADB and device are properly configured
3. **Restart**: Try restarting both the app and your device
4. **Device Settings**: Check USB debugging and developer options
5. **Community**: Search GitHub issues for similar problems
6. **Report Bug**: Create new issue with:
   - Device model and Android version
   - Error message and relevant log entries
   - Steps to reproduce the problem

#### Issue Report Template:
```
Device: [Your device model]
Android Version: [Version number]
App Version: 3.0.2
ADB Version: [Run 'adb version']

Problem Description:
[Describe what happened]

Steps to Reproduce:
1. [First step]
2. [Second step]
3. [Error occurs]

Log Excerpt:
[Relevant lines from android_debloater.log]
```

## Development

### Building from Source

#### Create Your Own Executable:
```bash
# Install build dependencies
pip install pyinstaller

# Create single executable file
pyinstaller --onefile --windowed --name "ChineseDebloater_v2" ChineseDebloater.py

# Advanced build with icon and additional options
pyinstaller --onefile --windowed --icon=icon.ico --name "ChineseDebloater_v2" ChineseDebloater.py
```

#### Build Script (Windows):
Use the included `build.bat`:
```batch
@echo off
echo Building Hammah's Android Debloater...
pyinstaller --onefile --windowed --name "ChineseDebloater_v2" ChineseDebloater.py
echo Build complete! Check dist/ folder.
pause
```

### Project Structure
```
Hammah-Android-Debloater/
├── ChineseDebloater.py          # Main application file
├── build.bat                    # Build script for Windows
├── README.md                    # This comprehensive guide
├── LICENSE                      # MIT License
├── CHANGELOG.md                 # Version history
├── PROJECT_SUMMARY.md           # Development summary
├── setup_adb.bat               # ADB setup helper
├── install_android_tools.bat   # Tools installation helper
├── build/                      # Build artifacts
│   └── ChineseDebloater_v2/    # PyInstaller build files
├── dist/                       # Compiled executables
│   └── ChineseDebloater_v2.exe # Ready-to-run executable
└── logs/                       # Application logs
    └── android_debloater.log   # Runtime logs
```

### Testing

#### Manual Testing Checklist:
```
Device Connection:
☐ ADB detection works
☐ Device authorization flows
☐ Connection status updates
☐ Reconnection handling

Scanning:
☐ Chinese apps detection
☐ All packages listing
☐ Search/filter functionality
☐ UI responsiveness during scan

Removal Operations:
☐ Uninstall method works
☐ Disable method works  
☐ Hide method works
☐ Batch operations
☐ Error handling

Safety Features:
☐ Backup creation
☐ Restore functionality
☐ Warning dialogs
☐ System app protection
```

#### Unit Testing Framework:
```python
# Example test structure (not included in current version)
import unittest
from ChineseDebloater import AndroidDebloaterGUI

class TestAndroidDebloater(unittest.TestCase):
    def test_chinese_detection(self):
        # Test Chinese character detection
        pass
    
    def test_adb_connection(self):
        # Test ADB connectivity
        pass
```

### Development Setup

#### Development Environment:
```bash
# Clone repository
git clone https://github.com/hammahMach1/Hammah-Android-Debloater.git
cd Hammah-Android-Debloater

# Set up development environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install development dependencies
pip install pyinstaller

# Run from source
python ChineseDebloater.py
```

#### Code Style Guidelines:
- **Python**: Follow PEP 8 standards
- **Documentation**: Comprehensive docstrings
- **Comments**: Clear, concise explanations
- **Testing**: Test all major functions
- **Logging**: Detailed operation logging

### Future Enhancements

#### Planned Features:
- **Multi-language Support**: Interface translations
- **macOS Support**: Cross-platform compatibility
- **Linux Support**: Ubuntu/Debian packages
- **Advanced Analytics**: Detailed removal statistics
- **Auto-updates**: Built-in update mechanism
- **Wireless ADB**: TCP/IP connection support

#### Technical Improvements:
- **Performance**: Faster scanning algorithms
- **UI/UX**: Modern framework migration (possibly PyQt/tkinter++)
- **Plugin System**: Extensible architecture
- **Cloud Backup**: Remote backup storage
- **AI Detection**: Smart bloatware identification

## Contributing

We welcome contributions from the community! Here's how you can help:

### Areas for Contribution

#### Bug Fixes:
- **Device Compatibility**: Test with different Android devices
- **ADB Issues**: Improve connection reliability
- **UI Bugs**: Fix interface glitches and responsiveness
- **Documentation**: Correct errors and improve clarity

#### New Features:
- **Internationalization**: Add support for multiple languages
- **Device Profiles**: Pre-configured removal lists for specific devices
- **Backup Improvements**: Enhanced backup/restore functionality
- **Reporting**: Better logging and operation reports

### Contribution Process

#### Getting Started:
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages: `git commit -m 'Add amazing feature'`
6. **Push** to your branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

#### Pull Request Guidelines:
```
Title: [Feature/Bug/Docs] Brief description

Description:
- What this PR does
- Why it's needed
- How to test it

Testing:
- [ ] Tested on Windows 10/11
- [ ] Tested with Android device
- [ ] No new lint warnings
- [ ] Documentation updated

Screenshots (if UI changes):
[Include before/after screenshots]
```

### Recognition

#### Contributors:
- **UI/UX Improvements**: [Your name here]
- **Bug Fixes**: [Your name here]  
- **Documentation**: [Your name here]
- **Translations**: [Your name here]

Want to see your name here? Contribute to the project!

## Disclaimer

### IMPORTANT WARNING

**This tool modifies system applications on your Android device. While it includes comprehensive safety features, please understand the risks:**

#### Risk Acknowledgment:
- **Use at your own risk** - No warranty provided
- **Always backup** your device before making changes
- **Test thoroughly** - Start with non-critical apps
- **Research packages** before removing unfamiliar ones
- **Device functionality** may be affected by improper use

#### Recommended Safe Practices:

1. **Start Conservative**:
   - Begin with "Chinese Apps Only" mode
   - Remove 2-3 apps at a time initially
   - Test device functionality after each removal

2. **Backup Everything**:
   - Enable automatic backups in the app
   - Create manual backups before major operations
   - Keep backups of important APK files

3. **Research First**:
   - Look up unfamiliar package names online
   - Check Android forums for package information
   - When in doubt, disable instead of uninstall

4. **Test Thoroughly**:
   - Verify device functionality after removals
   - Check that essential features still work
   - Keep backups until you're sure changes are stable

#### Limitation of Liability:
**The author and contributors are not responsible for:**
- Device damage or malfunction
- Data loss or corruption  
- Software instability
- Loss of device functionality
- Any consequential damages

#### Your Responsibility:
By using this tool, you acknowledge that you:
- Have read and understood these warnings
- Have the technical knowledge to use ADB tools safely
- Will create appropriate backups before making changes
- Will test changes incrementally
- Accept full responsibility for any consequences

### If Something Goes Wrong:

1. **Restore from Backup**: Use the app's restore function
2. **Factory Reset**: Last resort - will erase all data
3. **Fastboot Recovery**: For advanced users with bootloader access
4. **Professional Help**: Contact device manufacturer or repair service

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary:
```
✅ Commercial use allowed
✅ Modification allowed  
✅ Distribution allowed
✅ Private use allowed
❌ Liability excluded
❌ Warranty excluded
```

**Translation**: You can use, modify, and distribute this software freely, but the authors provide no warranty and accept no liability for damages.

---

## Acknowledgments

### Special Thanks:
- **Android Developer Community**: For ADB tools and comprehensive documentation
- **PyInstaller Team**: For making Python app distribution easy
- **Python Community**: For the excellent standard libraries used
- **XDA Developers**: For Android debloating research and community knowledge
- **Beta Testers**: Users who helped test and improve the application

### Inspiration:
This project was inspired by:
- **Universal Android Debloater**: Similar concept, different implementation
- **ADB AppControl**: GUI approach to ADB package management  
- **Debloat Scripts**: Community scripts for removing bloatware
- **Personal Need**: Frustration with Chinese bloatware on international devices

### Built With:
- **Python 3.7+**: Core programming language
- **Tkinter**: GUI framework (included with Python)
- **ADB (Android Debug Bridge)**: Android device communication
- **PyInstaller**: Executable compilation
- **Love**: For the Android community and open source

---

## Project Statistics

![GitHub stars](https://img.shields.io/github/stars/hammahMach1/Hammah-Android-Debloater)
![GitHub forks](https://img.shields.io/github/forks/hammahMach1/Hammah-Android-Debloater)
![GitHub issues](https://img.shields.io/github/issues/hammahMach1/Hammah-Android-Debloater)
![GitHub last commit](https://img.shields.io/github/last-commit/hammahMach1/Hammah-Android-Debloater)

## Quick Links

- **[Download Latest Release](../../releases/latest)**
- **[Report Issues](../../issues)**
- **[Request Features](../../issues/new)**
- **[View Documentation](../../wiki)**
- **[Join Discussions](../../discussions)**

---

**Made with care for the Android community**

*If this tool helped you reclaim your device from bloatware, consider giving it a star on GitHub!*

**Happy Debloating!**
