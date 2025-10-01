#!/usr/bin/env python3
"""
Lanceur Sécurisé pour GlobalExam AI
===================================

Ce lanceur utilise le nouveau système de sécurité v4 qui vous donne
un contrôle total sur qui peut utiliser l'application.

Fonctionnalités :
- AUCUN CODE visible à l'utilisateur
- Contrôle serveur (vous approuvez/refusez)
- Logs de toutes les utilisations
- Révocation d'accès à distance
- Pas de mode hors ligne (sécurité renforcée)

Auteur : Projet Étudiant
"""

import sys
import os
from pathlib import Path

# Ajouter les chemins nécessaires
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def show_welcome():
    """Afficher le message d'accueil avec logo"""
    try:
        # Essayer d'afficher le logo ASCII
        logo_path = Path(__file__).parent / "assets" / "logo.txt"
        if logo_path.exists():
            with open(logo_path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            # Fallback si pas de logo
            print("="*80)
            print("🚀 GLOBALEXAM AI - SYSTÈME SÉCURISÉ v4 🚀")
            print("="*80)
    except:
        # Fallback en cas d'erreur
        print("="*60)
        print("GLOBALEXAM AI - SYSTÈME SÉCURISÉ v4")
        print("="*60)
    
    print()
    print("🔒 Sécurité : Contrôle serveur (aucun code visible)")
    print("🤖 Intelligence : OCR + Analyse IA")
    print("🎯 Automatisation : Clics adaptatifs")
    print("🛡️ Fiabilité : Systèmes de secours multiples")
    print("="*80)
    print()

def launch_control_panel():
    """Lancer le panneau de contrôle avec protection par code"""
    
    # Demander le code d'accès
    print("🔐 ACCÈS PANNEAU DE CONTRÔLE")
    print("="*40)
    print("Ce panneau est réservé au propriétaire de l'application.")
    
    try:
        access_code = input("Entrez le code d'accès : ").strip()
        
        # Vérifier le code (configuré par le propriétaire)
        OWNER_ACCESS_CODE = "YOUR_SECRET_CODE_HERE"  # À changer par le propriétaire
        
        if access_code != OWNER_ACCESS_CODE:
            print("❌ Code d'accès incorrect !")
            print("Accès refusé au panneau de contrôle.")
            return False
        
        print("✅ Code correct - Accès autorisé")
        print()
        
    except KeyboardInterrupt:
        print("\n❌ Accès annulé")
        return False
    
    # Lancer le panneau de contrôle
    try:
        from control_panel import ControlPanel
        
        print("🎛️ Lancement du panneau de contrôle...")
        print("Vous pouvez maintenant :")
        print("• Approuver/refuser des utilisateurs")
        print("• Voir les logs d'utilisation")
        print("• Révoquer l'accès à distance")
        print("• Démarrer un serveur local pour tests")
        print()
        
        app = ControlPanel()
        app.run()
        
    except ImportError as e:
        print(f"❌ Erreur d'import du panneau de contrôle : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur du panneau de contrôle : {e}")
        return False

def launch_main_app():
    """Lancer l'application principale"""
    try:
        from main_application import GlobalExamAI
        
        print("🚀 Lancement de l'application principale...")
        print("L'application va maintenant demander l'autorisation...")
        print()
        
        # Créer et lancer l'application
        app = GlobalExamAI("GlobalExamAI")
        result = app.run_automation()
        
        # Afficher les résultats
        if 'error' in result:
            print(f"\n❌ Erreur : {result['error']}")
        else:
            print(f"\n✅ Automation terminée avec succès")
            print(f"Questions tentées : {result.get('questions_attempted', 0)}")
            print(f"Questions réussies : {result.get('questions_successful', 0)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import de l'application : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur de l'application : {e}")
        return False

def test_security_system():
    """Tester le système de sécurité"""
    try:
        from security_system_v4 import ServerControlledSecurity
        
        print("🧪 Test du système de sécurité...")
        
        security = ServerControlledSecurity("TestApp")
        authorized = security.check_authorization()
        
        if authorized:
            print("✅ Test de sécurité réussi - accès autorisé")
            session_info = security.get_session_info()
            if session_info:
                print(f"Utilisateur : {session_info['user_id']}")
                print(f"Mode : {session_info.get('mode', 'online')}")
        else:
            print("❌ Test de sécurité - accès refusé")
        
        return authorized
        
    except Exception as e:
        print(f"❌ Erreur du test de sécurité : {e}")
        return False

def test_adaptive_clicking():
    """Tester le système de clics adaptatifs"""
    try:
        # Import depuis le répertoire parent
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from test_adaptive_system import main as test_main
        
        print("🎯 Lancement du test de clics adaptatifs...")
        test_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'import du test adaptatif : {e}")
    except Exception as e:
        print(f"❌ Erreur du test adaptatif : {e}")

def main():
    """Menu principal"""
    show_welcome()
    
    while True:
        print("OPTIONS DISPONIBLES :")
        print("1. 🚀 Lancer l'application principale")
        print("2. 🎛️ Ouvrir le panneau de contrôle (propriétaire)")
        print("3. 🧪 Tester le système de sécurité")
        print("4. 🎯 Tester les clics adaptatifs")
        print("5. ❓ Aide et informations")
        print("6. 🚪 Quitter")
        
        try:
            choice = input("\nSélectionnez une option (1-6) : ").strip()
            
            if choice == '1':
                print("\n" + "="*50)
                launch_main_app()
                
            elif choice == '2':
                print("\n" + "="*50)
                launch_control_panel()
                
            elif choice == '3':
                print("\n" + "="*50)
                test_security_system()
                
            elif choice == '4':
                print("\n" + "="*50)
                test_adaptive_clicking()
                
            elif choice == '5':
                show_help()
                
            elif choice == '6':
                print("\n👋 Au revoir !")
                break
                
            else:
                print("❌ Choix invalide. Veuillez sélectionner 1-6.")
            
            print("\n" + "="*50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")

def show_help():
    """Afficher l'aide"""
    print("\n" + "="*60)
    print("AIDE - GLOBALEXAM AI v4")
    print("="*60)
    
    print("\n🔒 SYSTÈME DE SÉCURITÉ :")
    print("• Aucun code visible à l'utilisateur")
    print("• Vous contrôlez qui peut utiliser l'app")
    print("• Approbation/refus depuis le panneau de contrôle")
    print("• Logs de toutes les utilisations")
    print("• Révocation d'accès instantanée")
    print("• Pas de mode hors ligne (sécurité renforcée)")
    
    print("\n🎯 SYSTÈME DE CLICS ADAPTATIFS :")
    print("• Détecte automatiquement le type de question")
    print("• S'adapte aux positions dynamiques des réponses")
    print("• Fonctionne avec tous les types de questions :")
    print("  - Vrai/Faux (positions fixes)")
    print("  - Choix multiples (positions fixes)")
    print("  - Remake phrase (positions dynamiques)")
    print("  - Remplir blancs (champs dynamiques)")
    
    print("\n🎛️ PANNEAU DE CONTRÔLE :")
    print("• Voir les demandes d'accès en temps réel")
    print("• Approuver/refuser des utilisateurs")
    print("• Étendre ou révoquer des sessions")
    print("• Consulter les logs d'utilisation")
    print("• Serveur local pour tests")
    print("• Protégé par code d'accès propriétaire")
    
    print("\n📞 UTILISATION :")
    print("1. Configurez votre code d'accès dans le script")
    print("2. Démarrez le panneau de contrôle (option 2)")
    print("3. L'utilisateur lance l'app (option 1)")
    print("4. Vous recevez une demande d'accès")
    print("5. Vous approuvez ou refusez")
    print("6. L'utilisateur peut utiliser l'app si approuvé")
    
    print("\n🔧 CONFIGURATION :")
    print("• Changez YOUR_SECRET_CODE_HERE par votre code")
    print("• Configurez les URLs de serveur si nécessaire")
    print("• Ajustez les coordonnées de clic si besoin")
    
    print("\n🔧 DÉPANNAGE :")
    print("• Si les clics ne fonctionnent pas : testez option 4")
    print("• Si la sécurité ne fonctionne pas : testez option 3")
    print("• Vérifiez que tous les modules sont installés")
    print("• Consultez les logs dans le panneau de contrôle")

if __name__ == "__main__":
    main()
