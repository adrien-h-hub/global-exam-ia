#!/usr/bin/env python3
"""
GlobalExam AI - Auto Setup & Launcher
=====================================
Automatically installs dependencies and launches the application
"""

import sys
import subprocess
import os
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou supérieur requis")
        print(f"Version actuelle : {sys.version}")
        print("Téléchargez Python depuis https://python.org")
        return False
    return True

def is_package_installed(package_name):
    """Check if a package is installed"""
    try:
        if package_name == "cv2":
            package_name = "opencv-python"
        
        spec = importlib.util.find_spec(package_name.replace("-", "_"))
        return spec is not None
    except ImportError:
        return False

def install_package(package):
    """Install a single package"""
    try:
        print(f"📦 Installation de {package}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package, "--user"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package} installé avec succès")
            return True
        else:
            print(f"❌ Erreur installation {package}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout installation {package}")
        return False
    except Exception as e:
        print(f"❌ Erreur installation {package}: {e}")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("🔧 INSTALLATION AUTOMATIQUE DES DÉPENDANCES")
    print("=" * 60)
    
    # Essential packages for the application
    essential_packages = [
        "requests>=2.31.0",
        "Pillow>=10.0.0",
        "pyautogui>=0.9.54",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "pytesseract>=0.3.10",
        "psutil>=5.9.0"
    ]
    
    # Windows-specific packages
    windows_packages = [
        "pywin32>=306",
        "comtypes>=1.2.0",
        "pynput>=1.7.6",
        "keyboard>=0.13.5",
        "mouse>=0.7.1",
        "screeninfo>=0.8.1",
        "pygetwindow>=0.0.9"
    ]
    
    # Check which packages need installation
    packages_to_install = []
    
    print("🔍 Vérification des dépendances...")
    
    for package in essential_packages:
        package_name = package.split(">=")[0].split("==")[0]
        if not is_package_installed(package_name):
            packages_to_install.append(package)
    
    # Add Windows packages if on Windows
    if sys.platform == "win32":
        for package in windows_packages:
            package_name = package.split(">=")[0].split("==")[0]
            if not is_package_installed(package_name):
                packages_to_install.append(package)
    
    if not packages_to_install:
        print("✅ Toutes les dépendances sont déjà installées!")
        return True
    
    print(f"📋 {len(packages_to_install)} packages à installer...")
    print()
    
    # Install packages
    failed_packages = []
    for package in packages_to_install:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ {len(failed_packages)} packages ont échoué:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\n💡 L'application peut fonctionner avec des fonctionnalités limitées")
        return False
    
    print(f"\n🎉 Installation terminée! {len(packages_to_install)} packages installés")
    return True

def install_tesseract():
    """Install Tesseract OCR if not present"""
    try:
        # Try to import pytesseract to check if Tesseract is available
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR déjà installé")
        return True
    except:
        print("📥 Installation de Tesseract OCR...")
        try:
            # Try to use the OCR analyzer's auto-install
            from ocr_ai_analysis import OCRAnalyzer
            analyzer = OCRAnalyzer()
            if analyzer.install_tesseract():
                print("✅ Tesseract OCR installé avec succès")
                return True
        except Exception as e:
            print(f"⚠️ Installation automatique de Tesseract échouée: {e}")
            print("💡 Vous pouvez l'installer manuellement depuis https://github.com/tesseract-ocr/tesseract")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut"""
    try:
        if sys.platform == "win32":
            from create_shortcuts import create_shortcuts
            create_shortcuts()
            print("✅ Raccourci bureau créé")
    except Exception as e:
        print(f"⚠️ Création raccourci échouée: {e}")

def show_welcome():
    """Show welcome message with logo"""
    try:
        logo_path = Path(__file__).parent / "assets" / "logo.txt"
        if logo_path.exists():
            with open(logo_path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("🚀 GLOBALEXAM AI - INSTALLATION AUTOMATIQUE 🚀")
            print("=" * 60)
    except:
        print("🚀 GLOBALEXAM AI - INSTALLATION AUTOMATIQUE 🚀")
        print("=" * 60)

def main():
    """Main auto-setup function"""
    show_welcome()
    
    print("🔍 Vérification du système...")
    
    # Check Python version
    if not check_python_version():
        input("Appuyez sur Entrée pour quitter...")
        return
    
    print(f"✅ Python {sys.version.split()[0]} détecté")
    print()
    
    # Install dependencies
    print("🚀 Démarrage de l'installation automatique...")
    success = install_dependencies()
    
    print()
    
    # Install Tesseract
    install_tesseract()
    
    print()
    
    # Create shortcuts
    create_desktop_shortcut()
    
    print()
    print("=" * 60)
    
    if success:
        print("🎉 INSTALLATION TERMINÉE AVEC SUCCÈS!")
        print()
        print("🚀 Lancement de GlobalExam AI...")
        print("=" * 60)
        
        # Launch the main application
        try:
            from run_app import main as run_main
            run_main()
        except ImportError:
            try:
                from launch_secure_app import main as launch_main
                launch_main()
            except ImportError:
                print("❌ Impossible de lancer l'application")
                print("Vérifiez que tous les fichiers sont présents")
    else:
        print("⚠️ INSTALLATION PARTIELLE")
        print("Certaines fonctionnalités peuvent être limitées")
        print()
        
        response = input("Voulez-vous lancer l'application quand même? (o/n): ").lower()
        if response in ['o', 'oui', 'y', 'yes']:
            try:
                from run_app import main as run_main
                run_main()
            except ImportError:
                try:
                    from launch_secure_app import main as launch_main
                    launch_main()
                except ImportError:
                    print("❌ Impossible de lancer l'application")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Installation annulée")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        input("Appuyez sur Entrée pour quitter...")
