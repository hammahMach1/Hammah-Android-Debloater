# Hammah's Android Debloater

A powerful GUI tool for removing unwanted Chinese apps and system packages from Android devices via ADB. Originally designed for Vivo X200S with OriginOS 5, but works with most Android devices.

![Version](https://img.shields.io/badge/version-3.0.2-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## Features

- **Dual Scan Modes**: 
  - Chinese Apps Only: Specifically targets apps with Chinese characters
  - All System Packages: Lists all installed packages for advanced users
- **Smart Detection**: Advanced Chinese character detection using comprehensive Unicode ranges
- **Safety Features**: 
  - Backup and restore functionality
  - Multiple uninstall methods (uninstall, disable, hide)
  - Warning dialogs for system-critical operations
- **User-Friendly GUI**: Modern tkinter interface with progress tracking
- **Search & Filter**: Real-time filtering of package lists
- **Batch Operations**: Select multiple apps for simultaneous removal
- **Comprehensive Logging**: Detailed operation logs for troubleshooting

## Screenshots

*GUI showing the main interface with scan options and package list*

## Requirements

### System Requirements
- Windows 10/11
- Python 3.7+ (for running from source)
- USB cable for device connection

### Android Device Requirements
- Android 5.0+ (API level 21+)
- USB Debugging enabled
- Computer authorization on device

### Required Tools
- **ADB (Android Debug Bridge)**: Essential for device communication
- **AAPT (Android Asset Packaging Tool)**: Optional, enhances app detection

## Installation

### Option 1: Download Pre-built Executable (Recommended)
1. Download `ChineseDebloater_v2.exe` from the [Releases](../../releases) page
2. Run the executable directly - no installation required!

### Option 2: Run from Source
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/hammahs-android-debloater.git
   cd hammahs-android-debloater
   ```

2. Install Python dependencies (tkinter is included with Python):
   ```bash
   # No additional dependencies required - uses only standard libraries!
   ```

3. Run the application:
   ```bash
   python ChineseDebloater.py
   ```

## Setup Instructions

### 1. Install Android SDK Platform Tools
Download from: https://developer.android.com/studio/releases/platform-tools

**Windows:**
1. Extract to `C:\platform-tools\`
2. Add to PATH environment variable
3. Verify: Open CMD and run `adb version`

### 2. Enable USB Debugging on Your Device
**For Vivo X200S (OriginOS 5):**
1. Go to Settings → About Phone
2. Tap "Version" 7 times to enable Developer Options
3. Go to Settings → System → Developer Options
4. Enable "USB Debugging"
5. Enable "USB Debugging (Security Settings)" if available

**For other devices:**
1. Go to Settings → About Phone
2. Tap "Build Number" 7 times
3. Go to Settings → Developer Options
4. Enable "USB Debugging"

### 3. Connect Your Device
1. Connect via USB cable
2. Select "File Transfer" mode when prompted
3. Authorize computer when debugging dialog appears
4. Check connection: Run `adb devices` in terminal

## Usage

### Quick Start
1. **Launch** the application (ChineseDebloater_v2.exe)
2. **Connect** your Android device via USB
3. **Choose scan mode**:
   - "Chinese Apps Only" - for targeted Chinese app removal
   - "All System Packages" - for advanced users to see all packages
4. **Click "Scan"** to detect apps
5. **Select apps** you want to remove (check the boxes)
6. **Choose removal method** and click "Remove Selected"

### Scan Modes Explained

#### Chinese Apps Only Mode
- Scans specifically for apps containing Chinese characters
- Safer for beginners
- Focuses on bloatware and unwanted Chinese apps
- Shows apps marked with "中文" indicator

#### All System Packages Mode
- Lists ALL installed packages (user + system)
- For advanced users who know what they're doing
- Includes critical system components
- **⚠️ Use with caution** - removing system packages can break your device

### Removal Methods

- **Uninstall**: Completely removes the app (recommended)
- **Disable**: Disables the app but keeps it installed
- **Hide**: Hides the app from launcher (least invasive)

### Safety Features

#### Backup & Restore
- **Backup**: Save list of removed apps before making changes
- **Restore**: Reinstall previously removed apps if needed
- Backup files saved as JSON format

#### Warnings
- System app warnings before removal
- Confirmation dialogs for batch operations
- Connection status monitoring

### Search & Filter
- Use the search box to filter displayed apps
- Real-time filtering as you type
- Filter persists during operations

## Troubleshooting

### Common Issues

**"ADB not found in PATH"**
- Install Android SDK Platform Tools
- Add platform-tools directory to system PATH
- Restart application after PATH changes

**"No devices found"**
- Check USB cable connection
- Enable USB Debugging on device
- Authorize computer on device
- Try different USB port
- Run `adb devices` to verify connection

**"Device unauthorized"**
- Check device screen for authorization dialog
- Tap "Always allow from this computer"
- If no dialog appears, run `adb kill-server` then `adb start-server`

**"AAPT not found" warning**
- This is optional - app will work without AAPT
- For better app detection, install Android SDK Build Tools
- Or ignore - fallback detection method will be used

**Apps not appearing after scan**
- Try switching scan modes
- Check if device is properly connected
- Some apps may be hidden from ADB listing

### Getting Help
If you encounter issues:
1. Check the `android_debloater.log` file in the app directory
2. Ensure your device is properly connected
3. Try different USB debugging settings
4. Restart both the app and your device

## Development

### Building from Source
To create your own executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "ChineseDebloater_v2" ChineseDebloater.py
```

### Project Structure
```
├── ChineseDebloater.py     # Main application file
├── build.bat              # Build script for Windows
├── README.md              # This file
├── LICENSE                # MIT License
└── dist/                  # Built executables
    └── ChineseDebloater_v2.exe
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Areas for Contribution
- Additional device compatibility
- UI/UX improvements
- Better error handling
- Internationalization
- macOS/Linux support

## Disclaimer

**⚠️ IMPORTANT WARNING ⚠️**

This tool modifies system applications on your Android device. While it includes safety features:

- **Use at your own risk**
- **Always backup** your device before making changes
- **Test the backup/restore** functionality before removing critical apps
- **Understand** what you're removing - some apps may be required for device functionality
- **The author is not responsible** for any damage to your device

### Recommended Safe Practice
1. Start with "Chinese Apps Only" mode
2. Remove apps in small batches
3. Test device functionality after each batch
4. Keep backups of removed app lists
5. Research unfamiliar package names before removal

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Android developer community for ADB tools and documentation
- Inspired by various Android debloating tools and scripts
- Built with Python's tkinter for cross-platform GUI support

## Version History

- **v3.0.2** - Fixed search filter data persistence bug
- **v3.0.1** - Added dual scan modes and improved filtering
- **v3.0.0** - Complete GUI rewrite with advanced features
- **v2.x** - Various improvements and bug fixes
- **v1.0** - Initial command-line version

---

**Made with ❤️ for the Android community**

*If this tool helped you reclaim your device from bloatware, consider giving it a ⭐ star!*
