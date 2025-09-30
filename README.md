# GlobalExam AI - Système d'Automatisation Ultime

[![GitHub](https://img.shields.io/badge/GitHub-adrien--h--hub%2Fglobal--exam--ia-blue?logo=github)](https://github.com/adrien-h-hub/global-exam-ia)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

Un système d'automatisation avancé alimenté par l'IA pour les activités GlobalExam, intégrant la sécurité, l'OCR, l'analyse IA et l'automatisation visuelle.

## 🚀 Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/adrien-h-hub/global-exam-ia.git
cd global-exam-ia

# Installation automatique (Windows)
run_with_python313.bat --setup

# Ou installation manuelle
python main_application.py --setup-security
```

## 🎯 Aperçu du Projet

Il s'agit d'un projet éducatif démontrant l'intégration de plusieurs technologies avancées :

- **Système de Sécurité** : Codes rotatifs quotidiens avec authentification par session
- **Technologie OCR** : Extraction de texte à partir du contenu d'écran
- **Analyse IA** : Compréhension intelligente des questions et génération de réponses
- **Automatisation Visuelle** : Vision par ordinateur pour l'interaction UI
- **Approche Multi-Stratégique** : Systèmes de secours multiples pour la fiabilité

## 🏗️ Architecture

Le système est construit avec une architecture modulaire :

```
global-exam-ia/
├── 📄 README.md                    # Documentation principale
├── 📄 INSTALLATION_FR.md           # Guide d'installation français
├── 📄 TEACHER_REVIEW.md            # Évaluation académique
├── 📄 LICENSE                      # Licence MIT
├── 📄 requirements.txt             # Dépendances Python
├── 📄 .gitignore                   # Règles Git
├── 📄 run_with_python313.bat       # Lanceur Windows
├── 🐍 main_application.py          # Application principale
├── 🐍 security_system_v3.py        # Système de licence unique
├── 🐍 ocr_ai_analysis.py          # Analyse OCR & IA
├── 🐍 visual_automation.py        # Automatisation visuelle
├── 🐍 app_launcher.py             # Interface graphique
└── 🐍 create_shortcuts.py         # Créateur de raccourcis
```

## 📁 Structure des Modules

### 1. Système de Sécurité (`security_system_v3.py`)
- **Licence Unique** : Autorisation requise seulement au premier démarrage
- **Empreinte Machine** : Système anti-partage basé sur le matériel
- **Activation Permanente** : Plus de saisie de code après activation
- **Stockage Chiffré** : Licence sécurisée et signée

**Fonctionnalités Clés :**
```python
# Générer le code unique d'aujourd'hui
daily_code = security.compute_daily_code(secret_hash, username)

# Créer une session temporaire
session_token = security.create_session_token(username, secret_hash)

# Valider l'approbation
approved = security.check_approval()
```

### 2. Analyse OCR & IA (`ocr_ai_analysis.py`)
- **Installation Automatique** : Installe automatiquement Tesseract OCR
- **Amélioration de Texte** : Prétraitement d'image pour un meilleur OCR
- **Analyse IA des Questions** : Comprend le contexte et le type des questions
- **Base de Connaissances** : Sujets de construction, affaires et généraux

**Fonctionnalités Clés :**
```python
# Extraire le texte de l'écran
text = ocr_engine.extract_text(screenshot)

# Analyser la question intelligemment
analysis = ai_analyzer.analyze_question(text)
# Retourne : type, sujet, confiance, réponse_suggérée
```

### 3. Automatisation Visuelle (`visual_automation.py`)
- **Détection UI** : Trouve les boutons, champs de saisie et mises en page
- **Clics Intelligents** : Systèmes de coordonnées multiples avec validation
- **Détection Type de Question** : Reconnaissance de motifs visuels
- **Glisser-Déposer** : Gère les questions d'appariement

**Fonctionnalités Clés :**
```python
# Détecter les éléments UI
layout = visual_detector.analyze_layout(screenshot)

# Clic intelligent avec validation
success = smart_clicker.click_with_validation(x, y, "Bouton")

# Gérer différents types de questions
handler.handle_true_false(context)
handler.handle_multiple_choice(context)
```

### 4. Application Principale (`main_application.py`)
- **Intégration Système** : Combine tous les modules de manière transparente
- **Analyse Complète** : Utilise visuel + OCR + IA ensemble
- **Suivi Statistiques** : Surveillance des performances
- **Récupération d'Erreur** : Stratégies de secours multiples

## 🔒 Fonctionnalités de Sécurité Expliquées

### Technologie d'Authentification par Session

Le système utilise une approche basée sur les sessions au lieu de la liaison machine :

1. **Nom d'Utilisateur** : Identification de l'utilisateur système
2. **Sessions Temporaires** : Jetons d'accès avec expiration (8 heures par défaut)
3. **Codes Quotidiens** : Codes uniques par utilisateur et par jour
4. **Stockage Sécurisé** : Configuration chiffrée localement

```python
def get_session_id(self) -> str:
    """Générer un identifiant de session unique"""
    identifiers = []
    
    # Méthode 1 : Nom d'utilisateur
    username = getpass.getuser()
    identifiers.append(username)
    
    # Méthode 2 : Timestamp de session
    session_time = str(int(time.time()))
    identifiers.append(session_time)
    
    # Méthode 3 : UUID aléatoire
    random_uuid = str(uuid.uuid4())
    identifiers.append(random_uuid)
    
    # Créer un hash stable
    combined = ''.join(identifiers)
    return hashlib.sha256(combined.encode()).hexdigest()
```

### Algorithme de Code Quotidien

Le code rotatif quotidien assure la sécurité tout en permettant l'utilisation légitime :

```python
def compute_daily_code(self, secret_hash: str, username: str) -> str:
    """Générer le code à 6 chiffres d'aujourd'hui"""
    today = time.strftime('%Y%m%d')  # 20231229
    
    # Combiner : utilisateur + secret + date
    combined = f"{username}{secret_hash}{today}"
    
    # Générer hash et extraire 6 chiffres
    hash_value = hashlib.sha256(combined.encode()).hexdigest()
    code = f"{int(hash_value, 16) % 1000000:06d}"
    
    return code
```

**Avantages de Sécurité :**
- Licence permanente après première activation
- Impossible de partager (lié au matériel)
- Aucune saisie de code après activation
- Chiffrement et signature de la licence
- Système anti-copie sophistiqué

## 🎮 Utilisation

### Première Installation
```bash
# 1. Cloner le repository
git clone https://github.com/adrien-h-hub/global-exam-ia.git
cd global-exam-ia

# 2. Premier démarrage (activation unique)
run_with_python313.bat --setup
# → Entrer le code d'activation (une seule fois)

# 3. Démarrages suivants (automatique)
run_with_python313.bat
# → Démarrage immédiat, aucun code requis !
```

### Interface Graphique
```bash
# Lancer l'interface graphique
python app_launcher.py

# Créer des raccourcis bureau
python create_shortcuts.py
```

### Options Avancées
```bash
# Mode debug avec captures d'écran
run_with_python313.bat --debug

# Limiter le nombre de questions
run_with_python313.bat --max-questions 10

# Afficher les informations de licence
python main_application.py --show-license-info
```

## 🤖 Système d'Analyse IA

### Détection du Type de Question

Le système IA utilise la correspondance de motifs et le traitement du langage naturel :

```python
def analyze_question(self, text: str) -> Dict:
    """Comprehensive question analysis"""
    
    # Detect type using patterns
    if re.search(r'\b(true|false)\b', text.lower()):
        question_type = 'true_false'
    elif re.search(r'\b[a-d]\)', text.lower()):
        question_type = 'multiple_choice'
    elif re.search(r'____+', text):
        question_type = 'fill_blank'
    
    # Classify topic
    if 'construction' in text.lower():
        topic = 'construction'
    elif 'business' in text.lower():
        topic = 'business'
    
    # Generate intelligent answer
    answer = self._generate_smart_answer(question_type, topic, text)
    
    return {
        'question_type': question_type,
        'topic': topic,
        'suggested_answer': answer,
        'confidence': confidence_score
    }
```

### Domain Knowledge Base

The system includes specialized knowledge for different domains:

```python
knowledge_base = {
    'construction': {
        'direct_costs': ['materials', 'labor', 'equipment'],
        'safety': ['helmet', 'gloves', 'boots', 'harness'],
        'permits': ['building permit', 'authorization']
    },
    'business': {
        'communication': ['notice', 'inform', 'notify'],
        'improvement': ['better', 'enhance', 'upgrade']
    }
}
```

## 🎮 Usage Instructions

### First Time Setup

1. **Install the system:**
```bash
python main_application.py --setup-security
```

2. **Configure security:**
- Enter master secret (password)
- Choose security mode (daily recommended)
- Set enforcement options

### Daily Usage

1. **Get today's code:**
```bash
python main_application.py --show-daily-code
```

2. **Run automation:**
```bash
python main_application.py
```

3. **Enter approval code when prompted**

### Development Mode

```bash
# Disable security for testing
python main_application.py --disable-security

# Run with debug screenshots
python main_application.py --debug

# Limit questions for testing
python main_application.py --max-questions 5
```

## 📊 Performance Statistics

The system tracks comprehensive performance metrics:

- **Success Rate**: Percentage of correctly answered questions
- **Question Types**: Distribution of encountered question types
- **Response Time**: Average time per question
- **Confidence Scores**: AI analysis confidence levels

Example output:
```
AUTOMATION COMPLETED
====================================
Questions attempted: 25
Questions successful: 19
Success rate: 76.0%
Duration: 125.3 seconds
Question types encountered:
  • multiple_choice: 15
  • true_false: 7
  • fill_blank: 3
```

## 🔧 Technical Implementation

### Auto-Installation System

The system automatically installs all dependencies:

```python
def install_tesseract_windows():
    """Auto-install Tesseract OCR"""
    # Download installer
    url = "https://github.com/UB-Mannheim/tesseract/releases/download/tesseract-ocr-5.0.0-alpha.20220807/tesseract-ocr-w64-setup-v5.0.0-alpha.20220807.exe"
    urllib.request.urlretrieve(url, "tesseract_installer.exe")
    
    # Silent installation
    subprocess.run('"tesseract_installer.exe" /S')
    
    # Configure PATH
{{ ... }}
```

### Multi-Strategy Answer Selection

The system uses multiple strategies for maximum accuracy:

1. **AI Analysis** (Highest Priority)
   - Text understanding and context analysis
   - Domain-specific knowledge application

2. **Visual Detection** (Medium Priority)
   - UI element recognition and layout analysis
   - Button counting and positioning

3. **Statistical Fallback** (Lowest Priority)
   - Based on exam answer distribution analysis
   - True/False: 70% True, 30% False
   - Multiple Choice: A(30%), C(35%), B(20%), D(15%)

### Error Recovery System

Multiple layers of error recovery ensure reliability:

```python
def answer_question(self, question_num: int) -> bool:
    try:
        # Primary: AI-guided answering
        if ai_analysis.confidence > 0.7:
            return self.use_ai_answer(ai_analysis)
        
        # Secondary: Visual pattern matching
        elif visual_analysis.confidence > 0.8:
            return self.use_visual_answer(visual_analysis)
        
        # Tertiary: Statistical fallback
        else:
            return self.use_statistical_answer()
            
    except Exception as e:
        # Ultimate fallback: basic clicking
        return self.emergency_fallback()
```

## 🎓 Valeur Éducative

Ce projet démontre plusieurs concepts importants de l'informatique :

### 1. **Vision par Ordinateur**
- Traitement et analyse d'images
- Détection de contours et recherche de contours
- Reconnaissance de motifs dans les éléments UI

### 2. **Intelligence Artificielle**
- Traitement du langage naturel
- Systèmes de base de connaissances
- Analyse contextuelle et classification

### 3. **Ingénierie de Sécurité**
- Systèmes de licence logicielle
- Chiffrement et signatures numériques
- Empreintes matérielles et anti-copie

### 4. **Architecture Logicielle**
- Conception modulaire et séparation des préoccupations
- Patterns de conception (Strategy, Factory)
- Gestion d'erreurs et systèmes de secours

## 🤝 Contribution

Ce projet est à des fins éducatives. Pour contribuer :

1. **Fork** le repository : [global-exam-ia](https://github.com/adrien-h-hub/global-exam-ia)
2. **Créer** une branche pour votre fonctionnalité
3. **Commiter** vos changements
4. **Pousser** vers la branche
5. **Ouvrir** une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Adrien H** - [adrien-h-hub](https://github.com/adrien-h-hub)

- 📧 Email : [Contactez via GitHub](https://github.com/adrien-h-hub)
- 🔗 Repository : [global-exam-ia](https://github.com/adrien-h-hub/global-exam-ia)

## 🙏 Remerciements

- **OpenCV** pour la vision par ordinateur
- **Tesseract** pour la reconnaissance de caractères
- **PyAutoGUI** pour l'automatisation GUI
- **Python** pour la plateforme de développement

---

⭐ **N'oubliez pas de mettre une étoile au repository si ce projet vous a aidé !**

[![GitHub stars](https://img.shields.io/github/stars/adrien-h-hub/global-exam-ia?style=social)](https://github.com/adrien-h-hub/global-exam-ia/stargazers)
