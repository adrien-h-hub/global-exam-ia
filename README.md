# GlobalExam AI - Automation System

[![GitHub](https://img.shields.io/badge/GitHub-adrien--h--hub%2Fglobal--exam--ia-blue?logo=github)](https://github.com/adrien-h-hub/global-exam-ia)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An advanced AI-powered automation system featuring security, OCR, AI analysis, and visual automation.

## 🚀 Quick Start

### **🔧 Automatic Installation (Recommended)**

```bash
# Clone repository
git clone https://github.com/adrien-h-hub/global-exam-ia.git
cd global-exam-ia

# Windows: Double-click this file
INSTALL_AND_RUN.bat

# Or run with Python
python auto_setup.py
```

### **📋 Manual Installation**

```bash
# Install dependencies manually
pip install -r requirements-client.txt

# Run application
python run_app.py
```

## 📸 Screenshots

````
{{ ... }}
 ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║
 ██║  ███╗██║     ██║   ██║██████╔╝███████║██║     █████╗   ╚███╔╝ ███████║██╔████╔██║
 ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║
 ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║
  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                                                        
                           █████╗ ██╗    ██╗   ██╗██╗  ██╗                           
                          ██╔══██╗██║    ██║   ██║██║  ██║                           
                          ███████║██║    ██║   ██║███████║                           
                          ██╔══██║██║    ╚██╗ ██╔╝╚════██║                           
                          ██║  ██║██║     ╚████╔╝      ██║                           
                          ╚═╝  ╚═╝╚═╝      ╚═══╝       ╚═╝                           
                                                                                        
                    🤖 SYSTÈME D'AUTOMATISATION INTELLIGENT 🤖                       
```

## 🏗️ Architecture

```
global-exam-ia/
├── 📄 README.md                    # Main documentation
├── 📄 INSTALLATION_FR.md           # French installation guide
├── 📄 ACADEMIC_OVERVIEW.md         # Educational overview
├── 📄 DEPLOY_GLOBAL.md             # Global deployment guide
├── 📄 requirements.txt             # Server dependencies (minimal)
├── 📄 requirements-client.txt      # Full client dependencies
├── 📄 LICENSE                      # MIT License
├── 📄 .python-version              # Python version for Heroku
├── 📄 Procfile                     # Heroku deployment config
├── 🚀 launch.bat                   # Windows launcher
├── 🚀 INSTALL_AND_RUN.bat          # Auto-installer (Windows)
├── 🐍 __init__.py                  # Python package file
├── 🐍 auto_setup.py                # Smart auto-installer
├── 🐍 run_app.py                   # Universal launcher
├── 🐍 launch_secure_app.py         # Main launcher
├── 🐍 main_application.py          # Core application
├── 🐍 security_system_v4.py        # Security system v4
├── 🐍 control_panel.py             # Owner control panel
├── 🐍 server.py                    # Global server (Heroku)
├── 🐍 ocr_ai_analysis.py          # OCR & AI analysis
├── 🐍 visual_automation.py        # Visual automation
├── 🐍 adaptive_clicking_system.py # Adaptive clicking
├── 🐍 test_adaptive_system.py     # Adaptive testing
├── 🐍 app_launcher.py             # GUI launcher
├── 🐍 create_shortcuts.py         # Desktop shortcuts
├── 🧪 accuracy_tester.py           # Simulated accuracy testing
├── 🧪 real_accuracy_test.py        # Real-world testing
├── 🧪 test_runner.py               # Complete test suite
├── 🧪 quick_accuracy_test.py       # Fast accuracy test
└── 📁 assets/                     # Logo and icons
    ├── logo.txt                   # ASCII logo
    └── icon.txt                   # Text icon
```

## 🔧 Core Features

### 🔐 Security System v4
- Server-controlled access management
- No visible codes to end users
- Owner control panel interface
- Complete usage logging
- Instant access revocation
- Global server deployment (Heroku)

### 🧠 AI Analysis
- Automatic question type detection
- Intelligent answer generation
- OCR text extraction
- Context-aware processing
- Multi-language support

### 🎯 Adaptive Automation
- Dynamic element detection
- Multiple clicking strategies
- Visual validation
- Error recovery systems
- Image recognition (0.85 confidence)

### 🔧 Auto-Installation
- Smart dependency detection
- One-click Windows installer
- Cross-platform compatibility
- Automatic Tesseract OCR setup
- Desktop shortcut creation

### 🧪 Accuracy Testing
- Comprehensive test suite
- Real-world performance testing
- Simulated accuracy testing
- Performance benchmarking
- Detailed reporting system

## 🎮 Usage

### 🚀 Quick Start (Auto-Installation)
```bash
# Windows: Double-click
INSTALL_AND_RUN.bat

# Or with Python
python auto_setup.py
```

### 👥 For Users
```bash
python run_app.py
# → Option 1: Main Application
# → Enter name/email
# → Wait for owner approval
```

### 🎛️ For Owners
```bash
python launch_secure_app.py
# → Option 2: Control Panel
# → Enter access code: 602172
# → Manage user access globally
```

### 🧪 Testing & Accuracy
```bash
# Quick accuracy test (30 seconds)
python quick_accuracy_test.py

# Complete test suite
python test_runner.py

# Real-world testing
python real_accuracy_test.py
```

### 🌐 Global Control
- **Admin Dashboard**: https://your-app.herokuapp.com/admin/dashboard
- **Mobile-friendly**: Control from any device
- **Real-time**: See requests instantly

## 📋 Requirements

### 🖥️ System Requirements
- **Python 3.8+** (3.11+ recommended)
- **Windows 10/11** (64-bit)
- **4GB RAM** minimum
- **Internet connection** (for global features)

### 📦 Dependencies
- **Auto-installed**: Run `python auto_setup.py`
- **Manual**: `pip install -r requirements-client.txt`
- **Server only**: `pip install -r requirements.txt`

### 🌐 Global Features
- **Heroku account** (for global deployment)
- **GitHub repository** (for code sharing)
- **Mobile device** (for remote control)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Adrien H** - [adrien-h-hub](https://github.com/adrien-h-hub)

---

⭐ **Star this repository if it helped you!**
