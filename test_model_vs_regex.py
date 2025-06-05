#!/usr/bin/env python3
"""
Test de comparaison entre le modèle entraîné et l'approche regex.
"""

import os
from extraction_enhanced import PDFExtractor

def test_model_performance():
    """Compare les performances du modèle entraîné vs regex."""
    print("🧪 COMPARAISON MODÈLE ENTRAÎNÉ VS REGEX")
    print("=" * 60)
    
    # Test avec différents formats de texte
    test_cases = [
        {
            "name": "Format standard",
            "text": "Nom : MARTIN JEAN\nRéférence : 2025-TEST/01-A\nObjet : Test d'analyse\nDate : 15/06/2025\nDemandeur : Service test"
        },
        {
            "name": "Format alternatif",
            "text": "Patient : DURAND MARIE\nDossier : 2025-LAB/02-B\nAnalyse : Examen sanguin\nPrélèvement : 20/06/2025\nService : Laboratoire"
        },
        {
            "name": "Format avec variations",
            "text": "Nom du patient: BERNARD SOPHIE\nRéf: 2025-HOSP/123-C\nType d'analyse: Analyse toxicologique\nDate de prélèvement: 10.12.2024\nService demandeur: CHU de Paris"
        },
        {
            "name": "Format compact",
            "text": "Identité: GARCIA LUIS | Référence dossier: REF-2025-4567 | Examen: IRM cérébrale | Date: 25/03/2025 | Prescripteur: Service neurologie"
        },
        {
            "name": "Format avec en-tête",
            "text": "RAPPORT D'ANALYSE MEDICALE\n\nNom: PETIT CLAIRE\nN° dossier: BIOL-789456\nAnalyse demandée: Test génétique\nPrélevé le: 18-11-2024\nDemandé par: Laboratoire Pasteur"
        }
    ]
    
    # Créer les extracteurs
    model_path = "training/model_output/model-best"
    if not os.path.exists(model_path):
        print("❌ Modèle entraîné non trouvé!")
        return
    
    print("🎯 Chargement du modèle entraîné...")
    extracteur_trained = PDFExtractor(model_path)
    
    print("📚 Chargement du modèle par défaut...")
    extracteur_default = PDFExtractor(None)
    
    # Tester chaque cas
    results = []
    
    for i, test_case in enumerate(test_cases):
        print(f"\n📋 TEST {i+1}: {test_case['name']}")
        print("-" * 40)
        
        # Créer un fichier temporaire pour le test
        temp_file = f"temp_test_{i}.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(test_case['text'])
        
        try:
            # Test avec modèle entraîné
            print("🎯 Modèle entraîné:")
            result_trained = extracteur_trained.extraire_avec_modele(test_case['text'])
            metadata_trained = {"model_fields": len([v for v in result_trained.values() if v])}
            
            # Test avec regex
            print("🔧 Approche regex:")
            result_regex = extracteur_default.extraire_avec_regex(test_case['text'])
            metadata_regex = {"regex_fields": len([v for v in result_regex.values() if v])}
            
            # Comparer les résultats
            print("\n📊 COMPARAISON:")
            print(f"{'Champ':<20} {'Modèle':<25} {'Regex':<25} {'Gagnant'}")
            print("-" * 80)
            
            fields = ["nom_prenom", "reference_dossier", "type_prelevement", "date_prelevement", "service_demandeur"]
            model_score = 0
            regex_score = 0
            
            for field in fields:
                # Adapter les noms de champs
                model_field = field
                if field == "nom_prenom":
                    model_field = "nom_personne"
                elif field == "type_prelevement":
                    model_field = "type_analyse"
                
                model_val = result_trained.get(model_field, "")
                regex_val = result_regex.get(field, "")
                
                # Déterminer le gagnant
                if model_val and regex_val:
                    winner = "Égalité"
                    model_score += 0.5
                    regex_score += 0.5
                elif model_val and not regex_val:
                    winner = "Modèle"
                    model_score += 1
                elif not model_val and regex_val:
                    winner = "Regex"
                    regex_score += 1
                else:
                    winner = "Aucun"
                
                model_str = (model_val[:20] + "...") if len(str(model_val)) > 23 else str(model_val)
                regex_str = (regex_val[:20] + "...") if len(str(regex_val)) > 23 else str(regex_val)
                
                print(f"{field:<20} {model_str:<25} {regex_str:<25} {winner}")
            
            print("-" * 80)
            print(f"{'SCORE TOTAL':<20} {model_score:<25} {regex_score:<25}")
            
            results.append({
                "test": test_case['name'],
                "model_score": model_score,
                "regex_score": regex_score,
                "model_fields": metadata_trained["model_fields"],
                "regex_fields": metadata_regex["regex_fields"]
            })
            
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
        
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 60)
    
    total_model_score = sum(r["model_score"] for r in results)
    total_regex_score = sum(r["regex_score"] for r in results)
    total_model_fields = sum(r["model_fields"] for r in results)
    total_regex_fields = sum(r["regex_fields"] for r in results)
    
    print(f"Score total modèle: {total_model_score}")
    print(f"Score total regex: {total_regex_score}")
    print(f"Champs trouvés modèle: {total_model_fields}")
    print(f"Champs trouvés regex: {total_regex_fields}")
    
    if total_model_score > total_regex_score:
        print("\n🏆 GAGNANT: MODÈLE ENTRAÎNÉ!")
        print("Le modèle entraîné surpasse l'approche regex.")
    elif total_regex_score > total_model_score:
        print("\n🏆 GAGNANT: APPROCHE REGEX!")
        print("L'approche regex surpasse le modèle entraîné.")
    else:
        print("\n🤝 ÉGALITÉ!")
        print("Les deux approches sont équivalentes.")
    
    # Test avec un vrai fichier PDF si disponible
    print("\n" + "=" * 60)
    print("📄 TEST AVEC FICHIER PDF RÉEL")
    print("=" * 60)
    
    test_files = ["exemple_rapport.pdf", "rapport_analyse_complet.pdf", "rapport_long_etendu.pdf"]
    test_file = None
    
    for file in test_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if test_file:
        print(f"📄 Test avec {test_file}")
        
        try:
            # Test avec modèle entraîné
            result_trained_pdf = extracteur_trained.extraire_infos(test_file)
            metadata_trained_pdf = result_trained_pdf.pop("_metadata", {})
            
            # Test avec regex seulement
            result_regex_pdf = extracteur_default.extraire_infos(test_file)
            metadata_regex_pdf = result_regex_pdf.pop("_metadata", {})
            
            print("\n📊 Résultats PDF:")
            print(f"Modèle entraîné - Méthode: {metadata_trained_pdf.get('extraction_method', 'N/A')}")
            print(f"Modèle entraîné - Champs: {sum(1 for v in result_trained_pdf.values() if v)}")
            print(f"Regex - Champs: {sum(1 for v in result_regex_pdf.values() if v)}")
            
            # Afficher les différences
            print("\n🔍 Comparaison détaillée:")
            for field in result_trained_pdf.keys():
                trained_val = result_trained_pdf.get(field, "")
                regex_val = result_regex_pdf.get(field, "")
                
                if trained_val != regex_val:
                    print(f"  {field}:")
                    print(f"    Modèle: {trained_val}")
                    print(f"    Regex:  {regex_val}")
            
        except Exception as e:
            print(f"❌ Erreur lors du test PDF: {e}")
    else:
        print("❌ Aucun fichier PDF de test trouvé")

if __name__ == "__main__":
    test_model_performance()
