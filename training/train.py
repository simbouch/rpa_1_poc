#!/usr/bin/env python3
"""
Script d'entraînement amélioré pour le modèle spaCy NER.
Inclut la préparation des données, l'entraînement et l'évaluation.
"""

import subprocess
import sys
import os
import logging
import json
from pathlib import Path
import spacy
import time

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training/training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées."""
    try:
        import spacy
        spacy.load("fr_core_news_md")
        logger.info("✅ spaCy et fr_core_news_md disponibles")
        return True
    except Exception as e:
        logger.error(f"❌ Dépendances manquantes: {e}")
        return False

def prepare_training_data():
    """Prépare les données d'entraînement en convertissant le JSON en format spaCy."""
    logger.info("🔄 Préparation des données d'entraînement...")

    # Importer et exécuter le script de conversion
    try:
        from training.scripts.convert_data import main as convert_main
        convert_main()
        logger.info("✅ Données d'entraînement préparées")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur lors de la préparation des données: {e}")
        return False

def validate_config(config_path: str):
    """Valide le fichier de configuration."""
    if not os.path.exists(config_path):
        logger.error(f"❌ Fichier de configuration non trouvé: {config_path}")
        return False

    # Vérifier que les fichiers de données existent
    train_data_path = "training/data/spacy_format/train_data.spacy"
    if not os.path.exists(train_data_path):
        logger.error(f"❌ Fichier de données d'entraînement non trouvé: {train_data_path}")
        return False

    logger.info("✅ Configuration validée")
    return True

def train_spacy_model(config_path: str):
    """
    Lance l'entraînement spaCy NER à partir du fichier de config spécifié.
    """
    output_dir = "training/model_output"

    # Créer le dossier de sortie
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable, "-m", "spacy", "train", config_path,
        "--output", output_dir,
        "--verbose"
    ]

    logger.info("🛠️ Démarrage de l'entraînement spaCy NER...")
    logger.info(f"Commande: {' '.join(command)}")

    start_time = time.time()

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info("✅ Entraînement terminé avec succès")
        logger.info(f"Sortie: {result.stdout}")

        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"⏱️ Durée d'entraînement: {duration:.2f} secondes")

        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors de l'entraînement: {e}")
        logger.error(f"Sortie d'erreur: {e.stderr}")
        return False

def evaluate_model():
    """Évalue le modèle entraîné."""
    model_path = "training/model_output/model-best"

    if not os.path.exists(model_path):
        logger.error(f"❌ Modèle non trouvé: {model_path}")
        return False

    try:
        logger.info("🔍 Évaluation du modèle...")

        # Charger le modèle
        nlp = spacy.load(model_path)

        # Test simple avec des exemples
        test_texts = [
            "Nom : MARTIN JEAN\nRéférence : 2025-TEST/01-A\nObjet : Test d'analyse\nDate : 15/06/2025\nDemandeur : Service test",
            "Patient : DURAND MARIE\nDossier : 2025-LAB/02-B\nAnalyse : Examen sanguin\nPrélèvement : 20/06/2025\nService : Laboratoire"
        ]

        for i, text in enumerate(test_texts):
            doc = nlp(text)
            logger.info(f"Test {i+1}: {len(doc.ents)} entités détectées")
            for ent in doc.ents:
                logger.info(f"  - {ent.text} ({ent.label_})")

        logger.info("✅ Évaluation terminée")
        return True

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'évaluation: {e}")
        return False

def create_model_info():
    """Crée un fichier d'information sur le modèle."""
    info = {
        "model_name": "pdf_extraction_ner",
        "version": "1.0.0",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "labels": ["nom_personne", "reference_dossier", "type_analyse", "date_prelevement", "service_demandeur"],
        "description": "Modèle NER pour l'extraction d'informations depuis des rapports PDF"
    }

    info_path = "training/model_output/model_info.json"
    try:
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Informations du modèle sauvegardées: {info_path}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la sauvegarde des infos: {e}")

def main():
    """Fonction principale d'entraînement."""
    logger.info("🚀 Démarrage du processus d'entraînement complet")

    # 1. Vérifier les dépendances
    if not check_dependencies():
        logger.error("❌ Dépendances manquantes. Arrêt du processus.")
        return False

    # 2. Préparer les données
    if not prepare_training_data():
        logger.error("❌ Échec de la préparation des données. Arrêt du processus.")
        return False

    # 3. Valider la configuration
    config_path = "training/config.cfg"
    if not validate_config(config_path):
        logger.error("❌ Configuration invalide. Arrêt du processus.")
        return False

    # 4. Entraîner le modèle
    if not train_spacy_model(config_path):
        logger.error("❌ Échec de l'entraînement. Arrêt du processus.")
        return False

    # 5. Évaluer le modèle
    if not evaluate_model():
        logger.warning("⚠️ Échec de l'évaluation, mais le modèle a été créé.")

    # 6. Créer les informations du modèle
    create_model_info()

    logger.info("🎉 Processus d'entraînement terminé avec succès!")
    logger.info("📁 Le modèle se trouve dans: training/model_output/model-best")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
