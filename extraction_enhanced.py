#!/usr/bin/env python3
"""
Module d'extraction amélioré avec support pour les modèles entraînés.
Combine l'extraction par modèle NER et les méthodes de fallback par regex.
"""

import pdfplumber
import spacy
import re
import os
import logging
from typing import Dict, Optional, Tuple, List
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extracteur de données PDF avec modèle NER et fallback regex."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialise l'extracteur.
        
        Args:
            model_path: Chemin vers le modèle entraîné. Si None, utilise le modèle par défaut.
        """
        self.nlp = None
        self.use_trained_model = False
        
        # Essayer de charger le modèle entraîné
        if model_path and os.path.exists(model_path):
            try:
                self.nlp = spacy.load(model_path)
                self.use_trained_model = True
                logger.info(f"✅ Modèle entraîné chargé: {model_path}")
            except Exception as e:
                logger.warning(f"⚠️ Impossible de charger le modèle entraîné: {e}")
        
        # Fallback vers le modèle par défaut
        if not self.use_trained_model:
            try:
                self.nlp = spacy.load("fr_core_news_md")
                logger.info("✅ Modèle par défaut fr_core_news_md chargé")
            except OSError:
                logger.error("❌ Aucun modèle spaCy disponible")
                raise
    
    def lire_pdf(self, chemin_fichier: str) -> str:
        """Extrait le texte d'un fichier PDF."""
        try:
            with pdfplumber.open(chemin_fichier) as pdf:
                texte = "\n".join([
                    page.extract_text() or "" 
                    for page in pdf.pages
                ])
            logger.info(f"✅ PDF lu: {len(texte)} caractères extraits")
            return texte
        except Exception as e:
            logger.error(f"❌ Erreur lors de la lecture du PDF: {e}")
            raise
    
    def extraire_avec_modele(self, texte: str) -> Dict[str, Optional[str]]:
        """Extrait les informations en utilisant le modèle NER."""
        if not self.use_trained_model:
            return {}
        
        try:
            doc = self.nlp(texte)
            
            # Mapping des labels vers les clés de sortie
            label_mapping = {
                "nom_personne": "nom_prenom",
                "reference_dossier": "reference_dossier",
                "type_analyse": "type_prelevement",
                "date_prelevement": "date_prelevement",
                "service_demandeur": "service_demandeur"
            }

            resultats = {}

            for ent in doc.ents:
                if ent.label_ in label_mapping:
                    key = label_mapping[ent.label_]
                    # Garder l'entité (pas de score disponible dans notre modèle simple)
                    if key not in resultats:
                        resultats[key] = ent.text.strip()
            
            logger.info(f"✅ Extraction par modèle: {len(resultats)} champs trouvés")
            return resultats
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de l'extraction par modèle: {e}")
            return {}
    
    def extraire_avec_regex(self, texte: str) -> Dict[str, Optional[str]]:
        """Extrait les informations en utilisant des expressions régulières."""
        try:
            # Patterns regex améliorés
            patterns = {
                "reference_dossier": [
                    r"(?:Référence|Réf\.?|Reference|N°\s*dossier)\s*:?\s*([\w\d\-\/]+)",
                    r"Dossier\s*:?\s*([\w\d\-\/]+)"
                ],
                "type_prelevement": [
                    r"(?:Objet|Type\s*d'analyse|Analyse|Examen)\s*:?\s*(.+?)(?:\n|$)",
                    r"(?:Prélèvement|Échantillon)\s*:?\s*(.+?)(?:\n|$)"
                ],
                "date_prelevement": [
                    r"(?:Date\s*de\s*prélèvement|Date\s*prélèvement|Prélevé\s*le|Date)\s*:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                    r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
                ],
                "service_demandeur": [
                    r"(?:Demandeur|Service|Demandé\s*par)\s*:?\s*([^:\n]+?)(?:\n|$)",
                    r"(?:Police|Gendarmerie|Laboratoire|Hôpital|Clinique|Centre)",
                ],
                "nom_prenom": [
                    r"(?:Nom|Patient|Nom\s*du\s*patient)\s*:?\s*([A-Z][A-Z\s\-]+?)(?:\n|$)",
                    r"(?:M\.|Mme|Mr|Madame|Monsieur)\s+([A-Z][A-Z\s\-]+)"
                ]
            }
            
            resultats = {}
            
            for field, pattern_list in patterns.items():
                for pattern in pattern_list:
                    match = re.search(pattern, texte, re.IGNORECASE | re.MULTILINE)
                    if match:
                        value = match.group(1).strip()
                        if value and len(value) > 1:  # Éviter les matches trop courts
                            resultats[field] = value
                            break
            
            # Post-traitement spécifique
            if "nom_prenom" in resultats:
                resultats["nom_prenom"] = resultats["nom_prenom"].upper()
            
            if "service_demandeur" in resultats:
                service = resultats["service_demandeur"]
                if any(word in service.lower() for word in ["police", "gendarmerie"]):
                    resultats["service_demandeur"] = service.capitalize()
            
            logger.info(f"✅ Extraction par regex: {len(resultats)} champs trouvés")
            return resultats
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de l'extraction par regex: {e}")
            return {}
    
    def fusionner_resultats(self, resultats_modele: Dict, resultats_regex: Dict) -> Dict[str, Optional[str]]:
        """Fusionne les résultats du modèle et du regex en privilégiant le modèle."""
        resultats_finaux = {}
        
        # Tous les champs possibles
        champs = {"nom_prenom", "reference_dossier", "type_prelevement", "date_prelevement", "service_demandeur"}
        
        for champ in champs:
            # Privilégier le modèle, puis le regex, puis None
            if champ in resultats_modele and resultats_modele[champ]:
                resultats_finaux[champ] = resultats_modele[champ]
            elif champ in resultats_regex and resultats_regex[champ]:
                resultats_finaux[champ] = resultats_regex[champ]
            else:
                resultats_finaux[champ] = None
        
        return resultats_finaux
    
    def extraire_infos(self, chemin_fichier: str) -> Dict[str, Optional[str]]:
        """
        Extrait les informations d'un fichier PDF.
        
        Args:
            chemin_fichier: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire avec les informations extraites
        """
        # Lire le PDF
        texte = self.lire_pdf(chemin_fichier)
        
        # Extraction avec le modèle NER
        resultats_modele = self.extraire_avec_modele(texte)
        
        # Extraction avec regex (fallback)
        resultats_regex = self.extraire_avec_regex(texte)
        
        # Fusionner les résultats
        resultats_finaux = self.fusionner_resultats(resultats_modele, resultats_regex)
        
        # Ajouter des métadonnées
        resultats_finaux["_metadata"] = {
            "extraction_method": "model" if self.use_trained_model else "regex",
            "model_fields": len(resultats_modele),
            "regex_fields": len(resultats_regex),
            "text_length": len(texte)
        }
        
        logger.info(f"✅ Extraction terminée: {sum(1 for v in resultats_finaux.values() if v and not isinstance(v, dict))} champs extraits")
        
        return resultats_finaux

