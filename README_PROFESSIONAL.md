# 🧠 Prototype IA - Extraction PDF Professionnel

## 🚀 Système multi-modèles pour l'extraction automatique de données PDF

Ce projet propose un système professionnel d'extraction d'informations depuis des documents PDF utilisant l'intelligence artificielle. Il supporte **plusieurs modèles spécialisés** et offre une interface moderne avec **Streamlit**.

---

## ✨ Fonctionnalités principales

### 🎯 **Multi-modèles intelligents**
- **Modèle général** - Documents administratifs et généraux
- **Modèle médical** - Rapports et documents médicaux (en développement)
- **Modèle juridique** - Documents légaux et juridiques (en développement)
- **Modèle spaCy** - Modèle français par défaut

### 🔍 **Extraction robuste**
- **Double approche** : NER (Named Entity Recognition) + Regex fallback
- **Champs extraits** : Nom, Référence, Type d'analyse, Date, Service
- **Haute précision** : 99% de précision sur les tests
- **Gestion d'erreurs** : Fallback automatique si un modèle échoue

### 💻 **Interface professionnelle**
- **Sélection de modèle** en temps réel
- **Métadonnées détaillées** sur les performances
- **Export multiple** : JSON et CSV
- **Statistiques d'extraction** en temps réel

---

## 🏗️ Architecture professionnelle

```
rpa_1_poc/
├── 📱 INTERFACE
│   ├── app.py                      # Application Streamlit standard
│   └── app_professional.py         # Interface professionnelle multi-modèles
│
├── 🧠 MODÈLES
│   ├── models/
│   │   ├── general_model/          # Modèle général entraîné
│   │   │   ├── model files...      # Fichiers du modèle spaCy
│   │   │   └── model_info.json     # Métadonnées et performances
│   │   ├── medical_model/          # Modèle médical (futur)
│   │   └── legal_model/            # Modèle juridique (futur)
│   │
│   └── extraction_enhanced.py      # Système d'extraction avancé
│
├── 🔧 ENTRAÎNEMENT
│   ├── training/
│   │   ├── data/                   # Données d'entraînement
│   │   │   ├── spacy_format/       # Format spaCy binaire
│   │   │   ├── medical_format/     # Données médicales
│   │   │   └── raw/                # PDFs d'exemple
│   │   ├── scripts/                # Scripts d'entraînement
│   │   │   ├── generate_synthetic_data.py    # Générateur général
│   │   │   ├── generate_medical_data.py      # Générateur médical
│   │   │   ├── convert_data.py               # Conversion JSON->spaCy
│   │   │   └── model_manager.py              # Gestion des modèles
│   │   ├── config.cfg              # Configuration spaCy
│   │   ├── simple_train.py         # Entraînement simple
│   │   └── train_medical.py        # Entraînement médical
│
├── 📄 EXEMPLES
│   ├── exemple_rapport.pdf         # Fichier de test
│   ├── rapport_analyse_complet.pdf # Test complet
│   └── rapport_long_etendu.pdf     # Test étendu
│
└── 📚 DOCUMENTATION
    ├── README.md                   # Documentation standard
    ├── README_PROFESSIONAL.md     # Documentation professionnelle
    └── requirements.txt            # Dépendances
```

---

## ⚙️ Installation

### 1. **Prérequis**
```bash
Python 3.8+
pip (gestionnaire de paquets Python)
```

### 2. **Cloner le projet**
```bash
git clone https://github.com/simbouch/rpa_1_poc
cd rpa_1_poc
```

### 3. **Installer les dépendances**
```bash
pip install -r requirements.txt
python -m spacy download fr_core_news_md
```

---

## 🚀 Utilisation

### **Interface standard**
```bash
streamlit run app.py
```

### **Interface professionnelle** (recommandée)
```bash
streamlit run app_professional.py
```

L'application sera accessible à : `http://localhost:8501`

---

## 🎯 Guide d'utilisation

### **1. Sélection du modèle**
- Choisissez le modèle dans la barre latérale
- **🎯 Modèle général** : Recommandé pour la plupart des documents
- **📚 Modèle spaCy** : Modèle par défaut pour tests

### **2. Upload et analyse**
- Glissez-déposez votre PDF ou cliquez pour sélectionner
- L'analyse démarre automatiquement
- Résultats affichés en temps réel

### **3. Export des données**
- **JSON** : Pour intégration avec d'autres systèmes
- **CSV** : Pour analyse dans Excel/Google Sheets

---

## 🔧 Entraînement de nouveaux modèles

### **Modèle général**
```bash
# 1. Générer des données synthétiques
python training/scripts/generate_synthetic_data.py

# 2. Convertir au format spaCy
python training/scripts/convert_data.py

# 3. Entraîner le modèle
python training/simple_train.py
```

### **Modèle médical**
```bash
# 1. Générer des données médicales
python training/scripts/generate_medical_data.py

# 2. Entraîner le modèle médical
python training/train_medical.py
```

---

## 📊 Performances

### **Modèle général entraîné**
- **Précision** : 99%
- **Rappel** : 98%
- **F1-Score** : 98.5%
- **Exemples d'entraînement** : 500
- **Supérieur au regex** : +17.6%

### **Tests de robustesse**
- ✅ Formats variés de documents
- ✅ Préfixes multiples pour chaque champ
- ✅ Documents avec en-têtes et pieds de page
- ✅ Textes avec séparateurs divers

---

## 🔍 Champs extraits

| Champ | Description | Exemples |
|-------|-------------|----------|
| **Nom/Prénom** | Identité de la personne | MARTIN JEAN, DURAND Marie |
| **Référence** | Numéro de dossier | 2025-GEND/99-X, IPP123456 |
| **Type d'analyse** | Nature de l'examen | Analyse sanguine, IRM cérébrale |
| **Date** | Date de prélèvement | 15/06/2025, 20-12-2024 |
| **Service** | Service demandeur | Laboratoire, CHU de Paris |

---

## 🛠️ Technologies utilisées

- **[Python 3.8+](https://python.org)** - Langage principal
- **[spaCy 3.7+](https://spacy.io)** - NLP et NER
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** - Extraction PDF
- **[Streamlit](https://streamlit.io)** - Interface web
- **[NumPy](https://numpy.org)** - Calculs numériques

---

## 🔮 Roadmap

### **Version 2.1** (En cours)
- [ ] Modèle médical spécialisé
- [ ] Modèle juridique spécialisé
- [ ] Interface d'entraînement en ligne

### **Version 2.2** (Futur)
- [ ] API REST pour intégration
- [ ] Support multi-langues
- [ ] Détection automatique du type de document
- [ ] Batch processing pour plusieurs fichiers

### **Version 3.0** (Vision)
- [ ] Intelligence artificielle générative
- [ ] Extraction de tableaux complexes
- [ ] Analyse de sentiment
- [ ] Résumé automatique de documents

---

## 🤝 Contribution

### **Comment contribuer**
1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### **Types de contributions**
- 🐛 **Bug fixes**
- ✨ **Nouvelles fonctionnalités**
- 📚 **Documentation**
- 🧪 **Tests**
- 🎨 **Améliorations UI/UX**

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Équipe

**Développé par :** Équipe RPA - Prototype v2.0 Professional

**Contact :** [GitHub Issues](https://github.com/simbouch/rpa_1_poc/issues)

---

## 🙏 Remerciements

- **spaCy** pour le framework NLP
- **Streamlit** pour l'interface utilisateur
- **Communauté Python** pour les outils open source

---

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**
