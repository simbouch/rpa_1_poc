#!/usr/bin/env python3
"""
Script d'entraînement simple et direct pour le modèle NER.
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch
import random
import json
from pathlib import Path

def load_training_data():
    """Charge les données d'entraînement."""
    with open("training/data/spacy_format/train_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"✅ Chargé {len(data)} exemples d'entraînement")
    return data

def create_examples(nlp, data):
    """Crée des exemples spaCy à partir des données JSON."""
    examples = []
    
    for text, annotations in data:
        doc = nlp.make_doc(text)
        entities = annotations["entities"]
        
        # Filtrer les entités valides
        valid_entities = []
        for start, end, label in entities:
            if start < end and end <= len(text):
                valid_entities.append((start, end, label))
        
        if valid_entities:
            example = Example.from_dict(doc, {"entities": valid_entities})
            examples.append(example)
    
    print(f"✅ Créé {len(examples)} exemples valides")
    return examples

def train_model():
    """Entraîne le modèle NER."""
    print("🚀 Démarrage de l'entraînement simple")
    
    # Charger le modèle de base
    nlp = spacy.load("fr_core_news_md")
    
    # Ajouter le composant NER s'il n'existe pas
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")
    
    # Charger les données
    data = load_training_data()
    
    # Ajouter les labels
    labels = ["nom_personne", "reference_dossier", "type_analyse", "date_prelevement", "service_demandeur"]
    for label in labels:
        ner.add_label(label)
    
    # Créer les exemples
    examples = create_examples(nlp, data)
    
    # Diviser en train/dev
    random.shuffle(examples)
    split_idx = int(len(examples) * 0.8)
    train_examples = examples[:split_idx]
    dev_examples = examples[split_idx:]
    
    print(f"📊 Division: {len(train_examples)} entraînement, {len(dev_examples)} validation")
    
    # Désactiver les autres composants pendant l'entraînement
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    # Entraînement
    print("🔄 Début de l'entraînement...")
    
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        
        for epoch in range(50):  # 50 époques
            print(f"Époque {epoch + 1}/50")
            
            # Mélanger les données
            random.shuffle(train_examples)
            losses = {}
            
            # Entraînement par mini-batches
            for batch in minibatch(train_examples, size=8):
                nlp.update(batch, drop=0.2, losses=losses, sgd=optimizer)
            
            # Évaluation tous les 10 époques
            if (epoch + 1) % 10 == 0:
                print(f"  Perte NER: {losses.get('ner', 0):.2f}")
                
                # Évaluation simple
                correct = 0
                total = 0
                
                for example in dev_examples[:20]:  # Tester sur 20 exemples
                    doc = nlp(example.reference.text)
                    predicted_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
                    gold_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in example.reference.ents]
                    
                    for pred_ent in predicted_entities:
                        if pred_ent in gold_entities:
                            correct += 1
                    total += len(gold_entities)
                
                accuracy = correct / total if total > 0 else 0
                print(f"  Précision: {accuracy:.2f} ({correct}/{total})")
    
    # Sauvegarder le modèle
    output_dir = Path("training/model_output/model-best")
    output_dir.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    
    print(f"✅ Modèle sauvegardé dans {output_dir}")
    
    # Test final
    print("\n🧪 Test final du modèle:")
    test_texts = [
        "Nom : MARTIN JEAN\nRéférence : 2025-TEST/01-A\nObjet : Test d'analyse\nDate : 15/06/2025\nDemandeur : Service test",
        "Patient : DURAND MARIE\nDossier : 2025-LAB/02-B\nAnalyse : Examen sanguin\nPrélèvement : 20/06/2025\nService : Laboratoire"
    ]
    
    for i, text in enumerate(test_texts):
        print(f"\nTest {i+1}:")
        doc = nlp(text)
        print(f"Texte: {text[:50]}...")
        print(f"Entités trouvées: {len(doc.ents)}")
        for ent in doc.ents:
            print(f"  - {ent.label_}: '{ent.text}'")

if __name__ == "__main__":
    train_model()