# Fonction de compatibilité avec l'ancienne API
def extraire_infos(chemin_fichier: str) -> Dict[str, Optional[str]]:
    """
    Fonction de compatibilité avec l'ancienne API.
    Essaie d'utiliser le modèle entraîné, sinon utilise le regex.
    """
    # Chercher le modèle entraîné
    model_path = "training/model_output/model-best"
    if not os.path.exists(model_path):
        model_path = None
    
    extracteur = PDFExtractor(model_path)
    resultats = extracteur.extraire_infos(chemin_fichier)
    
    # Retirer les métadonnées pour la compatibilité
    if "_metadata" in resultats:
        del resultats["_metadata"]
    
    return resultats

# Fonction pour obtenir les modèles disponibles
def get_available_models() -> List[str]:
    """Retourne la liste des modèles disponibles."""
    models = []
    
    # Modèle entraîné
    trained_model = "training/model_output/model-best"
    if os.path.exists(trained_model):
        models.append(trained_model)
    
    # Modèle par défaut
    try:
        spacy.load("fr_core_news_md")
        models.append("fr_core_news_md")
    except OSError:
        pass
    
    return models

if __name__ == "__main__":
    # Test simple
    print("🧪 Test de l'extracteur...")
    
    # Lister les modèles disponibles
    models = get_available_models()
    print(f"Modèles disponibles: {models}")
    
    # Test avec un fichier exemple si disponible
    test_files = ["exemple_rapport.pdf", "rapport_analyse_complet.pdf"]
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📄 Test avec {test_file}:")
            try:
                resultats = extraire_infos(test_file)
                for key, value in resultats.items():
                    print(f"  {key}: {value}")
            except Exception as e:
                print(f"  ❌ Erreur: {e}")
            break
    else:
        print("Aucun fichier de test trouvé")
