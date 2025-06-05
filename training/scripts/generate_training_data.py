#!/usr/bin/env python3
"""
Générateur de données d'entraînement pour le modèle NER.
Crée des exemples synthétiques variés pour améliorer les performances.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingDataGenerator:
    """Générateur de données d'entraînement synthétiques."""
    
    def __init__(self):
        # Données de base pour la génération
        self.noms = [
            "MARTIN", "BERNARD", "THOMAS", "PETIT", "ROBERT", "RICHARD", "DURAND", "DUBOIS",
            "MOREAU", "LAURENT", "SIMON", "MICHEL", "LEFEBVRE", "LEROY", "ROUX", "DAVID",
            "BERTRAND", "MOREL", "FOURNIER", "GIRARD", "BONNET", "DUPONT", "LAMBERT", "FONTAINE",
            "ROUSSEAU", "VINCENT", "MULLER", "LEFEVRE", "FAURE", "ANDRE", "MERCIER", "BLANC",
            "GUERIN", "BOYER", "GARNIER", "CHEVALIER", "FRANCOIS", "LEGRAND", "GAUTHIER", "GARCIA"
        ]
        
        self.prenoms = [
            "JEAN", "MARIE", "PIERRE", "MICHEL", "ANDRE", "PHILIPPE", "ALAIN", "BERNARD",
            "CHRISTOPHE", "PATRICK", "NICOLAS", "JACQUES", "DANIEL", "FRANCOIS", "ERIC", "LAURENT",
            "OLIVIER", "SEBASTIEN", "JULIEN", "DAVID", "STEPHANE", "PASCAL", "FABRICE", "JEROME",
            "SYLVIE", "NATHALIE", "ISABELLE", "CATHERINE", "CHRISTINE", "SANDRINE", "VALERIE", "KARINE",
            "VERONIQUE", "MARTINE", "NICOLE", "PATRICIA", "BRIGITTE", "MONIQUE", "CORINNE", "CELINE"
        ]
        
        self.prefixes_nom = [
            "Nom :", "Nom:", "Nom du patient :", "Patient :", "Nom de famille :",
            "Identité :", "Personne concernée :", "Sujet :", "Nom complet :"
        ]
        
        self.prefixes_reference = [
            "Référence :", "Réf :", "Référence dossier :", "N° dossier :", "Dossier :",
            "Numéro :", "Ref :", "ID :", "Identifiant :", "Code dossier :"
        ]
        
        self.prefixes_analyse = [
            "Objet :", "Type d'analyse :", "Analyse :", "Examen :", "Prélèvement :",
            "Nature :", "Type :", "Échantillon :", "Test :", "Diagnostic :"
        ]
        
        self.prefixes_date = [
            "Date :", "Date de prélèvement :", "Date prélèvement :", "Prélevé le :",
            "Date d'analyse :", "Date échantillon :", "Collecté le :", "Date collecte :"
        ]
        
        self.prefixes_service = [
            "Demandeur :", "Service :", "Service demandeur :", "Demandé par :",
            "Origine :", "Prescripteur :", "Commanditaire :", "Institution :"
        ]
        
        self.types_analyse = [
            "Analyse toxicologique sur cheveux", "Analyse sanguine préventive", 
            "Examen anatomopathologique de biopsie", "Test de dépistage urinaire",
            "Analyse microbiologique", "Examen cytologique", "Test génétique",
            "Analyse biochimique", "Examen histologique", "Test immunologique",
            "Analyse parasitologique", "Examen bactériologique", "Test virologique",
            "Analyse hormonale", "Examen dermatologique", "Test allergologique",
            "Analyse nutritionnelle", "Examen cardiologique", "Test pulmonaire"
        ]
        
        self.services = [
            "Service régional d'investigation", "Département médical", "Centre d'analyses cliniques",
            "Laboratoire de biologie", "Service de police scientifique", "Gendarmerie nationale",
            "Police judiciaire", "Hôpital universitaire", "Clinique privée", "Centre hospitalier",
            "Laboratoire privé", "Service de médecine légale", "Institut médico-légal",
            "Centre de toxicologie", "Service d'urgences", "Laboratoire de recherche"
        ]
    
    def generate_reference(self) -> str:
        """Génère une référence de dossier aléatoire."""
        year = random.randint(2020, 2025)
        
        patterns = [
            f"{year}-GEND/{random.randint(1, 999):03d}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
            f"{year}-BIO/{random.randint(1, 999):02d}-{random.choice('XYZ')}",
            f"{year}-ANAT/{random.randint(1, 99):02d}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
            f"{year}-LAB/{random.randint(1, 9999):04d}",
            f"REF-{year}-{random.randint(1000, 9999)}",
            f"DOS-{random.randint(100000, 999999)}",
            f"{year}/{random.randint(1, 12):02d}/{random.randint(1, 999):03d}",
            f"ID{year}{random.randint(1000, 9999)}"
        ]
        
        return random.choice(patterns)
    
    def generate_date(self) -> str:
        """Génère une date aléatoire."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2025, 12, 31)
        
        random_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d.%m.%Y"
        ]
        
        return random_date.strftime(random.choice(formats))
    
    def generate_name(self) -> str:
        """Génère un nom complet aléatoire."""
        nom = random.choice(self.noms)
        prenom = random.choice(self.prenoms)
        
        patterns = [
            f"{nom} {prenom}",
            f"{prenom} {nom}",
            f"{nom}, {prenom}",
            f"{nom}-{prenom}"
        ]
        
        return random.choice(patterns)
    
    def generate_training_example(self) -> Tuple[str, Dict]:
        """Génère un exemple d'entraînement complet."""
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
        separators = ["\n", "\n\n", " | ", " - "]
        separator = random.choice(separators)
        
        # Ordre aléatoire des champs
        fields = [
            (prefix_nom, nom, "nom_personne"),
            (prefix_ref, reference, "reference_dossier"),
            (prefix_analyse, analyse, "type_analyse"),
            (prefix_date, date, "date_prelevement"),
            (prefix_service, service, "service_demandeur")
        ]
        
        # Mélanger l'ordre parfois
        if random.random() < 0.3:
            random.shuffle(fields)
        
        # Construire le texte et les annotations
        text_parts = []
        entities = []
        current_pos = 0
        
        for i, (prefix, value, label) in enumerate(fields):
            if i > 0:
                text_parts.append(separator)
                current_pos += len(separator)
            
            # Ajouter le préfixe
            text_parts.append(prefix)
            current_pos += len(prefix)
            
            # Ajouter un espace si nécessaire
            if not prefix.endswith(" "):
                text_parts.append(" ")
                current_pos += 1
            
            # Ajouter la valeur et créer l'annotation
            start_pos = current_pos
            text_parts.append(value)
            end_pos = current_pos + len(value)
            current_pos = end_pos
            
            entities.append([start_pos, end_pos, label])
        
        text = "".join(text_parts)
        annotations = {"entities": entities}
        
        return text, annotations
    
    def generate_dataset(self, num_examples: int = 100) -> List[Tuple[str, Dict]]:
        """Génère un dataset complet."""
        dataset = []
        
        for i in range(num_examples):
            try:
                example = self.generate_training_example()
                dataset.append(example)
                
                if (i + 1) % 20 == 0:
                    logger.info(f"Généré {i + 1}/{num_examples} exemples")
                    
            except Exception as e:
                logger.warning(f"Erreur lors de la génération de l'exemple {i}: {e}")
        
        logger.info(f"✅ Dataset généré: {len(dataset)} exemples")
        return dataset
    
    def add_noise_and_variations(self, dataset: List[Tuple[str, Dict]]) -> List[Tuple[str, Dict]]:
        """Ajoute du bruit et des variations aux données."""
        enhanced_dataset = dataset.copy()
        
        for text, annotations in dataset:
            # Variation 1: Changer la casse
            if random.random() < 0.2:
                new_text = text.lower()
                enhanced_dataset.append((new_text, annotations))
            
            # Variation 2: Ajouter des espaces supplémentaires
            if random.random() < 0.2:
                new_text = text.replace(":", " : ").replace("  ", " ")
                # Ajuster les positions des entités
                new_annotations = self._adjust_annotations(text, new_text, annotations)
                if new_annotations:
                    enhanced_dataset.append((new_text, new_annotations))
            
            # Variation 3: Ajouter du texte de contexte
            if random.random() < 0.1:
                context_before = random.choice([
                    "RAPPORT D'ANALYSE\n\n",
                    "Document confidentiel\n",
                    "Laboratoire XYZ\n\n",
                    ""
                ])
                context_after = random.choice([
                    "\n\nFin du rapport",
                    "\n\nSignature: Dr. Martin",
                    "\n\nDocument validé",
                    ""
                ])
                
                new_text = context_before + text + context_after
                # Ajuster les positions
                offset = len(context_before)
                new_entities = []
                for start, end, label in annotations["entities"]:
                    new_entities.append([start + offset, end + offset, label])
                
                enhanced_dataset.append((new_text, {"entities": new_entities}))
        
        logger.info(f"✅ Dataset enrichi: {len(dataset)} -> {len(enhanced_dataset)} exemples")
        return enhanced_dataset
    
    def _adjust_annotations(self, old_text: str, new_text: str, annotations: Dict) -> Dict:
        """Ajuste les annotations après modification du texte."""
        # Implémentation simplifiée - dans un cas réel, il faudrait un alignement plus sophistiqué
        try:
            new_entities = []
            for start, end, label in annotations["entities"]:
                old_entity = old_text[start:end]
                new_start = new_text.find(old_entity)
                if new_start != -1:
                    new_end = new_start + len(old_entity)
                    new_entities.append([new_start, new_end, label])
            
            return {"entities": new_entities}
        except:
            return None
    
    def save_dataset(self, dataset: List[Tuple[str, Dict]], output_path: str):
        """Sauvegarde le dataset au format JSON."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Dataset sauvegardé: {output_path}")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")

def main():
    """Fonction principale de génération."""
    generator = TrainingDataGenerator()
    
    # Générer le dataset de base
    logger.info("🔄 Génération du dataset de base...")
    base_dataset = generator.generate_dataset(num_examples=50)
    
    # Ajouter des variations
    logger.info("🔄 Ajout de variations...")
    enhanced_dataset = generator.add_noise_and_variations(base_dataset)
    
    # Charger les données existantes
    existing_data_path = "training/data/spacy_format/train_data.json"
    try:
        with open(existing_data_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        logger.info(f"📂 Données existantes chargées: {len(existing_data)} exemples")
        
        # Combiner avec les nouvelles données
        combined_dataset = existing_data + enhanced_dataset
    except FileNotFoundError:
        logger.info("📂 Aucune donnée existante trouvée, utilisation des nouvelles données uniquement")
        combined_dataset = enhanced_dataset
    
    # Sauvegarder le dataset final
    output_path = "training/data/spacy_format/train_data_enhanced.json"
    generator.save_dataset(combined_dataset, output_path)
    
    # Remplacer le fichier original
    import shutil
    shutil.copy(output_path, existing_data_path)
    
    logger.info(f"🎉 Génération terminée! Dataset final: {len(combined_dataset)} exemples")
    
    # Afficher quelques exemples
    logger.info("📋 Exemples générés:")
    for i, (text, annotations) in enumerate(combined_dataset[:3]):
        logger.info(f"Exemple {i+1}:")
        logger.info(f"  Texte: {text[:100]}...")
        logger.info(f"  Entités: {len(annotations['entities'])}")

if __name__ == "__main__":
    main()
