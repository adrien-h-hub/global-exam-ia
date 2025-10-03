@echo off
title GlobalExam AI - Installation Automatique
color 0A

echo.
echo  ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     ███████╗██╗  ██╗ █████╗ ███╗   ███╗
echo ██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║
echo ██║  ███╗██║     ██║   ██║██████╔╝███████║██║     █████╗   ╚███╔╝ ███████║██╔████╔██║
echo ██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║
echo ╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║
echo  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
echo.
echo                    🤖 INSTALLATION AUTOMATIQUE 🤖                       
echo                    🔧 TOUTES LES DÉPENDANCES INCLUSES 🔧                     
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo.
    echo 📥 INSTALLATION DE PYTHON REQUISE:
    echo 1. Allez sur https://python.org
    echo 2. Téléchargez Python 3.8 ou supérieur
    echo 3. IMPORTANT: Cochez "Add Python to PATH" pendant l'installation
    echo 4. Relancez ce fichier après installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
echo 🚀 Lancement de l'installation automatique...
echo.

REM Lancer l'installation automatique
python auto_setup.py

REM Pause pour voir les messages d'erreur éventuels
if errorlevel 1 (
    echo.
    echo ❌ Une erreur s'est produite pendant l'installation
    echo 💡 Essayez de relancer en tant qu'administrateur
    pause
)
