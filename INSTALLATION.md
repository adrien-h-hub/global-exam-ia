# Installation and Setup Guide

## 🚀 Quick Start

### Prerequisites
- Windows 10/11 (64-bit)
- Python 3.8 or higher
- Administrative privileges (for Tesseract installation)
- Internet connection (for auto-installation)

### One-Command Installation
```bash
# Run this single command to install everything automatically
python main_application.py --setup-security
```

## 📋 Detailed Installation Steps

### Step 1: Python Setup
If you don't have Python installed:

1. Download Python from [python.org](https://python.org)
2. During installation, check "Add Python to PATH"
3. Verify installation:
```bash
python --version
```

### Step 2: Download the Project
```bash
# Clone or download the project files
git clone https://github.com/yourusername/globalexam-ai.git
cd globalexam-ai
```

### Step 3: Run Auto-Installation
```bash
# This will automatically install all dependencies
python main_application.py --setup-security
```

The auto-installer will:
- Install Python packages (PyAutoGUI, OpenCV, Pillow, etc.)
- Download and install Tesseract OCR
- Configure system paths
- Set up security system

### Step 4: Security Configuration
During setup, you'll be prompted for:

1. **Master Secret**: Your password for generating daily codes
2. **Security Mode**: 
   - `daily` (recommended): Codes change every day
   - `static`: Same code always
3. **Enforcement**: Whether to require approval every run

Example setup:
```
Enter master secret (password): MySecretPassword123
Security mode (daily/static) [daily]: daily
Require approval every run? (y/n) [y]: y
```

## 🔧 Manual Installation (If Auto-Install Fails)

### Install Python Packages
```bash
pip install pyautogui
pip install Pillow
pip install opencv-python
pip install numpy
pip install pytesseract
```

### Install Tesseract OCR Manually

1. Download Tesseract installer:
   - Go to: https://github.com/UB-Mannheim/tesseract/releases
   - Download: `tesseract-ocr-w64-setup-5.3.0.20221214.exe`

2. Run installer with admin privileges
3. Add to PATH: `C:\Program Files\Tesseract-OCR`

### Verify Installation
```bash
# Test Tesseract
tesseract --version

# Test Python packages
python -c "import pyautogui, cv2, pytesseract; print('All packages OK')"
```

## ⚙️ Configuration Options

### Security Settings
Located in: `%APPDATA%\GlobalExamAI\config.json`

```json
{
  "REQUIRE_APPROVAL": true,
  "CODE_MODE": "daily",
  "CODE_ENFORCE_EVERY_RUN": true,
  "APPROVAL_SECRET_HASH": "sha256_hash_here",
  "APPROVAL_OK": false,
  "APPROVAL_MACHINE_TOKEN": "",
  "APPROVAL_LAST_DATE": ""
}
```

### Application Settings
```bash
# Show current machine ID
python main_application.py --show-machine-id

# Show today's daily code
python main_application.py --show-daily-code

# Disable security (development mode)
python main_application.py --disable-security
```

## 🎮 Usage Examples

### Basic Usage
```bash
# Run with default settings
python main_application.py
```

### Advanced Usage
```bash
# Debug mode with screenshots
python main_application.py --debug

# Limit to 10 questions
python main_application.py --max-questions 10

# Development mode (no security)
python main_application.py --disable-security --debug
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "Tesseract not found" Error
```bash
# Check if Tesseract is installed
tesseract --version

# If not found, add to PATH manually:
# Windows: Add C:\Program Files\Tesseract-OCR to PATH
# Or reinstall with admin privileges
```

#### 2. "Permission Denied" Error
```bash
# Run as administrator
# Right-click Command Prompt → "Run as administrator"
python main_application.py --setup-security
```

#### 3. "Module not found" Error
```bash
# Reinstall Python packages
pip install --upgrade pyautogui opencv-python pillow numpy pytesseract
```

#### 4. Security Setup Issues
```bash
# Reset security configuration
python main_application.py --disable-security
python main_application.py --setup-security
```

### Debug Mode
Enable debug mode to see detailed logs:
```bash
python main_application.py --debug
```

This will:
- Save screenshots of each question
- Show detailed OCR text extraction
- Display AI analysis results
- Log all click coordinates

### Log Files
Check these locations for logs:
- Screenshots: `%APPDATA%\GlobalExamAI\screenshots\`
- Config: `%APPDATA%\GlobalExamAI\config.json`
- Debug images: Current directory (`question_*.png`)

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit)
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **CPU**: Intel i3 or equivalent
- **Display**: 1366x768 resolution

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **RAM**: 8 GB or more
- **Storage**: 1 GB free space
- **CPU**: Intel i5 or equivalent
- **Display**: 1920x1080 resolution

### Performance Optimization
For better performance:
1. Close unnecessary applications
2. Use dedicated graphics card if available
3. Ensure stable internet connection
4. Run from SSD if possible

## 🔒 Security Best Practices

### Master Secret Guidelines
- Use a strong, unique password
- Don't share with others
- Store securely (password manager recommended)
- Change periodically for maximum security

### Daily Code Management
```bash
# Get today's code (run this daily)
python main_application.py --show-daily-code

# Example output: Today's daily code: 123456
```

### Machine Binding
The system automatically binds to your machine using:
- MAC address of network adapter
- CPU serial number
- System UUID
- Computer name

This prevents sharing the configured system with others.

## 📱 Multiple Machine Setup

To use on multiple authorized machines:

1. **Setup on each machine separately:**
```bash
# On Machine 1
python main_application.py --setup-security
# Use same master secret

# On Machine 2  
python main_application.py --setup-security
# Use same master secret
```

2. **Each machine gets unique daily codes:**
```bash
# Machine 1 code: 123456
# Machine 2 code: 789012
# (Codes are different due to different hardware)
```

## 🔄 Updates and Maintenance

### Updating the System
```bash
# Download new version
git pull origin main

# Reinstall dependencies if needed
python main_application.py --setup-security
```

### Backup Configuration
```bash
# Backup your config (important!)
copy "%APPDATA%\GlobalExamAI\config.json" "backup_config.json"
```

### Reset to Factory Settings
```bash
# Complete reset (will require reconfiguration)
rmdir /s "%APPDATA%\GlobalExamAI"
python main_application.py --setup-security
```

## 🎯 Performance Tuning

### Optimize for Speed
```bash
# Reduce question limit for faster testing
python main_application.py --max-questions 5

# Disable debug mode in production
python main_application.py  # (no --debug flag)
```

### Optimize for Accuracy
```bash
# Enable debug mode to analyze failures
python main_application.py --debug

# Review screenshots to improve coordinate accuracy
# Check OCR text extraction quality
```

### Monitor Performance
The system provides detailed statistics:
```
Questions attempted: 25
Questions successful: 19
Success rate: 76.0%
Duration: 125.3 seconds
Average per question: 5.0 seconds
```

## 🆘 Getting Help

### Self-Diagnosis
```bash
# Run system check
python main_application.py --show-machine-id
python main_application.py --show-daily-code

# Test individual components
python security_system.py      # Test security
python ocr_ai_analysis.py      # Test OCR/AI
python visual_automation.py    # Test automation
```

### Common Solutions

| Problem | Solution |
|---------|----------|
| Low success rate | Enable debug mode, check screenshots |
| Security errors | Reconfigure with `--setup-security` |
| OCR failures | Reinstall Tesseract with admin rights |
| Click failures | Check screen resolution and scaling |
| Performance issues | Close other applications, use SSD |

### Error Codes
- **Exit Code 0**: Success
- **Exit Code 1**: General error
- **Security Error**: Approval failed
- **Module Error**: Missing dependencies

## 📞 Support Information

This is an educational project. For learning purposes:

1. **Read the documentation** thoroughly
2. **Check troubleshooting** section first
3. **Enable debug mode** to understand issues
4. **Review code comments** for technical details
5. **Experiment safely** in development mode

Remember: This project is for educational demonstration of programming concepts including automation, AI, computer vision, and security implementation.
