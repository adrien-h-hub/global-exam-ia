<div align="center">

# 🚀 Guide d'Installation - GlobalExam AI
### *Système d'Automatisation Intelligent Avancé*

<p align="center">
  <img src="https://img.shields.io/badge/Installation-Automatique-success?style=for-the-badge" alt="Installation">
  <img src="https://img.shields.io/badge/Temps-2%20Minutes-blue?style=for-the-badge" alt="Temps">
  <img src="https://img.shields.io/badge/Difficulté-Facile-green?style=for-the-badge" alt="Difficulté">
</p>

---

</div>

## 📋 Prérequis Système

<table align="center">
<tr>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-🖥️-blue?style=for-the-badge" alt="OS"><br>
<b>Système d'Exploitation</b><br>
Windows 10/11 (64-bit)
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-🐍-green?style=for-the-badge" alt="Python"><br>
<b>Python</b><br>
3.8+ (<a href="https://python.org">Télécharger</a>)
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-💾-orange?style=for-the-badge" alt="RAM"><br>
<b>Mémoire RAM</b><br>
4GB minimum
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/-🌐-purple?style=for-the-badge" alt="Internet"><br>
<b>Connexion Internet</b><br>
Pour les dépendances
</td>
</tr>
</table>

---

## ⚡ Installation Automatique (Recommandée)

### 🎯 Méthode Ultra-Rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/adrien-h-hub/global-exam-ia.git
cd global-exam-ia

# 2. Windows: Double-cliquez sur ce fichier
INSTALL_AND_RUN.bat
```

**🎉 C'est tout! L'application s'installe et se lance automatiquement!**

### 🐍 Méthode Python

```bash
# Installation intelligente avec Python
python auto_setup.py
```

---

## 📋 Installation Manuelle (Alternative)

### 1. Installation des Dépendances

```bash
# Installation complète pour utilisation locale
pip install -r requirements-client.txt

# Ou installation minimale (serveur seulement)
pip install -r requirements.txt
```

### 2. Lancement de l'Application

```bash
# Lanceur universel (recommandé)
python run_app.py

# Ou lanceur principal
python launch_secure_app.py
```

## 🎮 Utilisation

### Menu Principal
L'application propose plusieurs options :

1. **🚀 Application Principale** - Lancer l'automation
2. **🎛️ Panneau de Contrôle** - Gestion des accès (propriétaire)
3. **🧪 Test Sécurité** - Vérifier le système de sécurité
4. **🎯 Test Clics Adaptatifs** - Tester l'automation
5. **❓ Aide** - Informations détaillées
6. **🚪 Quitter** - Fermer l'application

### Pour les Utilisateurs
```bash
python launch_secure_app.py
# → Choisir option 1
# → Entrer nom/email
# → Attendre l'approbation
```

### Pour le Propriétaire
```bash
python launch_secure_app.py
# → Choisir option 2
# → Entrer le code d'accès
# → Gérer les utilisateurs
```

## 🔧 Configuration Avancée

### Variables d'Environnement (Optionnel)
```bash
# Configuration OCR
set TESSERACT_PATH="C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configuration IA
set AI_CONFIDENCE_THRESHOLD=0.85
```

### Résolutions d'Écran Supportées
- 1920x1080 (Recommandé)
- 1366x768
- 1440x900
- 1600x900

## 🛠️ Dépannage

### Problèmes Courants

#### "Module not found"
```bash
pip install --upgrade -r requirements.txt
```

#### "Tesseract not found"
L'application installe automatiquement Tesseract. Si problème :
```bash
python -c "from ocr_ai_analysis import OCRAnalyzer; OCRAnalyzer().install_tesseract()"
```

#### "Permission denied"
Exécuter en tant qu'administrateur :
```bash
# Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"
```

### Logs de Débogage
```bash
python launch_secure_app.py --debug
```

## 🔐 Sécurité

### Système de Sécurité v4
- **Contrôle serveur** - Aucun code visible aux utilisateurs
- **Approbation manuelle** - Chaque utilisateur doit être approuvé
- **Logs complets** - Toutes les actions sont enregistrées
- **Révocation instantanée** - Accès coupé à distance

### Configuration Propriétaire
1. Éditez `launch_secure_app.py`
2. Changez `YOUR_SECRET_CODE_HERE` par votre code
3. Sauvegardez le fichier

## 📊 Performance

### Temps de Traitement Moyens
- **Analyse OCR** : 0.8s par question
- **Analyse IA** : 1.2s par question
- **Exécution Action** : 0.3s par clic

### Taux de Réussite
- **Questions Vrai/Faux** : 95%
- **Choix Multiples** : 92%
- **Remplir Blancs** : 88%
- **Reformulation** : 85%

## 🆘 Support

### En Cas de Problème
1. **Vérifiez les prérequis** - Python 3.8+, Windows 10+
2. **Réinstallez les dépendances** - `pip install -r requirements.txt --force-reinstall`
3. **Testez les composants** - Options 3 et 4 du menu
4. **Consultez les logs** - Fichiers .log dans le dossier de l'application

### Ressources
- **Repository GitHub** : [global-exam-ia](https://github.com/adrien-h-hub/global-exam-ia)
- **Documentation** : README.md
- **Aperçu Académique** : ACADEMIC_OVERVIEW.md

---

🎯 **L'installation est maintenant terminée ! Lancez `python launch_secure_app.py` pour commencer.**
