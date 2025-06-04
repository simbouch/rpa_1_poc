# 🧠 Prototype IA - Extraction automatique de données depuis des documents PDF

Ce projet propose un outil intelligent d'extraction d'informations clés à partir de fichiers PDF à l’aide du traitement automatique du langage (NLP) avec [spaCy](https://spacy.io/) et [pdfplumber](https://github.com/jsvine/pdfplumber). L'application est accessible via une interface simple en [Streamlit](https://streamlit.io/).

---

## 🚀 Fonctionnalités

- 🔍 Extraction automatique des éléments suivants :
  - Nom et prénom
  - Référence de dossier
  - Type d’analyse
  - Date de prélèvement
  - Service demandeur (extrait depuis le texte)

- 📄 Traitement de fichiers PDF multipages
- 🧠 Analyse linguistique avec modèle pré-entraîné `fr_core_news_md` de spaCy
- 💻 Interface interactive Streamlit

---

## 🏗️ Architecture

```
project/
├── extraction.py           # Fonctions d’extraction des informations
├── app.py                  # Interface Streamlit
├── requirements.txt        # Dépendances
└── README.md               # Documentation
```

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/simbouch/rpa_1_poc
cd rpa_1_poc
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 📦 Lancer l’application

```bash
streamlit run app.py
```

---

## 🧪 Exemple d’utilisation

- Déposez un fichier PDF contenant des informations structurées (rapports, comptes rendus, etc.).
- L'application détectera automatiquement les champs importants et vous retournera un dictionnaire JSON exportable.

---

## 📚 Technologies utilisées

- [Python](https://www.python.org/)
- [spaCy](https://spacy.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Streamlit](https://streamlit.io/)

---

## 🛡️ Remarques

Aucune donnée personnelle n’est conservée. Ce projet est fourni à titre de démonstration pour illustrer le potentiel des techniques NLP dans l'automatisation documentaire.

---

## 📄 Licence

Ce projet est sous licence MIT. Vous êtes libre de le modifier, le distribuer et l’utiliser à vos fins.
