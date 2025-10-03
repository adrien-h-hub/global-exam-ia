#!/usr/bin/env python3
"""
GlobalExam AI - Universal Launcher
==================================
Works both locally and when downloaded from GitHub
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Main launcher that works everywhere"""
    try:
        # Try to import the launcher
        try:
            from launch_secure_app import main as launch_main
        except ImportError:
            print("❌ Cannot find launch_secure_app.py")
            print("Make sure all files are in the same directory")
            return
        
        # Run the main application
        launch_main()
        
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("Vérifiez que tous les fichiers sont présents")

if __name__ == "__main__":
    main()
