# Changelog

All notable changes to Hammah's Android Debloater will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.2] - 2025-08-10

### Fixed
- Fixed critical bug where search filter would permanently remove data from package list
- Improved thread-safe item management in GUI tree view
- Fixed filtering system to preserve original data while showing filtered results

### Technical Changes
- Added ll_tree_items persistent storage for filtering
- Implemented dd_tree_item_threadsafe() method for thread safety
- Rewrote on_filter_change() to preserve data integrity

## [3.0.1] - 2025-08-10

### Added
- Dual scan modes: "Chinese Apps Only" and "All System Packages"
- Advanced filtering system with real-time search
- Missing check_adb_connection() method implementation

### Fixed
- ADB connection checking functionality
- Application startup errors

### Changed
- Improved user interface with scan mode selection
- Enhanced package detection and listing

## [3.0.0] - 2025-08-10

### Added
- Complete GUI rewrite using tkinter
- Modern user interface with progress tracking
- Dual scan modes for different user levels
- Real-time search and filtering of packages
- Batch operations for multiple app selection
- Comprehensive backup and restore functionality
- Multiple uninstall methods (uninstall, disable, hide)
- Safety warnings for system-critical operations
- Detailed logging system
- Threading for non-blocking operations

### Changed
- Renamed application from "Chinese Debloater" to "Hammah's Android Debloater"
- Updated class name from ChineseDebloaterGUI to AndroidDebloaterGUI
- Changed log file from chinese_debloater.log to ndroid_debloater.log
- Device target updated from X20S to X200S

### Fixed
- AAPT missing error with graceful fallback
- Improved Chinese character detection using comprehensive Unicode ranges
- Better error handling throughout the application

## [2.x] - Previous Versions

### Added
- GUI interface improvements
- Basic backup functionality
- Enhanced Chinese app detection

### Fixed
- Various stability improvements
- Error handling enhancements

## [1.0] - Initial Release

### Added
- Basic command-line Chinese app detection
- ADB integration for Android device communication
- Simple uninstall functionality for Chinese apps
- Target device: Vivo X20S (later updated to X200S)

### Features
- Scan for Chinese-labeled applications
- Uninstall detected Chinese apps
- Basic logging and feedback
