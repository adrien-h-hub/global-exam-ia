@echo off
REM GlobalExam AI - Python 3.13 Runner
REM This batch file handles Python PATH issues for Python 3.13

echo ========================================
echo GlobalExam AI - Python 3.13 Launcher
echo ========================================

REM Set Python 3.13 path
set PYTHON_EXE="C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe"

REM Check if Python exists
if not exist %PYTHON_EXE% (
    echo ERROR: Python 3.13 not found at expected location
    echo Expected: %PYTHON_EXE%
    echo Please check your Python installation
    pause
    exit /b 1
)

echo Python 3.13 found: %PYTHON_EXE%

REM Parse command line arguments
if "%1"=="--setup" goto setup
if "%1"=="--install-deps" goto install_deps
if "%1"=="--show-code" goto show_code
if "%1"=="--disable-security" goto disable_security
if "%1"=="--debug" goto debug_mode
if "%1"=="--help" goto show_help
if "%1"=="" goto run_main

REM Default: run main application
:run_main
echo.
echo Starting GlobalExam AI...
%PYTHON_EXE% main_application.py %*
goto end

:setup
echo.
echo Setting up GlobalExam AI security...
%PYTHON_EXE% main_application.py --setup-security
goto end

:install_deps
echo.
echo Installing Python dependencies...
%PYTHON_EXE% -m pip install --upgrade pip
%PYTHON_EXE% -m pip install pyautogui Pillow opencv-python numpy pytesseract requests psutil
echo Dependencies installed!
goto end

:show_code
echo.
echo Showing today's daily code...
%PYTHON_EXE% main_application.py --show-daily-code
goto end

:disable_security
echo.
echo Disabling security system...
%PYTHON_EXE% main_application.py --disable-security
goto end

:debug_mode
echo.
echo Starting GlobalExam AI in DEBUG mode...
%PYTHON_EXE% main_application.py --debug %2 %3 %4 %5
goto end

:show_help
echo.
echo   run_with_python313.bat           - Run main application
echo   run_with_python313.bat --setup   - Setup security system
echo   run_with_python313.bat --daily-code - Show today's code
echo   run_with_python313.bat --machine-id - Show machine ID
echo   run_with_python313.bat --disable-security - Disable security
echo   run_with_python313.bat --debug   - Run with debug mode
echo   run_with_python313.bat --help    - Show this help
echo.
goto end

:end
echo.
echo Press any key to exit...
pause >nul
