# Guide d'Installation et de Configuration

## 🚀 Démarrage Rapide

### Prérequis
- Windows 10/11 (64-bit)
- Python 3.8 ou supérieur
- Privilèges administrateur (pour l'installation de Tesseract)
- Connexion Internet (pour l'auto-installation)

### Installation en Une Commande
```bash
# Exécutez cette commande unique pour tout installer automatiquement
python main_application.py --setup-security
```

## 📋 Étapes d'Installation Détaillées

### Étape 1 : Configuration Python
Si vous n'avez pas Python installé :

1. Téléchargez Python depuis [python.org](https://python.org)
2. Pendant l'installation, cochez "Ajouter Python au PATH"
3. Vérifiez l'installation :
```bash
python --version
```

### Étape 2 : Télécharger le Projet
```bash
# Clonez ou téléchargez les fichiers du projet
git clone https://github.com/adrien-h-hub/global-exam-ia.git
cd global-exam-ia
```

### Étape 3 : Exécuter l'Auto-Installation
```bash
# Ceci installera automatiquement toutes les dépendances
python main_application.py --setup-security
```

L'auto-installateur va :
- Installer les packages Python (PyAutoGUI, OpenCV, Pillow, etc.)
- Télécharger et installer Tesseract OCR
- Configurer les chemins système
- Paramétrer le système de sécurité

### Étape 4 : Configuration de Sécurité
Pendant la configuration, vous serez invité à saisir :

1. **Secret Maître** : Votre mot de passe pour générer les codes quotidiens
2. **Mode de Sécurité** : 
   - `session` (recommandé) : Sessions temporaires avec codes quotidiens
   - `daily` : Codes quotidiens simples
   - `disabled` : Sécurité désactivée
3. **Durée de Session** : Durée en heures (par défaut : 8 heures)

Exemple de configuration :
```
Entrez le secret maître (mot de passe) : MonMotDePasseSecret123
Mode de sécurité (session/daily/disabled) [session] : session
Durée de session en heures [8] : 8
```

## 🔧 Installation Manuelle (Si l'Auto-Installation Échoue)

### Installer les Packages Python
```bash
pip install pyautogui
pip install Pillow
pip install opencv-python
pip install numpy
pip install pytesseract
```

### Installer Tesseract OCR Manuellement

1. Téléchargez l'installateur Tesseract :
   - Allez sur : https://github.com/UB-Mannheim/tesseract/releases
   - Téléchargez : `tesseract-ocr-w64-setup-5.3.0.20221214.exe`

2. Exécutez l'installateur avec les privilèges administrateur
3. Ajoutez au PATH : `C:\Program Files\Tesseract-OCR`

### Vérifier l'Installation
```bash
# Tester Tesseract
tesseract --version

# Tester les packages Python
python -c "import pyautogui, cv2, pytesseract; print('Tous les packages OK')"
```

## ⚙️ Options de Configuration

### Paramètres de Sécurité
Situés dans : `%APPDATA%\GlobalExamAI\config.json`

```json
{
  "REQUIRE_APPROVAL": true,
  "AUTH_MODE": "session",
  "SESSION_DURATION_HOURS": 8,
  "APPROVAL_SECRET_HASH": "hash_sha256_ici",
  "CURRENT_SESSION": {},
  "REGISTERED_USERS": {},
  "SECURITY_VERSION": "2.0"
}
```

### Paramètres d'Application
```bash
# Afficher l'ID utilisateur actuel
python main_application.py --show-user-id

# Afficher le code quotidien d'aujourd'hui
python main_application.py --show-daily-code

# Désactiver la sécurité (mode développement)
python main_application.py --disable-security
```

## 🎮 Exemples d'Utilisation

### Utilisation de Base
```bash
# Exécuter avec les paramètres par défaut
python main_application.py
```

### Utilisation Avancée
```bash
# Mode debug avec captures d'écran
python main_application.py --debug

# Limiter à 10 questions
python main_application.py --max-questions 10

# Mode développement (sans sécurité)
python main_application.py --disable-security --debug
```

### Utilisation avec Python 3.13 (Problèmes de PATH)
```bash
# Utiliser le fichier batch fourni
run_with_python313.bat

# Ou utiliser PowerShell directement
& "C:\Users\Dardq\AppData\Local\Programs\Python\Python313\python.exe" main_application.py
```

## 🔍 Dépannage

### Problèmes Courants

#### 1. Erreur "Tesseract non trouvé"
```bash
# Vérifier si Tesseract est installé
tesseract --version

# Si non trouvé, ajouter au PATH manuellement :
# Windows : Ajouter C:\Program Files\Tesseract-OCR au PATH
# Ou réinstaller avec les privilèges administrateur
```

#### 2. Erreur "Permission Refusée"
```bash
# Exécuter en tant qu'administrateur
# Clic droit sur Invite de Commandes → "Exécuter en tant qu'administrateur"
python main_application.py --setup-security
```

#### 3. Erreur "Module non trouvé"
```bash
# Réinstaller les packages Python
pip install --upgrade pyautogui opencv-python pillow numpy pytesseract
```

#### 4. Problèmes de Configuration de Sécurité
```bash
# Réinitialiser la configuration de sécurité
python main_application.py --disable-security
python main_application.py --setup-security
```

### Mode Debug
Activez le mode debug pour voir les journaux détaillés :
```bash
python main_application.py --debug
```

Ceci va :
- Sauvegarder les captures d'écran de chaque question
- Afficher l'extraction de texte OCR détaillée
- Montrer les résultats d'analyse IA
- Enregistrer toutes les coordonnées de clic

### Fichiers de Journal
Vérifiez ces emplacements pour les journaux :
- Captures d'écran : `%APPDATA%\GlobalExamAI\screenshots\`
- Configuration : `%APPDATA%\GlobalExamAI\config.json`
- Images de debug : Répertoire courant (`question_*.png`)

## 🔒 Nouvelles Fonctionnalités de Sécurité

### Authentification par Session
Le nouveau système de sécurité utilise :

1. **Sessions Temporaires** : Jetons d'accès qui expirent automatiquement
2. **Codes par Utilisateur** : Codes uniques basés sur le nom d'utilisateur
3. **Pas de Liaison Machine** : Fonctionne sur différents ordinateurs avec le même utilisateur
4. **Expiration Automatique** : Sessions expirent après 8 heures par défaut

### Gestion des Codes Quotidiens
```bash
# Obtenir le code d'aujourd'hui (à exécuter quotidiennement)
python main_application.py --show-daily-code

# Exemple de sortie : Code quotidien d'aujourd'hui : 123456
```

### Gestion des Sessions
```bash
# Effacer la session actuelle
python main_application.py --clear-session

# Vérifier le statut de session
python main_application.py --session-status
```

## 📱 Configuration Multi-Utilisateurs

Pour utiliser sur plusieurs utilisateurs autorisés :

1. **Configuration sur chaque compte utilisateur :**
```bash
# Sur le Compte Utilisateur 1
python main_application.py --setup-security
# Utiliser le même secret maître

# Sur le Compte Utilisateur 2
python main_application.py --setup-security
# Utiliser le même secret maître
```

2. **Chaque utilisateur obtient des codes quotidiens uniques :**
```bash
# Code Utilisateur 1 : 123456
# Code Utilisateur 2 : 789012
# (Les codes sont différents en raison des noms d'utilisateur différents)
```

## 🔄 Mises à Jour et Maintenance

### Mise à Jour du Système
```bash
# Télécharger la nouvelle version
git pull origin main

# Réinstaller les dépendances si nécessaire
python main_application.py --setup-security
```

### Sauvegarde de Configuration
```bash
# Sauvegarder votre configuration (important !)
copy "%APPDATA%\GlobalExamAI\config.json" "backup_config.json"
```

### Réinitialisation aux Paramètres d'Usine
```bash
# Réinitialisation complète (nécessitera une reconfiguration)
rmdir /s "%APPDATA%\GlobalExamAI"
python main_application.py --setup-security
```

## 🎯 Optimisation des Performances

### Optimiser pour la Vitesse
```bash
# Réduire la limite de questions pour des tests plus rapides
python main_application.py --max-questions 5

# Désactiver le mode debug en production
python main_application.py  # (pas de flag --debug)
```

### Optimiser pour la Précision
```bash
# Activer le mode debug pour analyser les échecs
python main_application.py --debug

# Examiner les captures d'écran pour améliorer la précision des coordonnées
# Vérifier la qualité d'extraction de texte OCR
```

## 🆘 Obtenir de l'Aide

### Auto-Diagnostic
```bash
# Exécuter la vérification système
python main_application.py --show-user-id
python main_application.py --show-daily-code

# Tester les composants individuels
python security_system_v2.py      # Tester la sécurité
python ocr_ai_analysis.py         # Tester OCR/IA
python visual_automation.py       # Tester l'automatisation
```

### Solutions Communes

| Problème | Solution |
|----------|----------|
| Faible taux de réussite | Activer le mode debug, vérifier les captures d'écran |
| Erreurs de sécurité | Reconfigurer avec `--setup-security` |
| Échecs OCR | Réinstaller Tesseract avec droits admin |
| Échecs de clic | Vérifier la résolution d'écran et la mise à l'échelle |
| Problèmes de performance | Fermer autres applications, utiliser SSD |

### Codes d'Erreur
- **Code de Sortie 0** : Succès
- **Code de Sortie 1** : Erreur générale
- **Erreur de Sécurité** : Approbation échouée
- **Erreur de Module** : Dépendances manquantes

## 📞 Informations de Support

Il s'agit d'un projet éducatif. À des fins d'apprentissage :

1. **Lisez la documentation** attentivement
2. **Vérifiez la section dépannage** en premier
3. **Activez le mode debug** pour comprendre les problèmes
4. **Examinez les commentaires du code** pour les détails techniques
5. **Expérimentez en sécurité** en mode développement

Rappel : Ce projet est pour la démonstration éducative des concepts de programmation incluant l'automatisation, l'IA, la vision par ordinateur, et l'implémentation de sécurité.
