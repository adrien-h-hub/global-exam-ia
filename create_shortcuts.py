#!/usr/bin/env python3
"""
Desktop Shortcut Creator for GlobalExam AI
==========================================

Creates desktop shortcuts for easy access to the GlobalExam AI application.

Author: Student Project
Purpose: Easy desktop access to the automation system
"""

import os
import sys
from pathlib import Path

def create_batch_shortcut():
    """Create a batch file shortcut on desktop"""
    try:
        # Get desktop path
        desktop = Path.home() / "Desktop"
        
        # Create batch shortcut content
        batch_content = f'''@echo off
cd /d "{Path(__file__).parent.absolute()}"
call run_with_python313.bat %*
'''
        
        # Write batch file to desktop
        shortcut_path = desktop / "GlobalExam AI.bat"
        with open(shortcut_path, 'w') as f:
            f.write(batch_content)
        
        print(f"✓ Created batch shortcut: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create batch shortcut: {e}")
        return False

def create_gui_shortcut():
    """Create a GUI launcher shortcut on desktop"""
    try:
        # Get desktop path
        desktop = Path.home() / "Desktop"
        
        # Create Python GUI launcher batch
        gui_batch_content = f'''@echo off
cd /d "{Path(__file__).parent.absolute()}"
"C:\\Users\\Dardq\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" app_launcher.py
pause
'''
        
        # Write GUI batch file to desktop
        gui_shortcut_path = desktop / "GlobalExam AI - GUI.bat"
        with open(gui_shortcut_path, 'w') as f:
            f.write(gui_batch_content)
        
        print(f"✓ Created GUI shortcut: {gui_shortcut_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create GUI shortcut: {e}")
        return False

def create_setup_shortcut():
    """Create a setup shortcut on desktop"""
    try:
        # Get desktop path
        desktop = Path.home() / "Desktop"
        
        # Create setup batch content
        setup_batch_content = f'''@echo off
cd /d "{Path(__file__).parent.absolute()}"
call run_with_python313.bat --setup
'''
        
        # Write setup batch file to desktop
        setup_shortcut_path = desktop / "GlobalExam AI - Setup.bat"
        with open(setup_shortcut_path, 'w') as f:
            f.write(setup_batch_content)
        
        print(f"✓ Created setup shortcut: {setup_shortcut_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create setup shortcut: {e}")
        return False

def main():
    """Main function to create all shortcuts"""
    print("GlobalExam AI - Desktop Shortcut Creator")
    print("="*50)
    
    current_dir = Path(__file__).parent.absolute()
    print(f"Application directory: {current_dir}")
    
    # Check if we're in the right directory
    if not (current_dir / "main_application.py").exists():
        print("✗ Error: main_application.py not found in current directory")
        print("Please run this script from the GlobalExam AI directory")
        input("Press Enter to exit...")
        return
    
    print("\nCreating desktop shortcuts...")
    
    success_count = 0
    
    # Create shortcuts
    if create_batch_shortcut():
        success_count += 1
    
    if create_gui_shortcut():
        success_count += 1
    
    if create_setup_shortcut():
        success_count += 1
    
    print(f"\n✓ Created {success_count}/3 shortcuts successfully")
    
    if success_count > 0:
        print("\nDesktop shortcuts created:")
        print("• 'GlobalExam AI.bat' - Run the main application")
        print("• 'GlobalExam AI - GUI.bat' - Open the graphical launcher")
        print("• 'GlobalExam AI - Setup.bat' - First time setup")
        print("\nYou can now run GlobalExam AI from your desktop!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
