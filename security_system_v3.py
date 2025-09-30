#!/usr/bin/env python3
"""
Système de Sécurité v3 pour GlobalExam AI
=========================================

Ce module implémente un système de sécurité avec autorisation unique :
1. Autorisation requise SEULEMENT au premier démarrage
2. Système de licence permanente liée à la machine
3. Impossible de partager une fois activé
4. Aucune saisie de code requise après activation

Auteur : Projet Étudiant
Objectif : Démonstration éducative d'un système de licence logicielle
"""

import hashlib
import json
import os
import time
import uuid
import getpass
import platform
import subprocess
from typing import Optional, Dict, Any
from datetime import datetime

class OneTimeLicenseManager:
    """
    Gestionnaire de Licence à Usage Unique
    
    Fonctionnement :
    1. Premier démarrage : Demande le code d'activation
    2. Génère une licence permanente liée à cette machine
    3. Démarrages suivants : Vérification automatique de la licence
    4. Impossible de copier la licence sur une autre machine
    """
    
    def __init__(self, app_name: str = "GlobalExamAI"):
        """
        Initialise le gestionnaire de licence unique
        
        Args:
            app_name: Nom de l'application pour le répertoire de configuration
        """
        self.app_name = app_name
        self.config_dir = self._get_config_directory()
        self.license_path = os.path.join(self.config_dir, 'license.dat')
        self.machine_fingerprint = self._generate_machine_fingerprint()
        
        # S'assurer que le répertoire de configuration existe
        os.makedirs(self.config_dir, exist_ok=True)
        
        print(f"[LICENCE] Initialisé pour {app_name}")
        print(f"[LICENCE] Empreinte machine : {self.machine_fingerprint[:16]}...")
    
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
    
    def _generate_machine_fingerprint(self) -> str:
        """
        Génère une empreinte unique de la machine
        
        Cette empreinte combine plusieurs identifiants matériels pour créer
        une signature unique qui ne peut pas être facilement copiée :
        
        Méthodes utilisées :
        1. Adresse MAC (la plus fiable)
        2. ID CPU (Windows uniquement)
        3. UUID système (carte mère)
        4. Nom de l'ordinateur
        5. Nom d'utilisateur
        6. Informations système
        
        Returns:
            Hash SHA-256 de l'empreinte machine combinée
        """
        identifiers = []
        
        try:
            # Méthode 1 : Adresse MAC (la plus fiable)
            mac = uuid.getnode()
            identifiers.append(str(mac))
            print(f"[EMPREINTE] MAC : {hex(mac)}")
            
        except Exception as e:
            print(f"[EMPREINTE] MAC échoué : {e}")
        
        try:
            # Méthode 2 : ID CPU (Windows uniquement)
            if os.name == 'nt':
                result = subprocess.run(['wmic', 'cpu', 'get', 'processorid'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    cpu_id = ''.join(result.stdout.split()[1:])  # Enlever l'en-tête
                    if cpu_id and cpu_id != 'ProcessorId':
                        identifiers.append(cpu_id)
                        print(f"[EMPREINTE] CPU ID : {cpu_id[:16]}...")
            
        except Exception as e:
            print(f"[EMPREINTE] CPU ID échoué : {e}")
        
        try:
            # Méthode 3 : UUID système (carte mère)
            if os.name == 'nt':
                result = subprocess.run(['wmic', 'csproduct', 'get', 'uuid'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    system_uuid = ''.join(result.stdout.split()[1:])  # Enlever l'en-tête
                    if system_uuid and system_uuid != 'UUID':
                        identifiers.append(system_uuid)
                        print(f"[EMPREINTE] Système UUID : {system_uuid[:16]}...")
            
        except Exception as e:
            print(f"[EMPREINTE] Système UUID échoué : {e}")
        
        try:
            # Méthode 4 : Nom de l'ordinateur
            computer_name = platform.node()
            identifiers.append(computer_name)
            print(f"[EMPREINTE] Nom ordinateur : {computer_name}")
            
        except Exception as e:
            print(f"[EMPREINTE] Nom ordinateur échoué : {e}")
        
        try:
            # Méthode 5 : Nom d'utilisateur
            username = getpass.getuser()
            identifiers.append(username)
            print(f"[EMPREINTE] Utilisateur : {username}")
            
        except Exception as e:
            print(f"[EMPREINTE] Utilisateur échoué : {e}")
        
        try:
            # Méthode 6 : Informations système
            system_info = f"{platform.system()}{platform.machine()}{platform.processor()}"
            identifiers.append(system_info)
            print(f"[EMPREINTE] Système : {platform.system()}")
            
        except Exception as e:
            print(f"[EMPREINTE] Informations système échouées : {e}")
        
        # Fallback si aucun identifiant n'est disponible
        if not identifiers:
            fallback = f"{time.time()}{os.getcwd()}{platform.platform()}"
            identifiers.append(fallback)
            print(f"[EMPREINTE] Utilisation du fallback")
        
        # Créer un hash stable à partir de tous les identifiants
        combined = ''.join(sorted(identifiers))
        fingerprint = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        print(f"[EMPREINTE] Générée : {fingerprint[:16]}...")
        return fingerprint
    
    def _generate_activation_code(self, master_secret: str) -> str:
        """
        Génère le code d'activation basé sur l'empreinte machine et le secret
        
        Args:
            master_secret: Secret maître fourni par le propriétaire
            
        Returns:
            Code d'activation à 8 chiffres
        """
        combined = f"{self.machine_fingerprint}{master_secret}"
        hash_value = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        activation_code = f"{int(hash_value, 16) % 100000000:08d}"
        
        print(f"[ACTIVATION] Code généré : {activation_code}")
        return activation_code
    
    def _create_license(self, activation_code: str, master_secret: str) -> Dict[str, Any]:
        """
        Crée une licence permanente pour cette machine
        
        Args:
            activation_code: Code d'activation fourni
            master_secret: Secret maître
            
        Returns:
            Dictionnaire de licence
        """
        license_data = {
            'machine_fingerprint': self.machine_fingerprint,
            'activation_code': activation_code,
            'master_secret_hash': hashlib.sha256(master_secret.encode()).hexdigest(),
            'creation_date': datetime.now().isoformat(),
            'username': getpass.getuser(),
            'computer_name': platform.node(),
            'license_version': '3.0',
            'app_name': self.app_name,
            # Signature de la licence pour éviter la modification
            'signature': None
        }
        
        # Créer une signature de la licence
        license_string = json.dumps(license_data, sort_keys=True)
        signature = hashlib.sha256(license_string.encode()).hexdigest()
        license_data['signature'] = signature
        
        return license_data
    
    def _save_license(self, license_data: Dict[str, Any]) -> bool:
        """
        Sauvegarde la licence de manière sécurisée
        
        Args:
            license_data: Données de licence à sauvegarder
            
        Returns:
            True si sauvegardé avec succès
        """
        try:
            # Chiffrer les données de licence (simple obfuscation)
            license_json = json.dumps(license_data, indent=2)
            encoded_license = license_json.encode('utf-8')
            
            # Simple XOR avec la clé basée sur l'empreinte machine
            key = self.machine_fingerprint[:32].encode('utf-8')
            encrypted_license = bytearray()
            
            for i, byte in enumerate(encoded_license):
                encrypted_license.append(byte ^ key[i % len(key)])
            
            # Sauvegarder le fichier de licence
            with open(self.license_path, 'wb') as f:
                f.write(encrypted_license)
            
            print(f"[LICENCE] Sauvegardée : {self.license_path}")
            return True
            
        except Exception as e:
            print(f"[LICENCE] Sauvegarde échouée : {e}")
            return False
    
    def _load_license(self) -> Optional[Dict[str, Any]]:
        """
        Charge et valide la licence existante
        
        Returns:
            Données de licence si valides, None sinon
        """
        try:
            if not os.path.exists(self.license_path):
                print("[LICENCE] Aucun fichier de licence trouvé")
                return None
            
            # Charger et déchiffrer la licence
            with open(self.license_path, 'rb') as f:
                encrypted_license = f.read()
            
            # Déchiffrer avec la clé basée sur l'empreinte machine
            key = self.machine_fingerprint[:32].encode('utf-8')
            decrypted_license = bytearray()
            
            for i, byte in enumerate(encrypted_license):
                decrypted_license.append(byte ^ key[i % len(key)])
            
            # Parser JSON
            license_json = decrypted_license.decode('utf-8')
            license_data = json.loads(license_json)
            
            # Valider la licence
            if self._validate_license(license_data):
                print("[LICENCE] Licence valide chargée")
                return license_data
            else:
                print("[LICENCE] Licence invalide")
                return None
                
        except Exception as e:
            print(f"[LICENCE] Chargement échoué : {e}")
            return None
    
    def _validate_license(self, license_data: Dict[str, Any]) -> bool:
        """
        Valide l'intégrité et l'authenticité de la licence
        
        Args:
            license_data: Données de licence à valider
            
        Returns:
            True si la licence est valide
        """
        try:
            # Vérifier l'empreinte machine
            if license_data.get('machine_fingerprint') != self.machine_fingerprint:
                print("[VALIDATION] Empreinte machine ne correspond pas")
                return False
            
            # Vérifier la signature
            signature = license_data.pop('signature', None)
            license_string = json.dumps(license_data, sort_keys=True)
            expected_signature = hashlib.sha256(license_string.encode()).hexdigest()
            license_data['signature'] = signature  # Remettre la signature
            
            if signature != expected_signature:
                print("[VALIDATION] Signature de licence invalide")
                return False
            
            # Vérifier la version
            if license_data.get('license_version') != '3.0':
                print("[VALIDATION] Version de licence incompatible")
                return False
            
            print("[VALIDATION] Licence valide")
            return True
            
        except Exception as e:
            print(f"[VALIDATION] Validation échouée : {e}")
            return False
    
    def is_licensed(self) -> bool:
        """
        Vérifie si l'application est déjà licenciée sur cette machine
        
        Returns:
            True si une licence valide existe
        """
        license_data = self._load_license()
        return license_data is not None
    
    def activate_license(self, master_secret: str) -> bool:
        """
        Active la licence pour cette machine (première utilisation seulement)
        
        Args:
            master_secret: Secret maître fourni par le propriétaire
            
        Returns:
            True si l'activation réussit
        """
        try:
            print("\n" + "="*60)
            print("ACTIVATION DE LICENCE - PREMIÈRE UTILISATION")
            print("="*60)
            
            # Générer le code d'activation attendu
            expected_code = self._generate_activation_code(master_secret)
            
            print(f"Machine : {platform.node()}")
            print(f"Utilisateur : {getpass.getuser()}")
            print(f"Empreinte : {self.machine_fingerprint[:16]}...")
            print(f"\nCode d'activation requis : {expected_code}")
            print("\nVeuillez entrer le code d'activation :")
            
            try:
                user_code = input("Code : ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[ACTIVATION] Activation annulée")
                return False
            
            # Vérifier le code
            if user_code == expected_code:
                # Créer et sauvegarder la licence
                license_data = self._create_license(expected_code, master_secret)
                
                if self._save_license(license_data):
                    print("\n[ACTIVATION] ✓ Licence activée avec succès !")
                    print("[ACTIVATION] L'application est maintenant autorisée sur cette machine")
                    print("[ACTIVATION] Aucune saisie de code ne sera requise à l'avenir")
                    return True
                else:
                    print("\n[ACTIVATION] ✗ Échec de sauvegarde de la licence")
                    return False
            else:
                print(f"\n[ACTIVATION] ✗ Code incorrect")
                print(f"Attendu : {expected_code}")
                print(f"Reçu    : {user_code}")
                return False
                
        except Exception as e:
            print(f"[ACTIVATION] Activation échouée : {e}")
            return False
    
    def check_authorization(self) -> bool:
        """
        Vérifie l'autorisation d'exécution
        
        Il s'agit de la porte de sécurité principale qui :
        1. Vérifie si une licence existe déjà
        2. Si oui, validation automatique (silencieuse)
        3. Si non, demande l'activation unique
        
        Returns:
            True si autorisé à continuer
        """
        try:
            print("\n[AUTORISATION] Vérification de la licence...")
            
            # Vérifier si déjà licencié
            if self.is_licensed():
                print("[AUTORISATION] ✓ Licence valide trouvée - accès autorisé")
                return True
            
            # Première utilisation - demander l'activation
            print("[AUTORISATION] Première utilisation détectée")
            print("[AUTORISATION] Activation de licence requise")
            
            return self._prompt_for_activation()
            
        except Exception as e:
            print(f"[AUTORISATION] Vérification échouée : {e}")
            return False
    
    def _prompt_for_activation(self) -> bool:
        """
        Demande l'activation à l'utilisateur
        
        Returns:
            True si l'activation réussit
        """
        try:
            print("\n" + "="*60)
            print("GLOBALEXAM AI - ACTIVATION REQUISE")
            print("="*60)
            print("Cette application nécessite une activation unique.")
            print("Après activation, aucun code ne sera plus demandé.")
            print("="*60)
            
            print("\nPour obtenir votre code d'activation :")
            print(f"1. Empreinte machine : {self.machine_fingerprint[:16]}...")
            print(f"2. Utilisateur : {getpass.getuser()}")
            print(f"3. Ordinateur : {platform.node()}")
            print("\nContactez le propriétaire avec ces informations.")
            
            try:
                master_secret = input("\nEntrez le secret maître : ").strip()
                if not master_secret:
                    print("[ACTIVATION] Secret maître requis")
                    return False
                
                return self.activate_license(master_secret)
                
            except (EOFError, KeyboardInterrupt):
                print("\n[ACTIVATION] Activation annulée")
                return False
                
        except Exception as e:
            print(f"[ACTIVATION] Demande d'activation échouée : {e}")
            return False
    
    def get_activation_code_for_machine(self, master_secret: str, 
                                       machine_fingerprint: str = None) -> str:
        """
        Génère le code d'activation pour une machine spécifique (usage propriétaire)
        
        Args:
            master_secret: Secret maître
            machine_fingerprint: Empreinte machine (utilise celle actuelle si None)
            
        Returns:
            Code d'activation à 8 chiffres
        """
        if machine_fingerprint is None:
            machine_fingerprint = self.machine_fingerprint
        
        combined = f"{machine_fingerprint}{master_secret}"
        hash_value = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        activation_code = f"{int(hash_value, 16) % 100000000:08d}"
        
        return activation_code
    
    def revoke_license(self) -> bool:
        """
        Révoque la licence (supprime le fichier de licence)
        
        Returns:
            True si révoqué avec succès
        """
        try:
            if os.path.exists(self.license_path):
                os.remove(self.license_path)
                print("[LICENCE] Licence révoquée")
                return True
            else:
                print("[LICENCE] Aucune licence à révoquer")
                return True
                
        except Exception as e:
            print(f"[LICENCE] Révocation échouée : {e}")
            return False
    
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """
        Obtient les informations de licence (si autorisé)
        
        Returns:
            Informations de licence ou None
        """
        license_data = self._load_license()
        if license_data:
            # Retourner seulement les informations non sensibles
            return {
                'creation_date': license_data.get('creation_date'),
                'username': license_data.get('username'),
                'computer_name': license_data.get('computer_name'),
                'license_version': license_data.get('license_version'),
                'app_name': license_data.get('app_name')
            }
        return None

# Exemple d'utilisation et de test
if __name__ == "__main__":
    print("Module Système de Licence v3 - Mode Test")
    print("="*50)
    
    # Créer le gestionnaire de licence
    license_manager = OneTimeLicenseManager("TestApp")
    
    # Test génération d'empreinte machine
    print(f"\nEmpreinte machine : {license_manager.machine_fingerprint}")
    
    # Test génération de code d'activation
    test_secret = "test_secret_123"
    activation_code = license_manager.get_activation_code_for_machine(test_secret)
    print(f"Code d'activation : {activation_code}")
    
    # Test statut de licence
    print(f"Déjà licencié : {license_manager.is_licensed()}")
    
    print("\nTest du système de licence terminé !")
