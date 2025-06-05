#!/usr/bin/env python3
"""
Script pour convertir les données d'entraînement JSON en format spaCy binaire.
"""

import json
import spacy
from spacy.tokens import DocBin
from spacy.training import Example
import random
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_json_data(json_path: str):
    """Charge les données d'entraînement depuis un fichier JSON."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"✅ Chargé {len(data)} exemples depuis {json_path}")
        return data
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement de {json_path}: {e}")
        raise

def validate_training_data(data):
    """Valide la structure des données d'entraînement."""
    valid_labels = {"nom_personne", "reference_dossier", "type_analyse", "date_prelevement", "service_demandeur"}
    
    for i, (text, annotations) in enumerate(data):
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"Exemple {i}: Le texte doit être une chaîne non vide")
        
        if "entities" not in annotations:
            raise ValueError(f"Exemple {i}: 'entities' manquant dans les annotations")
        
        entities = annotations["entities"]
        for j, (start, end, label) in enumerate(entities):
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError(f"Exemple {i}, entité {j}: start et end doivent être des entiers")
            
            if start >= end:
                raise ValueError(f"Exemple {i}, entité {j}: start ({start}) doit être < end ({end})")
            
            if end > len(text):
                raise ValueError(f"Exemple {i}, entité {j}: end ({end}) dépasse la longueur du texte ({len(text)})")
            
            if label not in valid_labels:
                logger.warning(f"Exemple {i}, entité {j}: Label '{label}' non reconnu")
    
    logger.info("✅ Validation des données réussie")

def create_spacy_examples(nlp, data):
    """Convertit les données JSON en exemples spaCy."""
    examples = []

    for i, (text, annotations) in enumerate(data):
        try:
            doc = nlp.make_doc(text)
            entities = annotations["entities"]

            # Trier les entités par position pour éviter les chevauchements
            entities = sorted(entities, key=lambda x: (x[0], x[1]))

            # Filtrer les entités qui se chevauchent
            filtered_entities = []
            for start, end, label in entities:
                # Vérifier qu'il n'y a pas de chevauchement avec les entités précédentes
                overlap = False
                for prev_start, prev_end, _ in filtered_entities:
                    if not (end <= prev_start or start >= prev_end):
                        overlap = True
                        break

                if not overlap and start < end and end <= len(text):
                    filtered_entities.append((start, end, label))

            # Créer les spans d'entités
            spans = []
            for start, end, label in filtered_entities:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    # Essayer avec un mode d'alignement différent
                    span = doc.char_span(start, end, label=label, alignment_mode="expand")
                    if span is None:
                        logger.warning(f"Impossible de créer un span pour '{text[start:end]}' ({start}-{end})")
                        continue
                spans.append(span)

            # Créer le doc avec les entités (seulement si on a des spans valides)
            if spans:
                doc.ents = spans
                example = Example.from_dict(doc, {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]})
                examples.append(example)
            else:
                logger.warning(f"Exemple {i} ignoré: aucun span valide")

        except Exception as e:
            logger.warning(f"Erreur lors du traitement de l'exemple {i}: {e}")
            continue

    logger.info(f"✅ Créé {len(examples)} exemples spaCy valides")
    return examples

def split_data(examples, train_ratio=0.8):
    """Divise les données en ensembles d'entraînement et de validation."""
    random.shuffle(examples)
    split_idx = int(len(examples) * train_ratio)
    
    train_examples = examples[:split_idx]
    dev_examples = examples[split_idx:]
    
    logger.info(f"✅ Division: {len(train_examples)} entraînement, {len(dev_examples)} validation")
    return train_examples, dev_examples

def save_spacy_data(examples, output_path):
    """Sauvegarde les exemples au format spaCy binaire."""
    doc_bin = DocBin()
    
    for example in examples:
        doc_bin.add(example.reference)
    
    doc_bin.to_disk(output_path)
    logger.info(f"✅ Données sauvegardées dans {output_path}")

def augment_data(data, num_augmentations=0):
    """Désactive l'augmentation pour éviter les problèmes de spans."""
    # Désactiver l'augmentation pour l'instant car elle cause des problèmes
    logger.info(f"✅ Données conservées sans augmentation: {len(data)} exemples")
    return data

def main():
    """Fonction principale de conversion des données."""
    # Chemins
    json_path = "training/data/spacy_format/train_data.json"
    train_output = "training/data/spacy_format/train_data.spacy"
    dev_output = "training/data/spacy_format/dev_data.spacy"
    
    # Créer les dossiers si nécessaire
    Path(train_output).parent.mkdir(parents=True, exist_ok=True)
    
    # Charger le modèle spaCy
    try:
        nlp = spacy.load("fr_core_news_md")
        logger.info("✅ Modèle fr_core_news_md chargé")
    except OSError:
        logger.error("❌ Modèle fr_core_news_md non trouvé. Installez-le avec: python -m spacy download fr_core_news_md")
        return
    
    # Charger et valider les données
    data = load_json_data(json_path)
    validate_training_data(data)
    
    # Augmenter les données
    augmented_data = augment_data(data, num_augmentations=3)
    
    # Convertir en exemples spaCy
    examples = create_spacy_examples(nlp, augmented_data)
    
    # Diviser les données
    train_examples, dev_examples = split_data(examples, train_ratio=0.8)
    
    # Sauvegarder
    save_spacy_data(train_examples, train_output)
    save_spacy_data(dev_examples, dev_output)
    
    logger.info("🎉 Conversion terminée avec succès!")
    logger.info(f"📊 Statistiques finales:")
    logger.info(f"   - Entraînement: {len(train_examples)} exemples")
    logger.info(f"   - Validation: {len(dev_examples)} exemples")

if __name__ == "__main__":
    main()
