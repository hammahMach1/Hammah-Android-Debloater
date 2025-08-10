#!/usr/bin/env python3
"""
Hammah's Android Debloater
A tool to remove Chinese-labeled apps from Android devices via ADB
Optimized for Vivo X200S with OriginOS 5
"""

import subprocess
import re
import os
import tempfile
import sys
import logging
import json
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('android_debloater.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AndroidDebloaterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hammah's Android Debloater - Vivo X200S OriginOS 5")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.chinese_apps = []
        self.all_packages = []
        self.all_tree_items = []  # Store all tree items for filtering
        self.is_scanning = False
        self.is_debloating = False
        self.scan_mode = "chinese"  # "chinese" or "all"
        
        # Create GUI
        self.create_widgets()
        
        # Check ADB connection on startup
        self.root.after(100, self.check_adb_connection)
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Hammah's Android Debloater", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Connection status
        ttk.Label(main_frame, text="ADB Status:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.status_label = ttk.Label(main_frame, text="Checking...", foreground="orange")
        self.status_label.grid(row=1, column=1, sticky=tk.W)
        
        # Refresh connection button
        self.refresh_btn = ttk.Button(main_frame, text="Refresh", command=self.check_adb_connection)
        self.refresh_btn.grid(row=1, column=2, sticky=tk.E)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Detected Apps", padding="5")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Scan mode selection
        mode_frame = ttk.Frame(results_frame)
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(mode_frame, text="Scan Mode:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.scan_mode_var = tk.StringVar(value="chinese")
        ttk.Radiobutton(mode_frame, text="Chinese Apps Only", variable=self.scan_mode_var, 
                       value="chinese", command=self.on_scan_mode_change).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="All System Packages", variable=self.scan_mode_var, 
                       value="all", command=self.on_scan_mode_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Filter frame
        filter_frame = ttk.Frame(results_frame)
        filter_frame.grid(row=0, column=1, sticky=tk.E, pady=(0, 5))
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 5))
        self.filter_var = tk.StringVar()
        self.filter_var.trace('w', self.on_filter_change)
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=20)
        filter_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(filter_frame, text="Clear", command=self.clear_filter).pack(side=tk.LEFT)
        
        # Treeview for apps
        columns = ("Package", "Label", "Type", "Status")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("Package", text="Package Name")
        self.tree.heading("Label", text="App Label")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("Package", width=300)
        self.tree.column("Label", width=200)
        self.tree.column("Type", width=100)
        self.tree.column("Status", width=100)
        
        # Add checkboxes for selection
        self.selected_apps = set()
        self.tree.bind('<Button-1>', self.on_tree_click)
        self.tree.bind('<space>', self.on_tree_space)
        
        # Configure tree tags for visual feedback
        self.tree.tag_configure('checked', background='lightblue')
        self.tree.tag_configure('unchecked', background='white')
        self.tree.tag_configure('critical', background='#ffcccc')  # Light red for critical packages
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid treeview and scrollbars
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Selection info
        self.selection_label = ttk.Label(main_frame, text="0 apps selected")
        self.selection_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        self.scan_btn = ttk.Button(buttons_frame, text="Scan Apps", command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.select_all_btn = ttk.Button(buttons_frame, text="Select All", command=self.select_all_apps, state="disabled")
        self.select_all_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_selection_btn = ttk.Button(buttons_frame, text="Clear Selection", command=self.clear_selection, state="disabled")
        self.clear_selection_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.debloat_btn = ttk.Button(buttons_frame, text="Uninstall Selected Apps", command=self.start_debloat, state="disabled")
        self.debloat_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.backup_btn = ttk.Button(buttons_frame, text="Create Backup List", command=self.create_backup)
        self.backup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.restore_btn = ttk.Button(buttons_frame, text="Restore Apps", command=self.restore_apps)
        self.restore_btn.pack(side=tk.LEFT)
    
    def on_scan_mode_change(self):
        """Called when scan mode radio button changes."""
        self.scan_mode = self.scan_mode_var.get()
        self.update_scan_button_text()
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.chinese_apps.clear()
        self.all_packages.clear()
        self.all_tree_items.clear()  # Clear stored items
        self.selected_apps.clear()
        self.update_selection_label()
    
    def update_scan_button_text(self):
        """Update scan button text based on mode."""
        if self.scan_mode == "chinese":
            self.scan_btn.config(text="Scan for Chinese Apps")
        else:
            self.scan_btn.config(text="Scan All System Packages")
    
    def on_filter_change(self, *args):
        """Filter the displayed apps based on search text."""
        filter_text = self.filter_var.get().lower()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Re-add filtered items from stored data
        for item_data in self.all_tree_items:
            values = item_data['values']
            tags = item_data['tags']
            
            # Check if any value matches the filter
            if not filter_text or any(filter_text in str(val).lower() for val in values):
                new_item = self.tree.insert('', 'end', values=values, tags=tags)
                # Restore selection state if this item was selected
                package_name = values[0]
                if package_name in self.selected_apps:
                    self.tree.set(new_item, "Status", "Selected ✓")
                    self.tree.item(new_item, tags=('checked',))
    
    def clear_filter(self):
        """Clear the filter."""
        self.filter_var.set("")
    
    def on_tree_click(self, event):
        """Handle tree item click for selection."""
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.toggle_selection(item)
    
    def on_tree_space(self, event):
        """Handle space key for selection."""
        selection = self.tree.selection()
        if selection:
            self.toggle_selection(selection[0])
    
    def toggle_selection(self, item):
        """Toggle selection of an app."""
        values = self.tree.item(item)['values']
        if not values:
            return
        
        package_name = values[0]
        
        if package_name in self.selected_apps:
            self.selected_apps.remove(package_name)
            self.tree.set(item, "Status", "Ready")
            tags = ('unchecked',)
        else:
            self.selected_apps.add(package_name)
            self.tree.set(item, "Status", "Selected ✓")
            tags = ('checked',)
        
        self.tree.item(item, tags=tags)
        self.update_selection_label()
        self.update_button_states()
    
    def select_all_apps(self):
        """Select all visible apps."""
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if values:
                package_name = values[0]
                self.selected_apps.add(package_name)
                self.tree.set(item, "Status", "Selected ✓")
                self.tree.item(item, tags=('checked',))
        
        self.update_selection_label()
        self.update_button_states()
    
    def clear_selection(self):
        """Clear all selections."""
        self.selected_apps.clear()
        for item in self.tree.get_children():
            self.tree.set(item, "Status", "Ready")
            self.tree.item(item, tags=('unchecked',))
        
        self.update_selection_label()
        self.update_button_states()
    
    def add_tree_item(self, values, tags=('unchecked',)):
        """Add an item to the tree and store it for filtering."""
        # This method should only be called from the main thread
        item = self.tree.insert('', 'end', values=values, tags=tags)
        
        # Store item data for filtering
        item_data = {
            'values': values,
            'tags': tags
        }
        self.all_tree_items.append(item_data)
        
        return item
    
    def add_tree_item_threadsafe(self, values, tags=('unchecked',)):
        """Thread-safe version to add tree item."""
        # Store item data immediately (this is thread-safe)
        item_data = {
            'values': values,
            'tags': tags
        }
        self.all_tree_items.append(item_data)
        
        # Schedule GUI update on main thread
        self.root.after(0, lambda: self.tree.insert('', 'end', values=values, tags=tags))
    
    def update_selection_label(self):
        """Update the selection count label."""
        count = len(self.selected_apps)
        self.selection_label.config(text=f"{count} apps selected")
    
    def update_button_states(self):
        """Update button states based on selection."""
        has_apps = len(list(self.tree.get_children())) > 0
        has_selection = len(self.selected_apps) > 0
        
        self.select_all_btn.config(state="normal" if has_apps else "disabled")
        self.clear_selection_btn.config(state="normal" if has_selection else "disabled")
        self.debloat_btn.config(state="normal" if has_selection else "disabled")
    
    def get_package_type(self, package_name: str) -> str:
        """Determine the type of package."""
        if package_name.startswith('com.android.'):
            return "Android System"
        elif package_name.startswith('com.google.'):
            return "Google"
        elif package_name.startswith('com.vivo.'):
            return "Vivo System"
        elif package_name.startswith('com.qualcomm.'):
            return "Qualcomm"
        elif package_name.startswith('com.samsung.'):
            return "Samsung"
        elif package_name.startswith('com.xiaomi.'):
            return "Xiaomi"
        elif package_name.startswith('com.oppo.'):
            return "OPPO"
        elif package_name.startswith('com.oneplus.'):
            return "OnePlus"
        elif package_name.startswith('com.huawei.'):
            return "Huawei"
        elif '.' not in package_name:
            return "System"
        else:
            return "User App"
    
    def is_safe_to_remove(self, package_name: str) -> bool:
        """Check if a package is generally safe to remove."""
        # Critical system packages that should never be removed
        critical_packages = [
            'com.android.systemui',
            'com.android.settings',
            'com.android.launcher',
            'com.android.phone',
            'com.android.contacts',
            'com.android.dialer',
            'com.android.mms',
            'com.android.bluetooth',
            'com.android.wifi',
            'com.android.nfc',
            'com.android.packageinstaller',
            'com.android.permissioncontroller',
            'com.google.android.gms',
            'com.google.android.gsf',
            'com.vivo.launcher',
            'com.vivo.systemui',
            'com.vivo.settings',
        ]
        
        for critical in critical_packages:
            if package_name.startswith(critical):
                return False
        
        return True
    
    def check_adb_connection(self):
        """Check if ADB is connected and device is authorized."""
        try:
            result = self.run_command('adb devices')
            if result and 'device' in result and 'unauthorized' not in result:
                device_lines = [line for line in result.split('\n') if '\tdevice' in line]
                if device_lines:
                    self.status_label.config(text="Connected ✓", foreground="green")
                    self.scan_btn.config(state="normal")
                    logger.info("ADB device connected and authorized")
                    return True
            
            self.status_label.config(text="Not Connected ✗", foreground="red")
            self.scan_btn.config(state="disabled")
            logger.warning("ADB device not connected or not authorized")
            return False
            
        except Exception as e:
            self.status_label.config(text="Error ✗", foreground="red")
            self.scan_btn.config(state="disabled")
            logger.error(f"Error checking ADB connection: {e}")
            return False
    
    def run_command(self, cmd: str, timeout: int = 30) -> str:
        """Run a shell command with timeout and return its output."""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Command failed '{cmd}': {result.stderr}")
                return ''
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {cmd}")
            return ''
        except Exception as e:
            logger.error(f"Error running command '{cmd}': {e}")
            return ''
    
    def is_chinese_text(self, text: str) -> bool:
        """Check if text contains Chinese characters (comprehensive detection)."""
        if not text:
            return False
        
        # CJK character ranges
        cjk_ranges = [
            (0x4E00, 0x9FFF),    # CJK Unified Ideographs
            (0x3400, 0x4DBF),    # CJK Extension A
            (0x20000, 0x2A6DF),  # CJK Extension B
            (0x2A700, 0x2B73F),  # CJK Extension C
            (0x2B740, 0x2B81F),  # CJK Extension D
            (0x2B820, 0x2CEAF),  # CJK Extension E
            (0x2CEB0, 0x2EBEF),  # CJK Extension F
            (0x3000, 0x303F),    # CJK Symbols and Punctuation
            (0x3040, 0x309F),    # Hiragana
            (0x30A0, 0x30FF),    # Katakana
        ]
        
        for char in text:
            char_code = ord(char)
            for start, end in cjk_ranges:
                if start <= char_code <= end:
                    return True
        return False
    
    def start_scan(self):
        """Start scanning for apps in a separate thread."""
        if self.is_scanning:
            return
        
        self.is_scanning = True
        self.scan_btn.config(state="disabled")
        self.debloat_btn.config(state="disabled")
        self.select_all_btn.config(state="disabled")
        self.clear_selection_btn.config(state="disabled")
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.chinese_apps.clear()
        self.all_packages.clear()
        self.all_tree_items.clear()  # Clear stored items
        self.selected_apps.clear()
        self.update_selection_label()
        
        # Start scanning thread
        if self.scan_mode == "chinese":
            thread = threading.Thread(target=self.scan_for_chinese_apps, daemon=True)
        else:
            thread = threading.Thread(target=self.scan_all_packages, daemon=True)
        thread.start()
    
    def scan_all_packages(self):
        """Scan for all system packages - runs in separate thread."""
        try:
            # Check if required tools are available
            missing_tools = self.check_tools_availability()
            if 'ADB (Android Debug Bridge)' in missing_tools:
                error_msg = "ADB (Android Debug Bridge) is required but not found.\n\n"
                error_msg += "Please install Android SDK Platform Tools.\n"
                error_msg += "See README.md for detailed setup instructions."
                raise Exception(error_msg)
            
            self.progress_var.set("Getting all installed packages...")
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start()
            
            # Get list of all installed packages
            packages_output = self.run_command('adb shell pm list packages')
            if not packages_output:
                raise Exception("Failed to get package list. Ensure device is connected and authorized.")
            
            packages = [line.replace('package:', '') for line in packages_output.split('\n') if line.strip()]
            logger.info(f"Found {len(packages)} packages to analyze")
            
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate', maximum=len(packages))
            
            all_packages = []
            
            for idx, pkg in enumerate(packages):
                if not self.is_scanning:  # Allow cancellation
                    break
                
                self.progress_var.set(f"Processing {idx+1}/{len(packages)}: {pkg}")
                self.progress_bar.config(value=idx+1)
                self.root.update_idletasks()
                
                try:
                    # Get package info
                    pkg_type = self.get_package_type(pkg)
                    
                    # Try to get app label
                    label = self.get_app_label_quick(pkg)
                    if not label:
                        # Try alternative method
                        label = self.get_app_name_from_dumpsys(pkg)
                    if not label:
                        label = pkg.split('.')[-1]  # Use last part of package name
                    
                    # Check if it's safe to remove
                    safety_warning = "" if self.is_safe_to_remove(pkg) else " ⚠️"
                    
                    # Check if it's Chinese
                    is_chinese = self.is_chinese_text(label)
                    chinese_marker = " 中文" if is_chinese else ""
                    
                    display_label = f"{label}{chinese_marker}{safety_warning}"
                    
                    all_packages.append((pkg, display_label, pkg_type))
                    
                    # Add to GUI tree (thread-safe)
                    self.add_tree_item_threadsafe((pkg, display_label, pkg_type, "Ready"), ('unchecked',))
                    
                except Exception as e:
                    logger.error(f"Error processing {pkg}: {e}")
                    continue
            
            self.all_packages = all_packages
            
            # Update UI
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            self.root.after(0, lambda: self.show_error(f"Scan failed: {e}"))
            self.root.after(0, self.scan_complete)
    
    def get_app_name_from_dumpsys(self, package_name: str) -> str:
        """Get app name using dumpsys package info."""
        try:
            dumpsys_output = self.run_command(f'adb shell dumpsys package {package_name}')
            if not dumpsys_output:
                return None
            
            # Look for application label in different formats
            for line in dumpsys_output.split('\n'):
                line = line.strip()
                if 'applicationInfo' in line and 'name=' in line:
                    # Extract name from applicationInfo line
                    name_start = line.find('name=')
                    if name_start != -1:
                        name_start += 5
                        name_end = line.find(' ', name_start)
                        if name_end == -1:
                            name_end = len(line)
                        return line[name_start:name_end].strip()
                
                # Look for other label patterns
                if 'label=' in line:
                    label_start = line.find('label=')
                    if label_start != -1:
                        label_start += 6
                        label_end = line.find(' ', label_start)
                        if label_end == -1:
                            label_end = len(line)
                        return line[label_start:label_end].strip()
            
            return None
            
        except Exception as e:
            logger.debug(f"Dumpsys name lookup failed for {package_name}: {e}")
            return None
    
    def check_tools_availability(self):
        """Check if required tools are available."""
        missing_tools = []
        
        # Check ADB
        if not self.run_command('adb version'):
            missing_tools.append('ADB (Android Debug Bridge)')
        
        # Check AAPT
        if not self.run_command('aapt version'):
            missing_tools.append('AAPT (Android Asset Packaging Tool)')
        
        return missing_tools
    
    def scan_for_chinese_apps(self):
        """Scan for Chinese apps - runs in separate thread."""
        try:
            # Check if required tools are available
            missing_tools = self.check_tools_availability()
            if missing_tools:
                error_msg = f"Missing required tools: {', '.join(missing_tools)}\n\n"
                error_msg += "Please install Android SDK Build Tools and Platform Tools.\n"
                error_msg += "See README.md for detailed setup instructions."
                raise Exception(error_msg)
            
            self.progress_var.set("Getting package list...")
            self.progress_bar.config(mode='indeterminate')
            self.progress_bar.start()
            
            # Get list of all installed packages
            packages_output = self.run_command('adb shell pm list packages')
            if not packages_output:
                raise Exception("Failed to get package list. Ensure device is connected and authorized.")
            
            packages = [line.replace('package:', '') for line in packages_output.split('\n') if line.strip()]
            logger.info(f"Found {len(packages)} packages to analyze")
            
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate', maximum=len(packages))
            
            temp_dir = tempfile.mkdtemp()
            chinese_apps = []
            
            try:
                for idx, pkg in enumerate(packages):
                    if not self.is_scanning:  # Allow cancellation
                        break
                    
                    self.progress_var.set(f"Processing {idx+1}/{len(packages)}: {pkg}")
                    self.progress_bar.config(value=idx+1)
                    self.root.update_idletasks()
                    
                    try:
                        # Try alternative method first: get app info without pulling APK
                        chinese_label = self.get_app_label_quick(pkg)
                        
                        if not chinese_label:
                            # Fallback to APK analysis if quick method fails
                            chinese_label = self.get_app_label_from_apk(pkg, temp_dir)
                        
                        if chinese_label:
                            pkg_type = self.get_package_type(pkg)
                            safety_warning = "" if self.is_safe_to_remove(pkg) else " ⚠️"
                            display_label = f"{chinese_label}{safety_warning}"
                            
                            chinese_apps.append((pkg, chinese_label))
                            logger.info(f"Found Chinese app: {pkg} - {chinese_label}")
                            
                            # Add to GUI tree (thread-safe)
                            self.add_tree_item_threadsafe((pkg, display_label, pkg_type, "Ready"), ('unchecked',))
                            
                    except Exception as e:
                        logger.error(f"Error processing {pkg}: {e}")
                        continue
            
            finally:
                # Clean up temp directory
                try:
                    os.rmdir(temp_dir)
                except:
                    pass
            
            self.chinese_apps = chinese_apps
            
            # Update UI
            self.root.after(0, self.scan_complete)
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            self.root.after(0, lambda: self.show_error(f"Scan failed: {e}"))
            self.root.after(0, self.scan_complete)
    
    def get_app_label_quick(self, package_name: str) -> str:
        """Try to get app label using dumpsys (faster method)."""
        try:
            # Get app info using dumpsys
            dumpsys_output = self.run_command(f'adb shell dumpsys package {package_name}')
            if not dumpsys_output:
                return None
            
            # Look for application label in dumpsys output
            # This is less reliable but doesn't require APK pulling
            for line in dumpsys_output.split('\n'):
                line = line.strip()
                if 'applicationInfo' in line or 'label' in line.lower():
                    # Extract potential label text
                    parts = line.split()
                    for part in parts:
                        if self.is_chinese_text(part):
                            return part
            
            return None
            
        except Exception as e:
            logger.debug(f"Quick label check failed for {package_name}: {e}")
            return None
    
    def get_app_label_from_apk(self, package_name: str, temp_dir: str) -> str:
        """Get app label by analyzing APK file."""
        try:
            # Get APK path on device
            path_output = self.run_command(f'adb shell pm path {package_name}')
            if not path_output:
                return None
            
            apk_path = path_output.split('\n')[0].replace('package:', '').strip()
            
            # Pull APK to temp dir
            local_apk = os.path.join(temp_dir, f'{package_name}.apk')
            pull_result = self.run_command(f'adb pull "{apk_path}" "{local_apk}"')
            
            if 'error' in pull_result.lower() or not os.path.exists(local_apk):
                return None
            
            try:
                # Use aapt to get badging info
                badging = self.run_command(f'aapt dump badging "{local_apk}"')
                if not badging:
                    return None
                
                # Extract application labels
                labels = []
                
                # Default label
                match = re.search(r"application-label:'([^']*)'", badging)
                if match:
                    labels.append(match.group(1))
                
                # Localized labels
                for match in re.finditer(r"application-label-([^:]+):'([^']*)'", badging):
                    labels.append(match.group(2))
                
                # Check for Chinese in any label
                for label in labels:
                    if self.is_chinese_text(label):
                        return label
                
                return None
                
            finally:
                # Clean up APK
                if os.path.exists(local_apk):
                    os.remove(local_apk)
            
        except Exception as e:
            logger.debug(f"APK analysis failed for {package_name}: {e}")
            return None
    
    def scan_complete(self):
        """Called when scan is complete."""
        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.update_button_states()
        
        if self.scan_mode == "chinese":
            if self.chinese_apps:
                self.progress_var.set(f"Scan complete. Found {len(self.chinese_apps)} Chinese apps.")
                messagebox.showinfo("Scan Complete", 
                                  f"Found {len(self.chinese_apps)} apps with Chinese labels.\n"
                                  f"Select apps and click 'Uninstall Selected Apps' to remove them.")
            else:
                self.progress_var.set("Scan complete. No Chinese apps found.")
                messagebox.showinfo("Scan Complete", "No apps with Chinese labels were found.")
        else:
            if self.all_packages:
                self.progress_var.set(f"Scan complete. Found {len(self.all_packages)} total packages.")
                messagebox.showinfo("Scan Complete", 
                                  f"Found {len(self.all_packages)} total packages.\n"
                                  f"⚠️ Warning: Be careful when removing system packages!\n"
                                  f"Packages marked with ⚠️ may be critical for system operation.\n"
                                  f"Select apps carefully and click 'Uninstall Selected Apps'.")
            else:
                self.progress_var.set("Scan complete. No packages found.")
                messagebox.showinfo("Scan Complete", "No packages were found.")
        
        self.progress_bar.config(value=0)
    
    def start_debloat(self):
        """Start debloating process."""
        if not self.selected_apps or self.is_debloating:
            return
        
        # Count critical packages
        critical_count = 0
        for pkg in self.selected_apps:
            if not self.is_safe_to_remove(pkg):
                critical_count += 1
        
        # Create warning message
        warning_msg = f"This will uninstall {len(self.selected_apps)} selected apps from your device.\n\n"
        
        if critical_count > 0:
            warning_msg += f"⚠️ WARNING: {critical_count} of the selected apps may be critical for system operation!\n"
            warning_msg += "Removing these apps could cause system instability or loss of functionality.\n\n"
        
        warning_msg += "Apps will be uninstalled for the current user only (not system-wide).\n"
        warning_msg += "App data is preserved and apps can be restored later.\n\n"
        warning_msg += "Continue with uninstalling the selected apps?"
        
        # Confirm with user
        response = messagebox.askyesnocancel(
            "Confirm Uninstall",
            warning_msg,
            icon='warning' if critical_count > 0 else 'question'
        )
        
        if not response:
            return
        
        self.is_debloating = True
        self.debloat_btn.config(state="disabled")
        self.scan_btn.config(state="disabled")
        self.select_all_btn.config(state="disabled")
        self.clear_selection_btn.config(state="disabled")
        
        # Start debloating thread
        thread = threading.Thread(target=self.debloat_apps, daemon=True)
        thread.start()
    
    def debloat_apps(self):
        """Debloat the selected apps - runs in separate thread."""
        try:
            success_count = 0
            selected_list = list(self.selected_apps)
            self.progress_bar.config(mode='determinate', maximum=len(selected_list))
            
            for idx, pkg in enumerate(selected_list):
                if not self.is_debloating:  # Allow cancellation
                    break
                
                self.progress_var.set(f"Uninstalling {idx+1}/{len(selected_list)}: {pkg}")
                self.progress_bar.config(value=idx+1)
                self.root.update_idletasks()
                
                # Update tree status
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    if values and values[0] == pkg:
                        self.root.after(0, lambda i=item: 
                                       self.tree.set(i, "Status", "Processing..."))
                        break
                
                # Try multiple uninstall methods
                success = False
                
                # Method 1: Standard user uninstall
                uninstall_result = self.run_command(f'adb shell pm uninstall -k --user 0 {pkg}')
                if 'success' in uninstall_result.lower():
                    success = True
                    status = "Uninstalled ✓"
                else:
                    # Method 2: Disable package
                    disable_result = self.run_command(f'adb shell pm disable-user --user 0 {pkg}')
                    if 'new state: disabled' in disable_result.lower() or 'disabled' in disable_result.lower():
                        success = True
                        status = "Disabled ✓"
                    else:
                        # Method 3: Hide package
                        hide_result = self.run_command(f'adb shell pm hide {pkg}')
                        if 'true' in hide_result.lower():
                            success = True
                            status = "Hidden ✓"
                        else:
                            status = "Failed ✗"
                
                if success:
                    success_count += 1
                    logger.info(f"Successfully processed {pkg}: {status}")
                else:
                    logger.warning(f"Failed to process {pkg}")
                
                # Update tree status
                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    if values and values[0] == pkg:
                        self.root.after(0, lambda i=item, s=status: 
                                       self.tree.set(i, "Status", s))
                        break
                
                time.sleep(0.1)  # Small delay to prevent overwhelming the device
            
            # Update UI
            self.root.after(0, lambda: self.debloat_complete(success_count, len(selected_list)))
            
        except Exception as e:
            logger.error(f"Debloat failed: {e}")
            self.root.after(0, lambda: self.show_error(f"Debloat failed: {e}"))
            self.root.after(0, lambda: self.debloat_complete(0, len(self.selected_apps)))
    
    def debloat_complete(self, success_count: int, total_count: int):
        """Called when debloat is complete."""
        self.is_debloating = False
        self.scan_btn.config(state="normal")
        self.update_button_states()
        
        self.progress_var.set(f"Uninstall complete. {success_count}/{total_count} apps processed.")
        
        message = (f"Uninstall process complete!\n\n"
                  f"Successfully processed: {success_count}/{total_count} apps\n\n"
                  f"Methods used:\n"
                  f"• Uninstalled: Apps removed for current user\n"
                  f"• Disabled: Apps disabled but still present\n"
                  f"• Hidden: Apps hidden from launcher\n\n"
                  f"Recommendations:\n"
                  f"• Reboot your device for changes to take effect\n"
                  f"• Apps can be restored using the 'Restore Apps' feature\n"
                  f"• Check your device functionality after reboot")
        
        messagebox.showinfo("Uninstall Complete", message)
        
        # Save backup list
        self.save_backup_list()
    
    def create_backup(self):
        """Create a backup list of detected apps."""
        apps_to_backup = []
        
        if self.scan_mode == "chinese" and self.chinese_apps:
            apps_to_backup = [{'package': pkg, 'label': label, 'type': 'Chinese'} 
                            for pkg, label in self.chinese_apps]
        elif self.scan_mode == "all" and self.all_packages:
            apps_to_backup = [{'package': pkg, 'label': label, 'type': pkg_type} 
                            for pkg, label, pkg_type in self.all_packages]
        
        if not apps_to_backup:
            messagebox.showwarning("No Apps", "No apps detected. Run a scan first.")
            return
        
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'device_info': self.get_device_info(),
                'scan_mode': self.scan_mode,
                'apps': apps_to_backup
            }
            
            mode_suffix = "chinese" if self.scan_mode == "chinese" else "all"
            backup_file = f"apps_backup_{mode_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Backup Created", f"Backup saved as: {backup_file}")
            logger.info(f"Backup created: {backup_file}")
            
        except Exception as e:
            self.show_error(f"Failed to create backup: {e}")
    
    def save_backup_list(self):
        """Automatically save backup list after debloating."""
        try:
            # Create backup of processed apps
            processed_apps = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                if values and len(values) >= 4:
                    pkg, label, pkg_type, status = values[0], values[1], values[2], values[3]
                    if "✓" in status:  # Only include successfully processed apps
                        processed_apps.append({
                            'package': pkg, 
                            'label': label, 
                            'type': pkg_type,
                            'status': status
                        })
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'device_info': self.get_device_info(),
                'scan_mode': self.scan_mode,
                'processed_apps': processed_apps
            }
            
            with open('last_uninstall_backup.json', 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Auto-backup saved: last_uninstall_backup.json")
            
        except Exception as e:
            logger.error(f"Failed to save auto-backup: {e}")
    
    def restore_apps(self):
        """Restore previously uninstalled apps."""
        try:
            # Look for backup file
            backup_file = 'last_uninstall_backup.json'
            if not os.path.exists(backup_file):
                # Try old backup file format
                backup_file = 'last_debloat_backup.json'
                if not os.path.exists(backup_file):
                    messagebox.showwarning("No Backup", "No backup file found. Cannot restore apps.")
                    return
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Handle both old and new backup formats
            if 'processed_apps' in backup_data:
                apps_to_restore = backup_data['processed_apps']
            elif 'debloated_apps' in backup_data:
                apps_to_restore = backup_data['debloated_apps']
            else:
                apps_to_restore = backup_data.get('apps', [])
            
            if not apps_to_restore:
                messagebox.showwarning("No Apps", "No apps to restore in backup file.")
                return
            
            response = messagebox.askyesno(
                "Confirm Restore",
                f"This will attempt to restore {len(apps_to_restore)} previously processed apps.\n\n"
                f"Methods will include:\n"
                f"• Re-installing uninstalled apps\n"
                f"• Re-enabling disabled apps\n"
                f"• Unhiding hidden apps\n\n"
                f"Continue?"
            )
            
            if not response:
                return
            
            # Restore apps
            success_count = 0
            for app in apps_to_restore:
                pkg = app['package']
                
                # Try multiple restore methods
                restored = False
                
                # Method 1: Install existing (for uninstalled apps)
                result = self.run_command(f'adb shell cmd package install-existing {pkg}')
                if 'success' in result.lower() or 'installed' in result.lower():
                    restored = True
                    logger.info(f"Re-installed {pkg}")
                
                # Method 2: Enable (for disabled apps)
                if not restored:
                    result = self.run_command(f'adb shell pm enable {pkg}')
                    if 'enabled' in result.lower() or 'new state: enabled' in result.lower():
                        restored = True
                        logger.info(f"Re-enabled {pkg}")
                
                # Method 3: Unhide (for hidden apps)
                if not restored:
                    result = self.run_command(f'adb shell pm unhide {pkg}')
                    if 'false' in result.lower():  # unhide returns false when successful
                        restored = True
                        logger.info(f"Unhidden {pkg}")
                
                if restored:
                    success_count += 1
                else:
                    logger.warning(f"Failed to restore {pkg}")
            
            messagebox.showinfo("Restore Complete", 
                              f"Restored {success_count}/{len(apps_to_restore)} apps.\n"
                              f"Reboot your device for changes to take effect.")
            
        except Exception as e:
            self.show_error(f"Restore failed: {e}")
    
    def get_device_info(self) -> dict:
        """Get device information."""
        try:
            info = {}
            info['model'] = self.run_command('adb shell getprop ro.product.model')
            info['brand'] = self.run_command('adb shell getprop ro.product.brand')
            info['version'] = self.run_command('adb shell getprop ro.build.version.release')
            info['sdk'] = self.run_command('adb shell getprop ro.build.version.sdk')
            return info
        except:
            return {}
    
    def show_error(self, message: str):
        """Show error message."""
        messagebox.showerror("Error", message)

def main():
    """Main function."""
    try:
        # Create and run GUI first, then check tools
        root = tk.Tk()
        app = AndroidDebloaterGUI(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Check for missing tools after GUI is created
        def check_tools_on_startup():
            missing_tools = []
            
            # Check if ADB is available
            try:
                subprocess.run(['adb', 'version'], capture_output=True, check=True, timeout=5)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                missing_tools.append('ADB (Android Debug Bridge)')
            
            # Check if AAPT is available (optional - we have fallback)
            try:
                subprocess.run(['aapt', 'version'], capture_output=True, check=True, timeout=5)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                # AAPT missing is not critical - we have alternative method
                logger.warning("AAPT not found - will use alternative detection method")
            
            if missing_tools:
                message = (
                    f"Missing required tools: {', '.join(missing_tools)}\n\n"
                    f"To use this application, you need:\n"
                    f"1. Android SDK Platform Tools (for ADB)\n"
                    f"2. Android SDK Build Tools (for AAPT - optional)\n\n"
                    f"Solutions:\n"
                    f"• Run 'setup_adb.bat' for setup instructions\n"
                    f"• Download Android SDK Platform Tools\n"
                    f"• Add tools to your system PATH\n\n"
                    f"The application will still work with limited functionality."
                )
                messagebox.showwarning("Missing Tools", message)
        
        # Check tools after a short delay to let GUI initialize
        root.after(1000, check_tools_on_startup)
        
        root.mainloop()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        try:
            messagebox.showerror("Fatal Error", f"An unexpected error occurred: {e}")
        except:
            print(f"Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()