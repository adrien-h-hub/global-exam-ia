#!/usr/bin/env python3
"""
Système de Sécurité v4 pour GlobalExam AI - Contrôle Serveur
===========================================================

Ce système vous donne un contrôle total sur qui peut utiliser l'application :

1. AUCUN CODE VISIBLE dans l'application
2. Authentification par serveur distant (vous contrôlez)
3. Vous pouvez activer/désactiver des utilisateurs à distance
4. Sessions temporaires avec expiration
5. Logs de qui utilise l'application et quand

Fonctionnement :
- L'utilisateur entre son nom/email
- L'app contacte votre serveur pour vérification
- Vous approuvez ou refusez depuis votre panneau de contrôle
- Aucun code n'est affiché à l'utilisateur

Auteur : Projet Étudiant
Objectif : Contrôle total de l'accès à l'application
"""

import hashlib
import json
import os
import time
import uuid
import getpass
import platform
import requests
import threading
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog

class ServerControlledSecurity:
    """
    Système de sécurité contrôlé par serveur
    
    Vous gardez le contrôle total :
    - Approuvez/refusez les utilisateurs depuis votre serveur
    - Aucun code visible dans l'application
    - Logs de toutes les utilisations
    - Révocation instantanée d'accès
    """
    
    def __init__(self, app_name: str = "GlobalExamAI"):
        """
        Initialise le système de sécurité contrôlé par serveur
        
        Args:
            app_name: Nom de l'application
        """
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.session_file = os.path.join(self.config_dir, 'session.dat')
        
        # Configuration serveur global
        self.server_config = {
            'auth_url': 'https://globalia.herokuapp.com/api/auth',  # Votre serveur global
            'check_url': 'https://globalia.herokuapp.com/api/check',  # Votre serveur global
            'log_url': 'https://globalia.herokuapp.com/api/log',     # Votre serveur global
            'local_server': 'http://localhost:8080',  # Serveur local pour tests
            'fallback_mode': False  # Mode hors ligne DÉSACTIVÉ
        }
        
        # Informations système (pour identification)
        self.system_info = {
            'username': getpass.getuser(),
            'computer_name': platform.node(),
            'system': platform.system(),
            'app_version': '4.0',
            'timestamp': datetime.now().isoformat()
        }
        
        # S'assurer que le répertoire existe
        os.makedirs(self.config_dir, exist_ok=True)
        
        print(f"[SÉCURITÉ] Système de contrôle serveur initialisé")
        print(f"[SÉCURITÉ] Utilisateur : {self.system_info['username']}")
        print(f"[SÉCURITÉ] Ordinateur : {self.system_info['computer_name']}")
    
    def _get_config_directory(self) -> str:
        """Obtenir le répertoire de configuration"""
        if os.name == 'nt':  # Windows
            base_dir = os.getenv('APPDATA', os.path.expanduser('~'))
        else:  # Linux/Mac
            base_dir = os.path.expanduser('~/.config')
        
        return os.path.join(base_dir, self.app_name)
    
    def request_access(self) -> bool:
        """
        Demande l'accès au serveur (AUCUN CODE VISIBLE)
        
        Returns:
            True si l'accès est accordé
        """
        print("\n" + "="*60)
        print("GLOBALEXAM AI - DEMANDE D'ACCÈS")
        print("="*60)
        print("Cette application nécessite une autorisation.")
        print("Aucun code ne sera affiché - tout est contrôlé par le propriétaire.")
        print("="*60)
        
        try:
            # Demander les informations utilisateur
            user_info = self._get_user_info()
            if not user_info:
                return False
            
            # Tenter l'authentification serveur
            if self._try_server_auth(user_info):
                return True
            
            # Pas de mode fallback - serveur requis
            print("[SÉCURITÉ] ✗ Serveur requis pour l'authentification")
            print("[SÉCURITÉ] Contactez le propriétaire pour l'accès")
            
            return False
            
        except Exception as e:
            print(f"[ERREUR] Demande d'accès échouée : {e}")
            return False
    
    def _get_user_info(self) -> Optional[Dict[str, str]]:
        """
        Obtenir les informations utilisateur (interface graphique)
        
        Returns:
            Dictionnaire avec les infos utilisateur ou None
        """
        try:
            # Créer une fenêtre simple pour saisie
            root = tk.Tk()
            root.withdraw()  # Cacher la fenêtre principale
            
            # Demander le nom/email
            user_id = simpledialog.askstring(
                "GlobalExam AI - Identification",
                "Entrez votre nom ou email :\n\n(Le propriétaire recevra une demande d'autorisation)",
                parent=root
            )
            
            if not user_id or not user_id.strip():
                root.destroy()
                return None
            
            # Demander une raison (optionnel)
            reason = simpledialog.askstring(
                "GlobalExam AI - Raison",
                "Raison d'utilisation (optionnel) :",
                parent=root
            ) or "Non spécifiée"
            
            root.destroy()
            
            return {
                'user_id': user_id.strip(),
                'reason': reason.strip(),
                'request_time': datetime.now().isoformat(),
                'system_info': self.system_info
            }
            
        except Exception as e:
            print(f"[ERREUR] Saisie utilisateur échouée : {e}")
            return None
    
    def _try_server_auth(self, user_info: Dict[str, str]) -> bool:
        """
        Tenter l'authentification via serveur
        
        Args:
            user_info: Informations utilisateur
            
        Returns:
            True si authentifié par le serveur
        """
        print("[SERVEUR] Connexion au serveur d'authentification...")
        
        # Liste des serveurs à essayer
        servers_to_try = [
            self.server_config['local_server'] + '/api/auth',  # Serveur local d'abord
            self.server_config['auth_url']  # Puis serveur global
        ]
        
        for server_url in servers_to_try:
            try:
                print(f"[SERVEUR] Tentative : {server_url}")
                
                # Préparer la requête
                auth_data = {
                    'app_name': self.app_name,
                    'user_info': user_info,
                    'request_type': 'access_request'
                }
                
                # Envoyer la requête (timeout court)
                response = requests.post(
                    server_url,
                    json=auth_data,
                    timeout=5,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('access_granted'):
                        # Sauvegarder la session
                        session_data = {
                            'user_id': user_info['user_id'],
                            'session_token': result.get('session_token'),
                            'expires_at': result.get('expires_at'),
                            'granted_at': datetime.now().isoformat()
                        }
                        
                        self._save_session(session_data)
                        
                        print(f"[SERVEUR] ✓ Accès accordé par {server_url}")
                        return True
                    else:
                        reason = result.get('reason', 'Accès refusé')
                        print(f"[SERVEUR] ✗ Accès refusé par {server_url} : {reason}")
                        continue  # Essayer le serveur suivant
                else:
                    print(f"[SERVEUR] ✗ Erreur serveur {server_url} : {response.status_code}")
                    continue  # Essayer le serveur suivant
                    
            except requests.exceptions.Timeout:
                print(f"[SERVEUR] ⏱️ Timeout - {server_url} non disponible")
                continue  # Essayer le serveur suivant
            except requests.exceptions.ConnectionError:
                print(f"[SERVEUR] 🔌 Impossible de se connecter à {server_url}")
                continue  # Essayer le serveur suivant
            except Exception as e:
                print(f"[SERVEUR] ❌ Erreur avec {server_url} : {e}")
                continue  # Essayer le serveur suivant
        
        # Aucun serveur n'a fonctionné
        print("[SERVEUR] ✗ Aucun serveur disponible")
        return False
    
    
    def _save_session(self, session_data: Dict[str, Any]) -> bool:
        """
        Sauvegarder la session de manière sécurisée
        
        Args:
            session_data: Données de session
            
        Returns:
            True si sauvegardé avec succès
        """
        try:
            # Chiffrer les données de session
            session_json = json.dumps(session_data, indent=2)
            
            # Simple obfuscation (vous pouvez améliorer)
            key = hashlib.sha256(f"{self.app_name}{getpass.getuser()}".encode()).digest()
            encrypted_data = bytearray()
            
            for i, byte in enumerate(session_json.encode('utf-8')):
                encrypted_data.append(byte ^ key[i % len(key)])
            
            # Sauvegarder
            with open(self.session_file, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"[SESSION] Session sauvegardée")
            return True
            
        except Exception as e:
            print(f"[SESSION] Sauvegarde échouée : {e}")
            return False
    
    def _load_session(self) -> Optional[Dict[str, Any]]:
        """
        Charger la session existante
        
        Returns:
            Données de session si valides, None sinon
        """
        try:
            if not os.path.exists(self.session_file):
                return None
            
            # Charger et déchiffrer
            with open(self.session_file, 'rb') as f:
                encrypted_data = f.read()
            
            key = hashlib.sha256(f"{self.app_name}{getpass.getuser()}".encode()).digest()
            decrypted_data = bytearray()
            
            for i, byte in enumerate(encrypted_data):
                decrypted_data.append(byte ^ key[i % len(key)])
            
            # Parser JSON
            session_json = decrypted_data.decode('utf-8')
            session_data = json.loads(session_json)
            
            return session_data
            
        except Exception as e:
            print(f"[SESSION] Chargement échoué : {e}")
            return None
    
    def _is_session_valid(self, session: Dict[str, Any]) -> bool:
        """
        Vérifier si la session est encore valide
        
        Args:
            session: Données de session
            
        Returns:
            True si la session est valide
        """
        try:
            expires_at = datetime.fromisoformat(session['expires_at'])
            return datetime.now() < expires_at
        except:
            return False
    
    
    def check_authorization(self) -> bool:
        """
        Vérifier l'autorisation d'utilisation
        
        Il s'agit de la fonction principale appelée par l'application
        
        Returns:
            True si autorisé à utiliser l'application
        """
        try:
            print("\n[AUTORISATION] Vérification de l'accès...")
            
            # Vérifier session existante
            session = self._load_session()
            if session and self._is_session_valid(session):
                print(f"[AUTORISATION] ✓ Session valide pour {session['user_id']}")
                
                # Vérifier avec le serveur (requis)
                if self._verify_with_server(session):
                    return True
                else:
                    print("[AUTORISATION] ✗ Impossible de vérifier avec le serveur")
                    print("[AUTORISATION] Session locale expirée - nouvelle demande requise")
                    
                    # Supprimer la session invalide
                    self.revoke_session()
                    return False
            
            # Pas de session valide - demander l'accès
            print("[AUTORISATION] Aucune session valide - demande d'accès requise")
            return self.request_access()
            
        except Exception as e:
            print(f"[AUTORISATION] Vérification échouée : {e}")
            return False
    
    def _verify_with_server(self, session: Dict[str, Any]) -> bool:
        """
        Vérifier la session avec le serveur
        
        Args:
            session: Données de session
            
        Returns:
            True si la session est confirmée par le serveur
        """
        try:
            check_data = {
                'session_token': session['session_token'],
                'user_id': session['user_id'],
                'app_name': self.app_name
            }
            
            response = requests.post(
                self.server_config['check_url'],
                json=check_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('session_valid', False)
            
        except:
            pass  # Échec silencieux - utiliser session locale
        
        return False
    
    def revoke_session(self) -> bool:
        """
        Révoquer la session actuelle
        
        Returns:
            True si révoqué avec succès
        """
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                print("[SESSION] Session révoquée")
                return True
            return True
        except Exception as e:
            print(f"[SESSION] Révocation échouée : {e}")
            return False
    
    def get_session_info(self) -> Optional[Dict[str, Any]]:
        """
        Obtenir les informations de session actuelle
        
        Returns:
            Informations de session ou None
        """
        session = self._load_session()
        if session and self._is_session_valid(session):
            return {
                'user_id': session.get('user_id'),
                'granted_at': session.get('granted_at'),
                'expires_at': session.get('expires_at'),
                'mode': session.get('mode', 'online')
            }
        return None

# Exemple d'utilisation et test
if __name__ == "__main__":
    print("Module Système de Sécurité v4 - Mode Test")
    print("="*50)
    
    # Créer le gestionnaire de sécurité
    security = ServerControlledSecurity("TestApp")
    
    # Test d'autorisation
    authorized = security.check_authorization()
    
    if authorized:
        print("\n✅ ACCÈS AUTORISÉ")
        session_info = security.get_session_info()
        if session_info:
            print(f"Utilisateur : {session_info['user_id']}")
            print(f"Mode : {session_info['mode']}")
            print(f"Expire : {session_info['expires_at']}")
    else:
        print("\n❌ ACCÈS REFUSÉ")
    
    print("\nTest du système de sécurité terminé !")
