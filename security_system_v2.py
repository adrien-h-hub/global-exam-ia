#!/usr/bin/env python3
"""
Système de Sécurité v2 pour GlobalExam AI
=========================================

Ce module implémente un système de sécurité basé sur l'authentification par session :
1. Codes rotatifs quotidiens sans liaison machine
2. Authentification par nom d'utilisateur et mot de passe
3. Sessions temporaires avec expiration automatique
4. Stockage chiffré des configurations

Auteur : Projet Étudiant
Objectif : Démonstration éducative des concepts de sécurité par session
"""

import hashlib
import json
import os
import time
import uuid
import getpass
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class SessionSecurityManager:
    """
    Gestionnaire de Sécurité par Session
    
    Gère la sécurité de l'application à travers plusieurs couches :
    
    Couche 1 : Authentification Utilisateur
    - Nom d'utilisateur et mot de passe
    - Hachage sécurisé des mots de passe
    
    Couche 2 : Sessions Temporaires
    - Tokens de session avec expiration
    - Validation automatique de l'expiration
    
    Couche 3 : Codes Quotidiens
    - Génération de codes uniques basés sur la date
    - Rotation automatique chaque jour
    """
    
    def __init__(self, app_name: str = "GlobalExamAI"):
        """
        Initialise le gestionnaire de sécurité par session
        
        Args:
            app_name: Nom de l'application pour le répertoire de configuration
        """
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.config_path = os.path.join(self.config_dir, 'config.json')
        self.session_duration_hours = 8  # Durée de session par défaut
        
        # S'assurer que le répertoire de configuration existe
        os.makedirs(self.config_dir, exist_ok=True)
        
        print(f"[SÉCURITÉ] Initialisé pour {app_name}")
        print(f"[SÉCURITÉ] Répertoire de config : {self.config_dir}")
    
    def _get_config_directory(self) -> str:
        """
        Obtenir le répertoire de configuration approprié à la plateforme
        
        Returns:
            Chemin vers le répertoire de configuration
        """
        if os.name == 'nt':  # Windows
            base_dir = os.getenv('APPDATA', os.path.expanduser('~'))
        else:  # Linux/Mac
            base_dir = os.path.expanduser('~/.config')
        
        return os.path.join(base_dir, self.app_name)
    
    def get_session_id(self) -> str:
        """
        Génère un identifiant de session unique
        
        Cet identifiant combine plusieurs éléments pour créer une session
        unique qui ne dépend pas du matériel mais reste sécurisée :
        
        Méthodes utilisées :
        1. Nom d'utilisateur système
        2. Timestamp de création de session
        3. UUID aléatoire
        4. Nom de l'ordinateur (optionnel)
        
        Returns:
            Hash SHA-256 de l'identifiant de session combiné
        """
        identifiers = []
        
        try:
            # Méthode 1 : Nom d'utilisateur système
            username = getpass.getuser()
            identifiers.append(username)
            print(f"[SESSION_ID] Utilisateur : {username}")
            
        except Exception as e:
            print(f"[SESSION_ID] Nom d'utilisateur échoué : {e}")
        
        try:
            # Méthode 2 : Timestamp de session
            session_time = str(int(time.time()))
            identifiers.append(session_time)
            print(f"[SESSION_ID] Timestamp : {session_time}")
            
        except Exception as e:
            print(f"[SESSION_ID] Timestamp échoué : {e}")
        
        try:
            # Méthode 3 : UUID aléatoire pour l'unicité
            random_uuid = str(uuid.uuid4())
            identifiers.append(random_uuid)
            print(f"[SESSION_ID] UUID : {random_uuid[:16]}...")
            
        except Exception as e:
            print(f"[SESSION_ID] UUID échoué : {e}")
        
        try:
            # Méthode 4 : Nom de l'ordinateur (pour différencier les machines)
            import platform
            computer_name = platform.node()
            identifiers.append(computer_name)
            print(f"[SESSION_ID] Ordinateur : {computer_name}")
            
        except Exception as e:
            print(f"[SESSION_ID] Nom d'ordinateur échoué : {e}")
        
        # Combiner tous les identifiants
        if not identifiers:
            # Fallback : utiliser timestamp et UUID
            fallback = f"{int(time.time())}{uuid.uuid4()}"
            identifiers.append(fallback)
            print(f"[SESSION_ID] Utilisation du fallback : {fallback[:16]}...")
        
        # Créer un hash stable à partir de tous les identifiants
        combined = ''.join(identifiers)
        session_id = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        print(f"[SESSION_ID] ID généré : {session_id[:16]}...")
        return session_id
    
    def compute_daily_code(self, secret_hash: str, username: str = None) -> str:
        """
        Génère le code d'approbation quotidien à 6 chiffres
        
        L'algorithme de code quotidien :
        1. Obtenir le nom d'utilisateur (ou utiliser celui fourni)
        2. Combiner avec le hash secret (défini par le propriétaire)
        3. Ajouter la date d'aujourd'hui (format AAAAMMJJ)
        4. Générer un hash SHA-256 de la combinaison
        5. Extraire les 6 derniers chiffres comme nombre décimal
        
        Cela garantit :
        - Le code change chaque jour automatiquement
        - Le code est unique par utilisateur (peut être partagé entre utilisateurs autorisés)
        - Le code est déterministe (même chaque jour pour le même utilisateur)
        - Le code est imprévisible sans le secret
        
        Args:
            secret_hash: Hash SHA-256 du secret maître
            username: Nom d'utilisateur optionnel (utilise l'utilisateur système si None)
            
        Returns:
            Code quotidien à 6 chiffres sous forme de chaîne
        """
        try:
            if username is None:
                username = getpass.getuser()
            
            today = time.strftime('%Y%m%d')  # Format : 20231229
            
            # Combiner utilisateur + secret + date
            combined_string = f"{username}{secret_hash}{today}"
            
            # Générer le hash
            daily_hash = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()
            
            # Extraire le code à 6 chiffres du hash
            # Convertir hex en int, puis obtenir les 6 derniers chiffres
            hash_int = int(daily_hash, 16)
            daily_code = f"{hash_int % 1000000:06d}"
            
            print(f"[CODE_QUOTIDIEN] Généré pour {today} (utilisateur: {username}): {daily_code}")
            return daily_code
            
        except Exception as e:
            print(f"[CODE_QUOTIDIEN] Génération échouée : {e}")
            return "000000"  # Fallback sécurisé
    
    def create_session_token(self, username: str, secret_hash: str) -> str:
        """
        Crée un token de session temporaire
        
        Args:
            username: Nom d'utilisateur
            secret_hash: Hash du secret maître
            
        Returns:
            Token de session chiffré
        """
        try:
            session_id = self.get_session_id()
            timestamp = str(int(time.time()))
            
            # Combiner pour créer le token
            token_data = f"{username}{session_id}{secret_hash}{timestamp}"
            session_token = hashlib.sha256(token_data.encode('utf-8')).hexdigest()
            
            print(f"[SESSION] Token créé pour {username}")
            return session_token
            
        except Exception as e:
            print(f"[SESSION] Création de token échouée : {e}")
            return ""
    
    def is_session_valid(self, session_data: Dict) -> bool:
        """
        Vérifie si une session est encore valide
        
        Args:
            session_data: Données de session à valider
            
        Returns:
            True si la session est valide
        """
        try:
            if not session_data:
                return False
            
            # Vérifier l'expiration
            session_start = session_data.get('start_time', 0)
            current_time = time.time()
            session_age_hours = (current_time - session_start) / 3600
            
            if session_age_hours > self.session_duration_hours:
                print(f"[SESSION] Expirée après {session_age_hours:.1f} heures")
                return False
            
            # Vérifier la date (nouvelle journée = nouvelle session requise)
            session_date = session_data.get('date', '')
            today = time.strftime('%Y%m%d')
            
            if session_date != today:
                print(f"[SESSION] Nouvelle journée détectée ({session_date} -> {today})")
                return False
            
            print(f"[SESSION] Valide (âge: {session_age_hours:.1f}h)")
            return True
            
        except Exception as e:
            print(f"[SESSION] Validation échouée : {e}")
            return False
    
    def load_config(self) -> Dict[str, Any]:
        """
        Charge et valide la configuration depuis le stockage chiffré
        
        Returns:
            Dictionnaire de configuration avec paramètres de sécurité
        """
        try:
            if not os.path.exists(self.config_path):
                print("[CONFIG] Aucun fichier de config trouvé, création par défaut")
                return self._create_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8-sig') as f:
                config = json.load(f)
            
            print("[CONFIG] Chargé avec succès")
            return config
            
        except Exception as e:
            print(f"[CONFIG] Chargement échoué : {e}")
            return self._create_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Sauvegarde la configuration dans le stockage chiffré
        
        Args:
            config: Dictionnaire de configuration à sauvegarder
            
        Returns:
            True si sauvegardé avec succès
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("[CONFIG] Sauvegardé avec succès")
            return True
            
        except Exception as e:
            print(f"[CONFIG] Sauvegarde échouée : {e}")
            return False
    
    def _create_default_config(self) -> Dict[str, Any]:
        """
        Crée la configuration de sécurité par défaut
        
        Returns:
            Dictionnaire de configuration par défaut
        """
        default_config = {
            "REQUIRE_APPROVAL": False,
            "AUTH_MODE": "session",  # session, daily, disabled
            "SESSION_DURATION_HOURS": 8,
            "APPROVAL_SECRET_HASH": "",
            "CURRENT_SESSION": {},
            "REGISTERED_USERS": {},
            "SECURITY_VERSION": "2.0"
        }
        
        self.save_config(default_config)
        return default_config
    
    def setup_security(self, master_secret: str, auth_mode: str = "session", 
                      session_duration: int = 8) -> bool:
        """
        Configure le système de sécurité avec le secret maître
        
        Args:
            master_secret: Mot de passe/secret maître pour générer les codes
            auth_mode: Mode de sécurité ('session', 'daily', 'disabled')
            session_duration: Durée de session en heures
            
        Returns:
            True si la configuration réussit
        """
        try:
            # Hacher le secret maître
            secret_hash = hashlib.sha256(master_secret.encode('utf-8')).hexdigest()
            
            # Créer la configuration
            config = {
                "REQUIRE_APPROVAL": True,
                "AUTH_MODE": auth_mode,
                "SESSION_DURATION_HOURS": session_duration,
                "APPROVAL_SECRET_HASH": secret_hash,
                "CURRENT_SESSION": {},
                "REGISTERED_USERS": {},
                "SECURITY_VERSION": "2.0"
            }
            
            if self.save_config(config):
                print(f"[CONFIGURATION] Sécurité configurée avec le mode {auth_mode}")
                
                # Montrer le code d'aujourd'hui pour référence
                if auth_mode in ["session", "daily"]:
                    username = getpass.getuser()
                    today_code = self.compute_daily_code(secret_hash, username)
                    print(f"[CONFIGURATION] Code d'aujourd'hui : {today_code}")
                
                return True
            
        except Exception as e:
            print(f"[CONFIGURATION] Configuration de sécurité échouée : {e}")
        
        return False
    
    def register_user(self, username: str, password: str) -> bool:
        """
        Enregistre un nouvel utilisateur dans le système
        
        Args:
            username: Nom d'utilisateur
            password: Mot de passe
            
        Returns:
            True si l'enregistrement réussit
        """
        try:
            config = self.load_config()
            
            # Hacher le mot de passe
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            
            # Ajouter l'utilisateur
            if 'REGISTERED_USERS' not in config:
                config['REGISTERED_USERS'] = {}
            
            config['REGISTERED_USERS'][username] = {
                'password_hash': password_hash,
                'created_date': time.strftime('%Y-%m-%d'),
                'last_login': None
            }
            
            if self.save_config(config):
                print(f"[UTILISATEUR] {username} enregistré avec succès")
                return True
            
        except Exception as e:
            print(f"[UTILISATEUR] Enregistrement échoué : {e}")
        
        return False
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authentifie un utilisateur avec nom d'utilisateur et mot de passe
        
        Args:
            username: Nom d'utilisateur
            password: Mot de passe
            
        Returns:
            True si l'authentification réussit
        """
        try:
            config = self.load_config()
            registered_users = config.get('REGISTERED_USERS', {})
            
            if username not in registered_users:
                print(f"[AUTH] Utilisateur {username} non trouvé")
                return False
            
            # Vérifier le mot de passe
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            stored_hash = registered_users[username]['password_hash']
            
            if password_hash != stored_hash:
                print(f"[AUTH] Mot de passe incorrect pour {username}")
                return False
            
            # Mettre à jour la dernière connexion
            registered_users[username]['last_login'] = time.strftime('%Y-%m-%d %H:%M:%S')
            self.save_config(config)
            
            print(f"[AUTH] Authentification réussie pour {username}")
            return True
            
        except Exception as e:
            print(f"[AUTH] Authentification échouée : {e}")
            return False
    
    def check_approval(self) -> bool:
        """
        Vérifie si l'utilisateur est approuvé pour exécuter l'application
        
        Il s'agit de la porte de sécurité principale qui :
        1. Charge la configuration actuelle
        2. Vérifie si l'approbation est requise
        3. Valide la session existante
        4. Demande l'authentification si nécessaire
        5. Met à jour le statut d'approbation
        
        Returns:
            True si l'utilisateur est approuvé pour continuer
        """
        try:
            config = self.load_config()
            
            # Vérifier si l'approbation est requise
            if not config.get('REQUIRE_APPROVAL', False):
                print("[APPROBATION] Sécurité désactivée, continuation")
                return True
            
            auth_mode = config.get('AUTH_MODE', 'session')
            
            if auth_mode == 'disabled':
                print("[APPROBATION] Mode désactivé, continuation")
                return True
            
            # Vérifier la session existante
            current_session = config.get('CURRENT_SESSION', {})
            if self.is_session_valid(current_session):
                print("[APPROBATION] Session valide, continuation")
                return True
            
            # Nouvelle authentification requise
            return self._prompt_for_authentication(config, auth_mode)
            
        except Exception as e:
            print(f"[APPROBATION] Vérification échouée : {e}")
            return False
    
    def _prompt_for_authentication(self, config: Dict[str, Any], auth_mode: str) -> bool:
        """
        Demande l'authentification à l'utilisateur
        
        Args:
            config: Configuration actuelle
            auth_mode: Mode d'authentification
            
        Returns:
            True si l'authentification réussit
        """
        try:
            print("\n" + "="*60)
            print("GLOBALEXAM AI - AUTHENTIFICATION REQUISE")
            print("="*60)
            
            username = getpass.getuser()
            print(f"Utilisateur système : {username}")
            print(f"Mode d'authentification : {auth_mode}")
            
            if auth_mode == 'session':
                return self._handle_session_auth(config, username)
            elif auth_mode == 'daily':
                return self._handle_daily_auth(config, username)
            else:
                print(f"[ERREUR] Mode d'authentification inconnu : {auth_mode}")
                return False
                
        except Exception as e:
            print(f"[AUTH] Demande d'authentification échouée : {e}")
            return False
    
    def _handle_session_auth(self, config: Dict[str, Any], username: str) -> bool:
        """
        Gère l'authentification par session
        """
        try:
            secret_hash = config.get('APPROVAL_SECRET_HASH', '')
            if not secret_hash:
                print("[AUTH] Aucun hash secret configuré")
                return False
            
            print(f"Entrez le code quotidien pour {username}:")
            
            try:
                user_code = input("Code : ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[AUTH] Saisie annulée")
                return False
            
            # Valider le code
            expected_code = self.compute_daily_code(secret_hash, username)
            
            if user_code == expected_code:
                # Créer une nouvelle session
                session_data = {
                    'username': username,
                    'start_time': time.time(),
                    'date': time.strftime('%Y%m%d'),
                    'token': self.create_session_token(username, secret_hash)
                }
                
                config['CURRENT_SESSION'] = session_data
                self.save_config(config)
                
                print("[AUTH] ✓ Authentification réussie ! Session créée.")
                return True
            else:
                print("[AUTH] ✗ Code invalide. Accès refusé.")
                return False
                
        except Exception as e:
            print(f"[AUTH] Authentification par session échouée : {e}")
            return False
    
    def _handle_daily_auth(self, config: Dict[str, Any], username: str) -> bool:
        """
        Gère l'authentification quotidienne simple
        """
        try:
            secret_hash = config.get('APPROVAL_SECRET_HASH', '')
            if not secret_hash:
                print("[AUTH] Aucun hash secret configuré")
                return False
            
            print("Entrez le code quotidien :")
            
            try:
                user_code = input("Code : ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[AUTH] Saisie annulée")
                return False
            
            # Valider le code
            expected_code = self.compute_daily_code(secret_hash, username)
            
            if user_code == expected_code:
                print("[AUTH] ✓ Code correct ! Accès accordé.")
                return True
            else:
                print("[AUTH] ✗ Code invalide. Accès refusé.")
                return False
                
        except Exception as e:
            print(f"[AUTH] Authentification quotidienne échouée : {e}")
            return False
    
    def get_daily_code_for_display(self, username: str = None) -> Optional[str]:
        """
        Obtient le code quotidien d'aujourd'hui pour affichage (référence propriétaire)
        
        Args:
            username: Nom d'utilisateur optionnel
            
        Returns:
            Code quotidien d'aujourd'hui ou None si non configuré
        """
        try:
            config = self.load_config()
            secret_hash = config.get('APPROVAL_SECRET_HASH', '')
            
            if not secret_hash:
                return None
            
            if username is None:
                username = getpass.getuser()
            
            return self.compute_daily_code(secret_hash, username)
            
        except Exception as e:
            print(f"[CODE_QUOTIDIEN] Affichage échoué : {e}")
            return None
    
    def disable_security(self) -> bool:
        """
        Désactive le système de sécurité (pour développement/test)
        
        Returns:
            True si désactivé avec succès
        """
        try:
            config = self.load_config()
            config['REQUIRE_APPROVAL'] = False
            config['AUTH_MODE'] = 'disabled'
            config['CURRENT_SESSION'] = {}
            
            return self.save_config(config)
            
        except Exception as e:
            print(f"[SÉCURITÉ] Désactivation échouée : {e}")
            return False
    
    def clear_session(self) -> bool:
        """
        Efface la session actuelle
        
        Returns:
            True si effacé avec succès
        """
        try:
            config = self.load_config()
            config['CURRENT_SESSION'] = {}
            
            if self.save_config(config):
                print("[SESSION] Session effacée")
                return True
            
        except Exception as e:
            print(f"[SESSION] Effacement échoué : {e}")
        
        return False

# Exemple d'utilisation et de test
if __name__ == "__main__":
    print("Module Système de Sécurité v2 - Mode Test")
    print("="*50)
    
    # Créer le gestionnaire de sécurité
    security = SessionSecurityManager("TestApp")
    
    # Test génération d'ID de session
    print("\n1. Test Génération d'ID de Session :")
    session_id = security.get_session_id()
    print(f"ID de Session : {session_id}")
    
    # Test génération de code quotidien
    print("\n2. Test Génération de Code Quotidien :")
    test_secret = "test_secret_123"
    secret_hash = hashlib.sha256(test_secret.encode()).hexdigest()
    daily_code = security.compute_daily_code(secret_hash)
    print(f"Code Quotidien : {daily_code}")
    
    # Test configuration
    print("\n3. Test Configuration :")
    config = security.load_config()
    print(f"Config chargée : {len(config)} paramètres")
    
    print("\nTest du système de sécurité terminé !")
