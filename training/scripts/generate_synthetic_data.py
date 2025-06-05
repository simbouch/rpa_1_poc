#!/usr/bin/env python3
"""
Générateur de données synthétiques pour améliorer le modèle NER.
Crée des centaines d'exemples variés pour un entraînement robuste.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import re

class SyntheticDataGenerator:
    """Générateur de données d'entraînement synthétiques avancé."""
    
    def __init__(self):
        # Noms de famille français
        self.noms = [
            "MARTIN", "BERNARD", "THOMAS", "PETIT", "ROBERT", "RICHARD", "DURAND", "DUBOIS",
            "MOREAU", "LAURENT", "SIMON", "MICHEL", "LEFEBVRE", "LEROY", "ROUX", "DAVID",
            "BERTRAND", "MOREL", "FOURNIER", "GIRARD", "BONNET", "DUPONT", "LAMBERT", "FONTAINE",
            "ROUSSEAU", "VINCENT", "MULLER", "LEFEVRE", "FAURE", "ANDRE", "MERCIER", "BLANC",
            "GUERIN", "BOYER", "GARNIER", "CHEVALIER", "FRANCOIS", "LEGRAND", "GAUTHIER", "GARCIA",
            "PERRIN", "ROBIN", "CLEMENT", "MORIN", "NICOLAS", "HENRY", "ROUSSEL", "MATHIEU",
            "GAUTIER", "MASSON", "MARCHAND", "DUVAL", "DENIS", "DUMONT", "MARIE", "LEMAIRE",
            "NOEL", "MEYER", "DUFOUR", "MEUNIER", "BRUN", "BLANCHARD", "GIRAUD", "JOLY",
            "RIVIERE", "LUCAS", "BRUNET", "GAILLARD", "BARBIER", "ARNAUD", "MARTINEZ", "GERARD",
            "ROCHE", "RENARD", "SCHMITT", "ROY", "LEROUX", "COLIN", "VIDAL", "CARON"
        ]
        
        # Prénoms français
        self.prenoms = [
            "JEAN", "MARIE", "PIERRE", "MICHEL", "ANDRE", "PHILIPPE", "ALAIN", "BERNARD",
            "CHRISTOPHE", "PATRICK", "NICOLAS", "JACQUES", "DANIEL", "FRANCOIS", "ERIC", "LAURENT",
            "OLIVIER", "SEBASTIEN", "JULIEN", "DAVID", "STEPHANE", "PASCAL", "FABRICE", "JEROME",
            "SYLVIE", "NATHALIE", "ISABELLE", "CATHERINE", "CHRISTINE", "SANDRINE", "VALERIE", "KARINE",
            "VERONIQUE", "MARTINE", "NICOLE", "PATRICIA", "BRIGITTE", "MONIQUE", "CORINNE", "CELINE",
            "CAROLINE", "FLORENCE", "SOPHIE", "AURELIE", "EMILIE", "JULIE", "CLAIRE", "ANNE",
            "MARC", "THIERRY", "BRUNO", "DIDIER", "FREDERIC", "VINCENT", "ANTOINE", "ALEXANDRE",
            "THOMAS", "MAXIME", "BENJAMIN", "KEVIN", "ROMAIN", "FLORIAN", "QUENTIN", "ADRIEN"
        ]
        
        # Variations de préfixes pour chaque champ
        self.prefixes_nom = [
            "Nom :", "Nom:", "Nom du patient :", "Patient :", "Nom de famille :",
            "Identité :", "Personne concernée :", "Sujet :", "Nom complet :",
            "Nom et prénom :", "Identité du patient :", "Concerné :", "Individu :",
            "Nom/Prénom :", "Dénomination :", "Appelation :", "Désignation :"
        ]
        
        self.prefixes_reference = [
            "Référence :", "Réf :", "Référence dossier :", "N° dossier :", "Dossier :",
            "Numéro :", "Ref :", "ID :", "Identifiant :", "Code dossier :",
            "N° de dossier :", "Référence du dossier :", "Numéro de référence :",
            "Code :", "N° :", "Réf. dossier :", "Dossier n° :", "Réf. n° :"
        ]
        
        self.prefixes_analyse = [
            "Objet :", "Type d'analyse :", "Analyse :", "Examen :", "Prélèvement :",
            "Nature :", "Type :", "Échantillon :", "Test :", "Diagnostic :",
            "Analyse demandée :", "Type d'examen :", "Nature de l'analyse :",
            "Objet de l'analyse :", "Examen requis :", "Type de test :",
            "Analyse à effectuer :", "Prélèvement pour :", "Test demandé :"
        ]
        
        self.prefixes_date = [
            "Date :", "Date de prélèvement :", "Date prélèvement :", "Prélevé le :",
            "Date d'analyse :", "Date échantillon :", "Collecté le :", "Date collecte :",
            "Date du prélèvement :", "Prélèvement effectué le :", "Date de l'examen :",
            "Échantillon prélevé le :", "Date de réalisation :", "Effectué le :",
            "Date d'échantillonnage :", "Prélèvement du :", "Réalisé le :"
        ]
        
        self.prefixes_service = [
            "Demandeur :", "Service :", "Service demandeur :", "Demandé par :",
            "Origine :", "Prescripteur :", "Commanditaire :", "Institution :",
            "Service prescripteur :", "Demande de :", "À la demande de :",
            "Prescrit par :", "Service d'origine :", "Organisme demandeur :",
            "Établissement :", "Unité :", "Département :", "Bureau :"
        ]
        
        # Types d'analyses variés
        self.types_analyse = [
            "Analyse toxicologique sur cheveux", "Analyse sanguine préventive", 
            "Examen anatomopathologique de biopsie", "Test de dépistage urinaire",
            "Analyse microbiologique", "Examen cytologique", "Test génétique",
            "Analyse biochimique", "Examen histologique", "Test immunologique",
            "Analyse parasitologique", "Examen bactériologique", "Test virologique",
            "Analyse hormonale", "Examen dermatologique", "Test allergologique",
            "Analyse nutritionnelle", "Examen cardiologique", "Test pulmonaire",
            "Analyse de sang pour dépistage de stupéfiants", "Test ADN",
            "Analyse d'urine", "Examen radiologique", "Scanner thoracique",
            "IRM cérébrale", "Échographie abdominale", "Électrocardiogramme",
            "Test de grossesse", "Analyse de selles", "Prélèvement nasal",
            "Test COVID-19", "Analyse de salive", "Biopsie cutanée",
            "Ponction lombaire", "Analyse du liquide céphalo-rachidien",
            "Test de paternité", "Analyse génétique", "Séquençage ADN",
            "Test d'allergie alimentaire", "Analyse de cheveux pour métaux lourds",
            "Dosage vitaminique", "Bilan lipidique", "Glycémie à jeun",
            "Test de fonction hépatique", "Analyse rénale", "Bilan thyroïdien"
        ]
        
        # Services variés
        self.services = [
            "Service régional d'investigation", "Département médical", "Centre d'analyses cliniques",
            "Laboratoire de biologie", "Service de police scientifique", "Gendarmerie nationale",
            "Police judiciaire", "Hôpital universitaire", "Clinique privée", "Centre hospitalier",
            "Laboratoire privé", "Service de médecine légale", "Institut médico-légal",
            "Centre de toxicologie", "Service d'urgences", "Laboratoire de recherche",
            "CHU de Paris", "Hôpital Saint-Antoine", "Clinique des Lilas",
            "Centre médical Pasteur", "Laboratoire Cerba", "Biomnis",
            "Laboratoire Eurofins", "Institut Pasteur", "APHP",
            "Service de cardiologie", "Service de neurologie", "Service d'oncologie",
            "Unité de soins intensifs", "Service de pédiatrie", "Maternité",
            "Service de psychiatrie", "Centre de rééducation", "Médecine du travail",
            "Service de radiologie", "Laboratoire d'anatomie pathologique",
            "Service de dermatologie", "Centre anti-poison", "SAMU",
            "Brigade criminelle", "Police technique et scientifique",
            "Laboratoire de la préfecture de police", "Service central de police judiciaire",
            "Direction générale de la gendarmerie nationale", "Institut de recherche criminelle"
        ]
    
    def generate_reference(self) -> str:
        """Génère une référence de dossier réaliste."""
        year = random.randint(2020, 2025)
        
        patterns = [
            f"{year}-GEND/{random.randint(1, 999):03d}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
            f"{year}-BIO/{random.randint(1, 999):02d}-{random.choice('XYZ')}",
            f"{year}-ANAT/{random.randint(1, 99):02d}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
            f"{year}-LAB/{random.randint(1, 9999):04d}",
            f"REF-{year}-{random.randint(1000, 9999)}",
            f"DOS-{random.randint(100000, 999999)}",
            f"{year}/{random.randint(1, 12):02d}/{random.randint(1, 999):03d}",
            f"ID{year}{random.randint(1000, 9999)}",
            f"CHU-{year}-{random.randint(100, 999)}",
            f"MED{random.randint(10000, 99999)}",
            f"LAB{year}{random.randint(100, 999)}",
            f"HOSP-{random.randint(1000, 9999)}",
            f"CLIN/{year}/{random.randint(1, 999):03d}",
            f"BIOL-{random.randint(100000, 999999)}",
            f"TOXI{year}{random.randint(10, 99)}",
            f"GENE/{random.randint(1000, 9999)}/{year}",
            f"HIST-{year}-{random.randint(1, 999):03d}",
            f"CYTO{random.randint(100000, 999999)}",
            f"MICRO/{year}-{random.randint(1, 99):02d}",
            f"VIRO-{random.randint(10000, 99999)}"
        ]
        
        return random.choice(patterns)
    
    def generate_date(self) -> str:
        """Génère une date réaliste."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2025, 12, 31)
        
        random_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d.%m.%Y",
            "%d %m %Y",
            "%d/%m/%y",
            "%d-%m-%y"
        ]
        
        return random_date.strftime(random.choice(formats))
    
    def generate_name(self) -> str:
        """Génère un nom complet réaliste."""
        nom = random.choice(self.noms)
        prenom = random.choice(self.prenoms)
        
        # Parfois ajouter un deuxième prénom
        if random.random() < 0.3:
            prenom2 = random.choice(self.prenoms)
            prenom = f"{prenom} {prenom2}"
        
        patterns = [
            f"{nom} {prenom}",
            f"{prenom} {nom}",
            f"{nom}, {prenom}",
            f"{nom}-{prenom}",
            f"{nom} ({prenom})",
            f"{prenom} {nom.lower().title()}"
        ]
        
        return random.choice(patterns)
    
    def create_training_example(self) -> Tuple[str, Dict]:
        """Crée un exemple d'entraînement complet avec annotations précises."""
        # Générer les données
        nom = self.generate_name()
        reference = self.generate_reference()
        analyse = random.choice(self.types_analyse)
        date = self.generate_date()
        service = random.choice(self.services)
        
        # Choisir les préfixes
        prefix_nom = random.choice(self.prefixes_nom)
        prefix_ref = random.choice(self.prefixes_reference)
        prefix_analyse = random.choice(self.prefixes_analyse)
        prefix_date = random.choice(self.prefixes_date)
        prefix_service = random.choice(self.prefixes_service)
        
        # Construire le texte avec des variations de format
        separators = ["\n", "\n\n", " | ", " - ", "\t", "  "]
        separator = random.choice(separators)
        
        # Ordre des champs (parfois mélangé)
        fields = [
            (prefix_nom, nom, "nom_personne"),
            (prefix_ref, reference, "reference_dossier"),
            (prefix_analyse, analyse, "type_analyse"),
            (prefix_date, date, "date_prelevement"),
            (prefix_service, service, "service_demandeur")
        ]
        
        # Mélanger l'ordre dans 40% des cas
        if random.random() < 0.4:
            random.shuffle(fields)
        
        # Construire le texte et calculer les positions exactes
        text_parts = []
        entities = []
        current_pos = 0
        
        # Parfois ajouter un en-tête
        if random.random() < 0.3:
            headers = [
                "RAPPORT D'ANALYSE MEDICALE\n\n",
                "LABORATOIRE DE BIOLOGIE\n",
                "CENTRE HOSPITALIER UNIVERSITAIRE\n\n",
                "ANALYSE BIOLOGIQUE\n",
                "COMPTE RENDU D'EXAMEN\n\n",
                "RESULTATS D'ANALYSE\n",
                ""
            ]
            header = random.choice(headers)
            text_parts.append(header)
            current_pos += len(header)
        
        for i, (prefix, value, label) in enumerate(fields):
            if i > 0:
                text_parts.append(separator)
                current_pos += len(separator)
            
            # Ajouter le préfixe
            text_parts.append(prefix)
            current_pos += len(prefix)
            
            # Ajouter un espace si nécessaire
            if not prefix.endswith(" ") and not prefix.endswith(":"):
                text_parts.append(" ")
                current_pos += 1
            elif prefix.endswith(":") and not prefix.endswith(": "):
                text_parts.append(" ")
                current_pos += 1
            
            # Ajouter la valeur et créer l'annotation
            start_pos = current_pos
            text_parts.append(value)
            end_pos = current_pos + len(value)
            current_pos = end_pos
            
            entities.append([start_pos, end_pos, label])
        
        # Parfois ajouter un pied de page
        if random.random() < 0.2:
            footers = [
                "\n\nFin du rapport",
                "\n\nSignature: Dr. Martin",
                "\n\nDocument validé",
                "\n\nRapport généré automatiquement",
                "\n\nConfidentiel",
                ""
            ]
            footer = random.choice(footers)
            text_parts.append(footer)
        
        text = "".join(text_parts)
        annotations = {"entities": entities}
        
        return text, annotations
    
    def generate_dataset(self, num_examples: int = 500) -> List[Tuple[str, Dict]]:
        """Génère un large dataset d'exemples."""
        dataset = []
        
        print(f"Génération de {num_examples} exemples d'entraînement...")
        
        for i in range(num_examples):
            try:
                example = self.create_training_example()
                dataset.append(example)
                
                if (i + 1) % 50 == 0:
                    print(f"✅ {i + 1}/{num_examples} exemples générés")
                    
            except Exception as e:
                print(f"⚠️ Erreur lors de la génération de l'exemple {i}: {e}")
        
        print(f"🎉 Dataset généré: {len(dataset)} exemples")
        return dataset
    
    def validate_dataset(self, dataset: List[Tuple[str, Dict]]) -> bool:
        """Valide le dataset généré."""
        print("🔍 Validation du dataset...")
        
        valid_labels = {"nom_personne", "reference_dossier", "type_analyse", "date_prelevement", "service_demandeur"}
        errors = 0
        
        for i, (text, annotations) in enumerate(dataset):
            if not isinstance(text, str) or not text.strip():
                print(f"❌ Exemple {i}: Texte invalide")
                errors += 1
                continue
            
            if "entities" not in annotations:
                print(f"❌ Exemple {i}: Annotations manquantes")
                errors += 1
                continue
            
            entities = annotations["entities"]
            for j, (start, end, label) in enumerate(entities):
                if not isinstance(start, int) or not isinstance(end, int):
                    print(f"❌ Exemple {i}, entité {j}: Positions invalides")
                    errors += 1
                    continue
                
                if start >= end:
                    print(f"❌ Exemple {i}, entité {j}: start >= end")
                    errors += 1
                    continue
                
                if end > len(text):
                    print(f"❌ Exemple {i}, entité {j}: Position dépasse le texte")
                    errors += 1
                    continue
                
                if label not in valid_labels:
                    print(f"❌ Exemple {i}, entité {j}: Label invalide '{label}'")
                    errors += 1
        
        if errors == 0:
            print("✅ Dataset validé avec succès!")
            return True
        else:
            print(f"❌ {errors} erreurs trouvées dans le dataset")
            return False
    
    def save_dataset(self, dataset: List[Tuple[str, Dict]], output_path: str):
        """Sauvegarde le dataset."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            print(f"💾 Dataset sauvegardé: {output_path}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")

def main():
    """Fonction principale."""
    print("🚀 Génération de données synthétiques pour l'entraînement NER")
    print("=" * 60)
    
    generator = SyntheticDataGenerator()
    
    # Générer un large dataset
    dataset = generator.generate_dataset(num_examples=500)
    
    # Valider le dataset
    if not generator.validate_dataset(dataset):
        print("❌ Échec de la validation. Arrêt du processus.")
        return
    
    # Sauvegarder
    output_path = "training/data/spacy_format/train_data.json"
    generator.save_dataset(dataset, output_path)
    
    # Afficher quelques statistiques
    print("\n📊 STATISTIQUES DU DATASET:")
    print(f"- Nombre total d'exemples: {len(dataset)}")
    
    # Compter les entités par type
    entity_counts = {}
    total_entities = 0
    
    for text, annotations in dataset:
        for start, end, label in annotations["entities"]:
            entity_counts[label] = entity_counts.get(label, 0) + 1
            total_entities += 1
    
    print(f"- Nombre total d'entités: {total_entities}")
    for label, count in entity_counts.items():
        print(f"  - {label}: {count}")
    
    # Afficher quelques exemples
    print("\n📋 EXEMPLES GÉNÉRÉS:")
    for i, (text, annotations) in enumerate(dataset[:3]):
        print(f"\nExemple {i+1}:")
        print(f"Texte: {text[:100]}...")
        print(f"Entités: {len(annotations['entities'])}")
        for start, end, label in annotations['entities']:
            print(f"  - {label}: '{text[start:end]}'")
    
    print("\n🎉 Génération terminée avec succès!")

if __name__ == "__main__":
    main()
