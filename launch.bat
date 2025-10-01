@echo off
title GlobalExam AI - Launcher
color 0A

echo.
echo  ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     ███████╗██╗  ██╗ █████╗ ███╗   ███╗
echo ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║
echo ██║  ███╗██║     ██║   ██║██████╔╝███████║██║     █████╗   ╚███╔╝ ███████║██╔████╔██║
echo ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║
echo ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║
echo  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
echo.
echo                           █████╗ ██╗    ██╗   ██╗██╗  ██╗                           
echo                          ██╔══██╗██║    ██║   ██║██║  ██║                           
echo                          ███████║██║    ██║   ██║███████║                           
echo                          ██╔══██║██║    ╚██╗ ██╔╝╚════██║                           
echo                          ██║  ██║██║     ╚████╔╝      ██║                           
echo                          ╚═╝  ╚═╝╚═╝      ╚═══╝       ╚═╝                           
echo.
echo                    🤖 SYSTÈME D'AUTOMATISATION INTELLIGENT 🤖                       
echo                    🔒 SÉCURITÉ AVANCÉE • 🎯 CLICS ADAPTATIFS 🎯                     
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo 📥 Téléchargez Python depuis https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
echo 🚀 Lancement de GlobalExam AI...
echo.

REM Lancer l'application Python
python launch_secure_app.py

REM Pause pour voir les messages d'erreur éventuels
if errorlevel 1 (
    echo.
    echo ❌ Une erreur s'est produite
    pause
)
