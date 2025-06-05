# 🧠 Prototype IA – Extraction de données depuis des documents PDF

Ce projet propose une application web interactive pour extraire automatiquement des informations clés depuis des rapports PDF à l’aide de techniques de traitement automatique du langage (NLP). L’outil s’appuie sur des modèles spaCy personnalisés ou pré-entraînés, et offre une interface simple grâce à Streamlit.

---

## 🚀 Fonctionnalités principales

- **Sélection du modèle d’extraction**  
  • Choix entre le modèle spaCy par défaut (`fr_core_news_md`) ou un modèle personnalisé entraîné (présent dans `training/model_output/model-best`).  
  • Affichage des informations (version, date de création) du modèle personnalisé lorsqu’il est reconnu.

- **Extraction structurée des champs suivants**  
  • Nom et prénom de la personne  
  • Référence de dossier  
  • Type d’analyse ou de prélèvement  
  • Date de prélèvement  
  • Service demandeur  

- **Affichage et téléchargement des résultats**  
  • Aperçu des champs extraits avec indicateurs de réussite/absence (✔/⚠).  
  • Téléchargement des résultats au format JSON et CSV.  
  • Option d’afficher des métadonnées techniques (méthode d’extraction, nombre de champs détectés, longueur du texte).

- **Traitement de fichiers PDF multipages**  
  • Lecture de tout le contenu d’un PDF via `pdfplumber`.  
  • Passage automatique du texte au pipeline spaCy pour la détection d’entités nommées.

- **Interface ergonomique**  
  • Barre latérale pour la configuration (sélection de modèle, affichage de métadonnées/options).  
  • Colonnes dynamiques pour l’upload, la visualisation des champs et le téléchargement.  
  • Indicateurs de temps de traitement.

---

## 🏗️ Architecture du projet

rpa_1_poc/
├── app.py # Point d’entrée Streamlit
├── extraction_enhanced.py # Classe PDFExtractor et utilitaires
├── requirements.txt # Dépendances Python
├── README.md # Documentation (ce fichier)
│
├── training/ # Entraînement et modèles spaCy NER
│ ├── data/
│ │ ├── raw/ # Rapports PDF bruts à annoter
│ │ └── spacy_format/
│ │ ├── train_data.json # Exemple de données annotées
│ │ └── train_data.spacy # Fichier binaire spaCy pour entraînement
│ ├── config.cfg # Configuration du pipeline spaCy (NER)
│ ├── train.py # Script pour lancer l’entraînement
│ └── model_output/
│ └── model-best/ # Répertoire contenant le modèle entraîné
│
├── data/ # Dossier facultatif pour exemples PDF
└── venv/ # Environnement virtuel (optionnel)

markdown
Copy
Edit

- **app.py** :  
  - Gère l’interface Streamlit (chargement de modèle, upload PDF, affichage des résultats, téléchargement).  
  - Définit la configuration de la page, la sidebar et les colonnes principales.  
- **extraction_enhanced.py** :  
  - Contient la classe `PDFExtractor`, qui encapsule la logique d’extraction : lecture PDF, prétraitement, passage au modèle spaCy, calcul des métadonnées, etc.  
  - La fonction `get_available_models()` liste les chemins des dossiers de modèles valides (modèle personnalisé ou `fr_core_news_md`).  
