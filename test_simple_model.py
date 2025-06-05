#!/usr/bin/env python3
"""
Test simple du modèle entraîné.
"""

import spacy
import os

def test_model_directly():
    """Test le modèle directement."""
    model_path = "training/model_output/model-best"
    
    if not os.path.exists(model_path):
        print("❌ Modèle non trouvé!")
        return
    
    print("🎯 Chargement du modèle entraîné...")
    nlp = spacy.load(model_path)
    
    # Tests simples
    test_texts = [
        "Nom : MARTIN JEAN\nRéférence : 2025-TEST/01-A\nObjet : Test d'analyse\nDate : 15/06/2025\nDemandeur : Service test",
        "Patient : DURAND MARIE\nDossier : 2025-LAB/02-B\nAnalyse : Examen sanguin\nPrélèvement : 20/06/2025\nService : Laboratoire",
        "Nom du patient: BERNARD SOPHIE\nRéf: 2025-HOSP/123-C\nType d'analyse: Analyse toxicologique\nDate de prélèvement: 10.12.2024\nService demandeur: CHU de Paris"
    ]
    
    for i, text in enumerate(test_texts):
        print(f"\n📋 TEST {i+1}:")
        print(f"Texte: {text[:50]}...")
        
        doc = nlp(text)
        print(f"Entités trouvées: {len(doc.ents)}")
        
        for ent in doc.ents:
            print(f"  - {ent.label_}: '{ent.text}' [{ent.start_char}:{ent.end_char}]")
        
        # Vérifier que toutes les entités attendues sont trouvées
        expected_labels = {"nom_personne", "reference_dossier", "type_analyse", "date_prelevement", "service_demandeur"}
        found_labels = {ent.label_ for ent in doc.ents}
        
        missing = expected_labels - found_labels
        if missing:
            print(f"  ⚠️ Labels manquants: {missing}")
        else:
            print(f"  ✅ Tous les labels trouvés!")

if __name__ == "__main__":
    test_model_directly()
