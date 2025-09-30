#!/usr/bin/env python3
"""
GlobalExam AI - Simple GUI Launcher
==================================

A simple graphical interface to launch the GlobalExam AI application
with different options and configurations.

Author: Student Project
Purpose: Easy-to-use launcher for the automation system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os
import threading
from pathlib import Path

class GlobalExamLauncher:
    """Simple GUI launcher for GlobalExam AI"""
    
    def __init__(self):
        """Initialize the launcher GUI"""
        self.root = tk.Tk()
        self.root.title("GlobalExam AI - Launcher")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Python executable path
        self.python_exe = r"C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe"
        
        # Check if files exist
        self.main_app_path = Path("main_application.py")
        self.python_exists = Path(self.python_exe).exists()
        
        self.create_widgets()
        self.check_system_status()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="GlobalExam AI", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Ultimate Automation System")
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = tk.StringVar()
        status_label = ttk.Label(status_frame, textvariable=self.status_text)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Action buttons frame
        buttons_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        buttons_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # First time setup
        setup_btn = ttk.Button(buttons_frame, text="🔧 First Time Setup", 
                              command=self.setup_security, width=20)
        setup_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Install dependencies
        deps_btn = ttk.Button(buttons_frame, text="📦 Install Dependencies", 
                             command=self.install_dependencies, width=20)
        deps_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Show daily code
        code_btn = ttk.Button(buttons_frame, text="🔑 Show Daily Code", 
                             command=self.show_daily_code, width=20)
        code_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Disable security
        disable_btn = ttk.Button(buttons_frame, text="🔓 Disable Security", 
                                command=self.disable_security, width=20)
        disable_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Main run buttons frame
        run_frame = ttk.LabelFrame(main_frame, text="Run Application", padding="10")
        run_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Normal run
        run_btn = ttk.Button(run_frame, text="🚀 Run GlobalExam AI", 
                            command=self.run_normal, width=25)
        run_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Debug run
        debug_btn = ttk.Button(run_frame, text="🐛 Run with Debug", 
                              command=self.run_debug, width=25)
        debug_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Max questions
        ttk.Label(options_frame, text="Max Questions:").grid(row=0, column=0, sticky=tk.W)
        self.max_questions = tk.StringVar(value="30")
        questions_spinbox = ttk.Spinbox(options_frame, from_=1, to=100, 
                                       textvariable=self.max_questions, width=10)
        questions_spinbox.grid(row=0, column=1, padx=(5, 0))
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, width=70)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
    
    def check_system_status(self):
        """Check and display system status"""
        status_parts = []
        
        if self.python_exists:
            status_parts.append("✓ Python 3.13 Found")
        else:
            status_parts.append("✗ Python 3.13 Not Found")
        
        if self.main_app_path.exists():
            status_parts.append("✓ Main Application Found")
        else:
            status_parts.append("✗ Main Application Missing")
        
        self.status_text.set(" | ".join(status_parts))
    
    def log_output(self, message):
        """Add message to output text area"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def run_command(self, args, description):
        """Run a command and show output"""
        self.log_output(f"=== {description} ===")
        
        if not self.python_exists:
            self.log_output("ERROR: Python 3.13 not found!")
            messagebox.showerror("Error", "Python 3.13 not found at expected location!")
            return
        
        def run_in_thread():
            try:
                process = subprocess.Popen(
                    [self.python_exe] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Read output line by line
                for line in process.stdout:
                    self.root.after(0, lambda l=line: self.log_output(l.strip()))
                
                process.wait()
                
                if process.returncode == 0:
                    self.root.after(0, lambda: self.log_output(f"✓ {description} completed successfully"))
                else:
                    self.root.after(0, lambda: self.log_output(f"✗ {description} failed with code {process.returncode}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_output(f"ERROR: {str(e)}"))
        
        # Run in background thread
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
    
    def setup_security(self):
        """Setup security system"""
        self.run_command(["main_application.py", "--setup-security"], "Security Setup")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.log_output("=== Installing Dependencies ===")
        
        # Install packages one by one for better feedback
        packages = [
            "pyautogui", "Pillow", "opencv-python", 
            "numpy", "pytesseract", "requests", "psutil"
        ]
        
        def install_package(package):
            self.run_command(["-m", "pip", "install", package], f"Installing {package}")
        
        for package in packages:
            install_package(package)
    
    def show_daily_code(self):
        """Show today's daily code"""
        self.run_command(["main_application.py", "--show-daily-code"], "Show Daily Code")
    
    def disable_security(self):
        """Disable security system"""
        result = messagebox.askyesno("Disable Security", 
                                   "Are you sure you want to disable the security system?\n"
                                   "This will allow the app to run without approval codes.")
        if result:
            self.run_command(["main_application.py", "--disable-security"], "Disable Security")
    
    def run_normal(self):
        """Run the application normally"""
        max_q = self.max_questions.get()
        args = ["main_application.py", "--max-questions", max_q]
        self.run_command(args, f"GlobalExam AI (Max: {max_q} questions)")
    
    def run_debug(self):
        """Run the application in debug mode"""
        max_q = self.max_questions.get()
        args = ["main_application.py", "--debug", "--max-questions", max_q]
        self.run_command(args, f"GlobalExam AI Debug Mode (Max: {max_q} questions)")
    
    def run(self):
        """Start the GUI"""
        try:
            self.log_output("GlobalExam AI Launcher Started")
            self.log_output("Ready to run automation system...")
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_output("Launcher closed by user")

def main():
    """Main entry point"""
    try:
        launcher = GlobalExamLauncher()
        launcher.run()
    except Exception as e:
        print(f"Launcher error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
