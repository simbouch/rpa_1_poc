#!/usr/bin/env python3
"""
Générateur de données synthétiques spécialisées pour les documents juridiques.
Crée un modèle spécialisé pour les documents légaux.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class LegalDataGenerator:
    """Générateur de données d'entraînement pour documents juridiques."""
    
    def __init__(self):
        # Noms juridiques spécialisés
        self.noms_juridiques = [
            "MARTIN", "BERNARD", "THOMAS", "PETIT", "ROBERT", "RICHARD", "DURAND", "DUBOIS",
            "MOREAU", "LAURENT", "SIMON", "MICHEL", "LEFEBVRE", "LEROY", "ROUX", "DAVID",
            "BERTRAND", "MOREL", "FOURNIER", "GIRARD", "BONNET", "DUPONT", "LAMBERT", "FONTAINE"
        ]
        
        self.prenoms_juridiques = [
            "JEAN", "MARIE", "PIERRE", "MICHEL", "ANDRE", "PHILIPPE", "ALAIN", "BERNARD",
            "CHRISTOPHE", "PATRICK", "NICOLAS", "JACQUES", "DANIEL", "FRANCOIS", "ERIC", "LAURENT",
            "SYLVIE", "NATHALIE", "ISABELLE", "CATHERINE", "CHRISTINE", "SANDRINE", "VALERIE"
        ]
        
        # Préfixes juridiques spécialisés
        self.prefixes_juridiques = {
            "nom_personne": [
                "Requérant :", "Défendeur :", "Plaignant :", "Mis en cause :", "Partie :",
                "Nom :", "Identité :", "Personne concernée :", "Justiciable :", "Client :"
            ],
            "reference_dossier": [
                "N° RG :", "Référence :", "Dossier :", "N° de procédure :", "Affaire :",
                "N° parquet :", "Répertoire général :", "N° :", "Référence judiciaire :", "Dossier n° :"
            ],
            "type_analyse": [
                "Objet :", "Nature de l'affaire :", "Procédure :", "Type de contentieux :", "Matière :",
                "Qualification :", "Chef d'accusation :", "Motif :", "Fondement :", "Cause :"
            ],
            "date_prelevement": [
                "Date d'audience :", "Date de citation :", "Date de convocation :", "Date :", "Fixé au :",
                "Audience du :", "Séance du :", "Date de comparution :", "Programmé le :", "Prévu le :"
            ],
            "service_demandeur": [
                "Tribunal :", "Juridiction :", "Cour :", "Instance :", "Formation :",
                "Chambre :", "Section :", "Parquet :", "Greffe :", "Cabinet :"
            ]
        }
        
        # Types d'affaires juridiques
        self.affaires_juridiques = [
            "Contentieux administratif", "Procédure civile", "Affaire pénale",
            "Divorce par consentement mutuel", "Succession litigieuse", "Contrat de travail",
            "Responsabilité civile", "Droit commercial", "Propriété intellectuelle",
            "Droit immobilier", "Droit de la famille", "Droit des sociétés",
            "Contentieux fiscal", "Droit pénal", "Procédure d'urgence",
            "Référé provision", "Saisie conservatoire", "Liquidation judiciaire",
            "Redressement judiciaire", "Procédure collective", "Bail commercial",
            "Expulsion locative", "Trouble de voisinage", "Servitude de passage",
            "Usufruit viager", "Donation entre époux", "Testament olographe",
            "Tutelle majeur protégé", "Curatelle renforcée", "Sauvegarde de justice",
            "Adoption plénière", "Reconnaissance de paternité", "Autorité parentale"
        ]
        
        # Juridictions
        self.juridictions = [
            "Tribunal de Grande Instance de Paris", "Cour d'Appel de Versailles",
            "Tribunal Administratif de Montreuil", "Conseil d'État",
            "Tribunal de Commerce de Nanterre", "Cour de Cassation",
            "Tribunal Correctionnel de Bobigny", "Cour d'Assises des Hauts-de-Seine",
            "Tribunal des Affaires de Sécurité Sociale", "Tribunal Paritaire des Baux Ruraux",
            "Conseil de Prud'hommes de Paris", "Tribunal pour Enfants",
            "Juge aux Affaires Familiales", "Juge de l'Exécution",
            "Juge des Libertés et de la Détention", "Tribunal Judiciaire",
            "Cour Administrative d'Appel", "Tribunal de Police",
            "Chambre Sociale", "Chambre Civile", "Chambre Commerciale",
            "Chambre Criminelle", "Formation Collégiale", "Juge Unique",
            "Référé Civil", "Référé Administratif", "Ordonnance sur Requête"
        ]
    
    def generate_legal_reference(self) -> str:
        """Génère une référence juridique."""
        year = random.randint(2020, 2025)
        patterns = [
            f"RG {year}/{random.randint(1000, 9999)}",
            f"{year}/RG/{random.randint(100, 999)}",
            f"N° {random.randint(100000, 999999)}/{year}",
            f"PROC-{year}-{random.randint(1000, 9999)}",
            f"AFF{year}{random.randint(1000, 9999)}",
            f"DOS/{year}/{random.randint(1, 999):03d}",
            f"REF-JUR-{random.randint(100000, 999999)}",
            f"PARQ-{year}-{random.randint(1, 999):03d}"
        ]
        return random.choice(patterns)
    
    def generate_legal_date(self) -> str:
        """Génère une date juridique."""
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2025, 12, 31)
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %m %Y"]
        return random_date.strftime(random.choice(formats))
    
    def generate_legal_name(self) -> str:
        """Génère un nom juridique."""
        nom = random.choice(self.noms_juridiques)
        prenom = random.choice(self.prenoms_juridiques)
        
        patterns = [f"{nom} {prenom}", f"{prenom} {nom}", f"{nom}, {prenom}"]
        return random.choice(patterns)
    
    def create_legal_example(self) -> Tuple[str, Dict]:
        """Crée un exemple juridique."""
        nom = self.generate_legal_name()
        reference = self.generate_legal_reference()
        affaire = random.choice(self.affaires_juridiques)
        date = self.generate_legal_date()
        juridiction = random.choice(self.juridictions)
        
        # Choisir les préfixes
        prefix_nom = random.choice(self.prefixes_juridiques["nom_personne"])
        prefix_ref = random.choice(self.prefixes_juridiques["reference_dossier"])
        prefix_affaire = random.choice(self.prefixes_juridiques["type_analyse"])
        prefix_date = random.choice(self.prefixes_juridiques["date_prelevement"])
        prefix_juridiction = random.choice(self.prefixes_juridiques["service_demandeur"])
        
        # Construire le texte juridique
        separators = ["\n", "\n\n", " | ", "\t"]
        separator = random.choice(separators)
        
        fields = [
            (prefix_nom, nom, "nom_personne"),
            (prefix_ref, reference, "reference_dossier"),
            (prefix_affaire, affaire, "type_analyse"),
            (prefix_date, date, "date_prelevement"),
            (prefix_juridiction, juridiction, "service_demandeur")
        ]
        
        # Parfois mélanger l'ordre
        if random.random() < 0.3:
            random.shuffle(fields)
        
        text_parts = []
        entities = []
        current_pos = 0
        
        # Ajouter un en-tête juridique parfois
        if random.random() < 0.4:
            headers = [
                "TRIBUNAL DE GRANDE INSTANCE\n\n",
                "COUR D'APPEL\n\n", 
                "ASSIGNATION EN JUSTICE\n\n",
                "CITATION À COMPARAÎTRE\n\n",
                "ORDONNANCE DE RÉFÉRÉ\n\n",
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
        
        # Ajouter une conclusion juridique parfois
        if random.random() < 0.3:
            footers = [
                "\n\nPar ces motifs",
                "\n\nEn conséquence",
                "\n\nLe Tribunal ordonne",
                ""
            ]
            footer = random.choice(footers)
            text_parts.append(footer)
        
        text = "".join(text_parts)
        annotations = {"entities": entities}
        
        return text, annotations
    
    def generate_legal_dataset(self, num_examples: int = 200) -> List[Tuple[str, Dict]]:
        """Génère un dataset juridique."""
        dataset = []
        print(f"Génération de {num_examples} exemples juridiques...")
        
        for i in range(num_examples):
            try:
                example = self.create_legal_example()
                dataset.append(example)
                
                if (i + 1) % 50 == 0:
                    print(f"✅ {i + 1}/{num_examples} exemples juridiques générés")
            except Exception as e:
                print(f"⚠️ Erreur exemple {i}: {e}")
        
        print(f"⚖️ Dataset juridique généré: {len(dataset)} exemples")
        return dataset
    
    def save_legal_dataset(self, dataset: List[Tuple[str, Dict]], output_path: str):
        """Sauvegarde le dataset juridique."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            print(f"💾 Dataset juridique sauvegardé: {output_path}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")

def main():
    """Génère le dataset juridique."""
    print("⚖️ Génération de données juridiques spécialisées")
    print("=" * 50)
    
    generator = LegalDataGenerator()
    dataset = generator.generate_legal_dataset(num_examples=200)
    
    # Sauvegarder
    output_path = "training/data/legal_format/train_data.json"
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generator.save_legal_dataset(dataset, output_path)
    
    print("\n📊 Exemples générés:")
    for i, (text, annotations) in enumerate(dataset[:2]):
        print(f"\nExemple juridique {i+1}:")
        print(f"Texte: {text[:80]}...")
        print(f"Entités: {len(annotations['entities'])}")

if __name__ == "__main__":
    main()
