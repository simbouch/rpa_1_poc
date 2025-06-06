#!/usr/bin/env python3
"""
Générateur de données synthétiques spécialisées pour les rapports médicaux.
Crée un modèle spécialisé pour les documents médicaux.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class MedicalDataGenerator:
    """Générateur de données d'entraînement pour rapports médicaux."""
    
    def __init__(self):
        # Noms médicaux spécialisés
        self.noms_medicaux = [
            "MARTIN", "BERNARD", "THOMAS", "PETIT", "ROBERT", "RICHARD", "DURAND", "DUBOIS",
            "MOREAU", "LAURENT", "SIMON", "MICHEL", "LEFEBVRE", "LEROY", "ROUX", "DAVID",
            "BERTRAND", "MOREL", "FOURNIER", "GIRARD", "BONNET", "DUPONT", "LAMBERT", "FONTAINE"
        ]
        
        self.prenoms_medicaux = [
            "JEAN", "MARIE", "PIERRE", "MICHEL", "ANDRE", "PHILIPPE", "ALAIN", "BERNARD",
            "CHRISTOPHE", "PATRICK", "NICOLAS", "JACQUES", "DANIEL", "FRANCOIS", "ERIC", "LAURENT",
            "SYLVIE", "NATHALIE", "ISABELLE", "CATHERINE", "CHRISTINE", "SANDRINE", "VALERIE"
        ]
        
        # Préfixes médicaux spécialisés
        self.prefixes_medicaux = {
            "nom_personne": [
                "Patient :", "Nom du patient :", "Identité :", "Malade :", "Personne examinée :",
                "Nom :", "Sujet :", "Individu :", "Bénéficiaire :", "Nom et prénom :"
            ],
            "reference_dossier": [
                "N° dossier médical :", "Dossier patient :", "IPP :", "N° séjour :", "Référence hospitalière :",
                "ID patient :", "Numéro de dossier :", "Dossier :", "N° :", "Référence :"
            ],
            "type_analyse": [
                "Examen :", "Analyse :", "Diagnostic :", "Investigation :", "Procédure :",
                "Test :", "Bilan :", "Exploration :", "Contrôle :", "Évaluation :"
            ],
            "date_prelevement": [
                "Date d'examen :", "Date de consultation :", "Réalisé le :", "Date :", "Effectué le :",
                "Date de prélèvement :", "Date d'intervention :", "Examiné le :", "Date du test :"
            ],
            "service_demandeur": [
                "Service :", "Unité :", "Département :", "Prescripteur :", "Médecin traitant :",
                "Service demandeur :", "Spécialité :", "Équipe médicale :", "Praticien :"
            ]
        }
        
        # Analyses médicales spécialisées
        self.analyses_medicales = [
            "Bilan sanguin complet", "Échographie abdominale", "Scanner thoracique",
            "IRM cérébrale", "Électrocardiogramme", "Radiographie pulmonaire",
            "Analyse d'urine", "Bilan lipidique", "Glycémie à jeun", "Test de fonction hépatique",
            "Analyse rénale", "Bilan thyroïdien", "Mammographie", "Coloscopie",
            "Endoscopie digestive", "Biopsie cutanée", "Ponction lombaire",
            "Test d'effort cardiaque", "Holter ECG 24h", "Spirométrie",
            "Densitométrie osseuse", "Scintigraphie", "Artériographie",
            "Échographie cardiaque", "Doppler vasculaire", "EEG",
            "EMG", "Fibroscopie bronchique", "Cystoscopie",
            "Arthroscopie", "Coronarographie", "Angiographie"
        ]
        
        # Services médicaux
        self.services_medicaux = [
            "Cardiologie", "Neurologie", "Gastro-entérologie", "Pneumologie",
            "Rhumatologie", "Endocrinologie", "Néphrologie", "Hématologie",
            "Oncologie", "Dermatologie", "Ophtalmologie", "ORL",
            "Gynécologie", "Urologie", "Orthopédie", "Chirurgie générale",
            "Anesthésie", "Radiologie", "Médecine interne", "Gériatrie",
            "Pédiatrie", "Psychiatrie", "Médecine d'urgence", "Réanimation",
            "Laboratoire de biologie", "Anatomie pathologique", "Médecine nucléaire"
        ]
    
    def generate_medical_reference(self) -> str:
        """Génère une référence médicale."""
        year = random.randint(2020, 2025)
        patterns = [
            f"IPP{random.randint(100000, 999999)}",
            f"MED-{year}-{random.randint(1000, 9999)}",
            f"PAT{random.randint(10000, 99999)}",
            f"HOSP/{year}/{random.randint(100, 999)}",
            f"CHU-{random.randint(100000, 999999)}",
            f"DOS{year}{random.randint(1000, 9999)}",
            f"REF-MED-{random.randint(100000, 999999)}",
            f"DOSS-{year}-{random.randint(1, 999):03d}"
        ]
        return random.choice(patterns)
    
    def generate_medical_date(self) -> str:
        """Génère une date médicale."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2025, 12, 31)
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %m %Y"]
        return random_date.strftime(random.choice(formats))
    
    def generate_medical_name(self) -> str:
        """Génère un nom médical."""
        nom = random.choice(self.noms_medicaux)
        prenom = random.choice(self.prenoms_medicaux)
        
        patterns = [f"{nom} {prenom}", f"{prenom} {nom}", f"{nom}, {prenom}"]
        return random.choice(patterns)
    
    def create_medical_example(self) -> Tuple[str, Dict]:
        """Crée un exemple médical."""
        nom = self.generate_medical_name()
        reference = self.generate_medical_reference()
        analyse = random.choice(self.analyses_medicales)
        date = self.generate_medical_date()
        service = random.choice(self.services_medicaux)
        
        # Choisir les préfixes
        prefix_nom = random.choice(self.prefixes_medicaux["nom_personne"])
        prefix_ref = random.choice(self.prefixes_medicaux["reference_dossier"])
        prefix_analyse = random.choice(self.prefixes_medicaux["type_analyse"])
        prefix_date = random.choice(self.prefixes_medicaux["date_prelevement"])
        prefix_service = random.choice(self.prefixes_medicaux["service_demandeur"])
        
        # Construire le texte médical
        separators = ["\n", "\n\n", " | ", "\t"]
        separator = random.choice(separators)
        
        fields = [
            (prefix_nom, nom, "nom_personne"),
            (prefix_ref, reference, "reference_dossier"),
            (prefix_analyse, analyse, "type_analyse"),
            (prefix_date, date, "date_prelevement"),
            (prefix_service, service, "service_demandeur")
        ]
        
        # Parfois mélanger l'ordre
        if random.random() < 0.3:
            random.shuffle(fields)
        
        text_parts = []
        entities = []
        current_pos = 0
        
        # Ajouter un en-tête médical parfois
        if random.random() < 0.4:
            headers = [
                "COMPTE RENDU MÉDICAL\n\n",
                "RAPPORT D'EXAMEN\n\n", 
                "CENTRE HOSPITALIER UNIVERSITAIRE\n\n",
                "RÉSULTATS D'ANALYSE MÉDICALE\n\n",
                "DOSSIER PATIENT\n\n",
                ""
            ]
            header = random.choice(headers)
            text_parts.append(header)
            current_pos += len(header)
        
        for i, (prefix, value, label) in enumerate(fields):
            if i > 0:
                text_parts.append(separator)
                current_pos += len(separator)
            
            text_parts.append(prefix)
            current_pos += len(prefix)
            
            if not prefix.endswith(" "):
                text_parts.append(" ")
                current_pos += 1
            
            start_pos = current_pos
            text_parts.append(value)
            end_pos = current_pos + len(value)
            current_pos = end_pos
            
            entities.append([start_pos, end_pos, label])
        
        # Ajouter une conclusion médicale parfois
        if random.random() < 0.3:
            footers = [
                "\n\nRapport validé par le médecin",
                "\n\nDocument confidentiel",
                "\n\nFin du compte rendu",
                ""
            ]
            footer = random.choice(footers)
            text_parts.append(footer)
        
        text = "".join(text_parts)
        annotations = {"entities": entities}
        
        return text, annotations
    
    def generate_medical_dataset(self, num_examples: int = 300) -> List[Tuple[str, Dict]]:
        """Génère un dataset médical."""
        dataset = []
        print(f"Génération de {num_examples} exemples médicaux...")
        
        for i in range(num_examples):
            try:
                example = self.create_medical_example()
                dataset.append(example)
                
                if (i + 1) % 50 == 0:
                    print(f"✅ {i + 1}/{num_examples} exemples médicaux générés")
            except Exception as e:
                print(f"⚠️ Erreur exemple {i}: {e}")
        
        print(f"🏥 Dataset médical généré: {len(dataset)} exemples")
        return dataset
    
    def save_medical_dataset(self, dataset: List[Tuple[str, Dict]], output_path: str):
        """Sauvegarde le dataset médical."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            print(f"💾 Dataset médical sauvegardé: {output_path}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")

def main():
    """Génère le dataset médical."""
    print("🏥 Génération de données médicales spécialisées")
    print("=" * 50)
    
    generator = MedicalDataGenerator()
    dataset = generator.generate_medical_dataset(num_examples=300)
    
    # Sauvegarder
    output_path = "training/data/medical_format/train_data.json"
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generator.save_medical_dataset(dataset, output_path)
    
    print("\n📊 Exemples générés:")
    for i, (text, annotations) in enumerate(dataset[:2]):
        print(f"\nExemple médical {i+1}:")
        print(f"Texte: {text[:80]}...")
        print(f"Entités: {len(annotations['entities'])}")

if __name__ == "__main__":
    main()