- **training/** :  
  - Permet de fine-tuner un modèle NER spaCy pour détecter spécifiquement les entités (nom_personne, reference_dossier, type_analyse, date_prelevement, service_demandeur).  
  - Le fichier `train_data.json` regroupe les exemples annotés, et `train_data.spacy` est le format binaire généré par `python -m spacy convert`.  
  - `config.cfg` définit le pipeline spaCy (tok2vec → ner) et les hyperparamètres d’entraînement (seed, dropout, max_epochs, etc.).  
  - `train.py` exécute la commande `spacy train training/config.cfg --output training/model_output`.  
  - Après l’entraînement, le modèle final se trouve dans `training/model_output/model-best`.

---

## ⚙️ Installation

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/simbouch/rpa_1_poc
   cd rpa_1_poc
Créer et activer un environnement virtuel

bash
Copy
Edit
python -m venv venv
# Sous PowerShell (Windows) :
.\venv\Scripts\Activate.ps1
# Sous macOS/Linux :
source venv/bin/activate
Installer les dépendances

bash
Copy
Edit
pip install -r requirements.txt
Télécharger le modèle spaCy français (si nécessaire)

Si fr_core_news_md n’est pas déjà installé via requirements.txt, exécute :

bash
Copy
Edit
python -m spacy download fr_core_news_md
📦 Lancer l’application
Une fois l’environnement activé et les dépendances installées, lance simplement :

bash
Copy
Edit
streamlit run app.py
Le navigateur s’ouvrira automatiquement sur http://localhost:8501/.

Dans la barre latérale, sélectionne le modèle à utiliser et configure les options d’affichage (métadonnées, scores de confiance).

Dans la zone principale, télécharge un fichier PDF à analyser et consulte les résultats.

🧪 Exemples d’utilisation
Sélectionner un modèle

Par défaut, l’application propose le modèle spaCy fr_core_news_md.

Si tu as déjà exécuté un entraînement spaCy dans training/model_output/model-best, tu verras apparaître “🎯 Modèle entraîné (recommandé)”.

Uploader un rapport PDF

Clique sur “Télécharger un rapport PDF” et choisis un fichier PDF.

L’application extrait automatiquement le texte du PDF et passe les données au pipeline NER spaCy.

Consulter les résultats

Les champs extraits s’affichent dans la colonne “Champs extraits”. Chaque champ valide s’accompagne d’une coche verte (✔), sinon d’une alerte jaune (⚠).

Le temps de traitement (en secondes) s’affiche sous le titre “Extraction réussie en X.XX secondes”.

Télécharger les données

Dans “Export des données”, clique sur “Télécharger en JSON” pour obtenir un fichier .json contenant les champs extraits.

Clique sur “Télécharger en CSV” pour obtenir un fichier .csv au format :

rust
Copy
Edit
nom_prenom,BERNARD MICHEL
reference_dossier,2025-GEND/99-X
type_prelevement,Analyse toxicologique sur cheveux
date_prelevement,05/05/2025
service_demandeur,Service régional d'investigation
Afficher les métadonnées

Si l’option “Afficher les métadonnées” est cochée, la section “Métadonnées techniques” affiche :

Méthode d’extraction (IA ou regex mixte)

Nombre de champs détectés par modèle

Nombre de champs détectés par regex

Longueur du texte source (en caractères)

📚 Entraînement du modèle spaCy NER (optionnel)
Si tu souhaites améliorer ou adapter le modèle personnalisé, suis ces étapes :

Préparer des exemples annotés

Place tes rapports PDF dans training/data/raw/.

Extrait manuellement le texte ou utilise pdfplumber pour obtenir le contenu brut.

Crée un fichier JSON train_data.json dans training/data/spacy_format/, au format spaCy :

json
Copy
Edit
[
  [
    "Nom : DUPOND JEAN\nRéférence : 2025-XYZ/01\nObjet : Analyse sanguine\nDate : 10/06/2025\nDemandeur : Service A",
    {
      "entities": [
        [6, 16, "nom_personne"],
        [28, 38, "reference_dossier"],
        [48, 63, "type_analyse"],
        [71, 81, "date_prelevement"],
        [93, 102, "service_demandeur"]
      ]
    }
  ],
  ...
]
Copie/colle ce JSON dans training/data/spacy_format/train_data.json.

Convertir le JSON en .spacy

bash
Copy
Edit
python -m spacy convert training/data/spacy_format/train_data.json training/data/spacy_format --lang fr
→ Génère train_data.spacy.

Modifier (ou vérifier) training/config.cfg

Assure-toi que la clé seed contient bien un entier (ex. seed = 42).

Vérifie que gpu_allocator et gpu_id sont sous [training].

Si tu souhaites un jeu de validation, crée un fichier dev_data.json en suivant la même structure, puis exécute la conversion pour obtenir dev_data.spacy et renseigne dev = "training/data/spacy_format/dev_data.spacy".

Lancer l’entraînement

bash
Copy
Edit
python training/train.py
→ Le modèle final se trouvera dans training/model_output/model-best/.

Tester le modèle

python
Copy
Edit
import spacy

nlp = spacy.load("training/model_output/model-best")
doc = nlp("Nom : LEROY PAUL\nRéférence : 2025-ABC/99\nObjet : Analyse urinaire\nDate : 12/06/2025\nDemandeur : Service B")
for ent in doc.ents:
    print(ent.text, ent.label_)
→ Devrait lister les entités nom_personne, reference_dossier, etc.

📄 Licence
Ce projet est sous licence **MIT