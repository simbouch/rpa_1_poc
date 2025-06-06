#!/usr/bin/env python3
"""
Système d'extraction avancé avec support multi-modèles.
"""

import pdfplumber
import spacy
import re
import os
import json
import logging
from typing import Dict, Optional, List
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiModelExtractor:
    """Extracteur PDF avec support de multiples modèles spécialisés."""
    
    def __init__(self):
        self.models = {}
        self.current_model = None
        self.model_info = {}
        self.load_available_models()
    
    def load_available_models(self):
        """Charge tous les modèles disponibles."""
        model_configs = {
            "spacy_default": {
                "path": "fr_core_news_md",
                "name": "Modèle spaCy par défaut",
                "description": "Modèle français général de spaCy",
                "type": "default"
            },
            "general": {
                "path": "models/general_model",
                "name": "Modèle général entraîné",
                "description": "Modèle entraîné pour documents généraux",
                "type": "trained"
            },
            "medical": {
                "path": "models/medical_model", 
                "name": "Modèle médical spécialisé",
                "description": "Modèle spécialisé pour rapports médicaux",
                "type": "trained"
            },
            "legal": {
                "path": "models/legal_model",
                "name": "Modèle juridique spécialisé", 
                "description": "Modèle spécialisé pour documents juridiques",
                "type": "trained"
            }
        }
        
        for model_id, config in model_configs.items():
            try:
                if config["type"] == "default":
                    nlp = spacy.load(config["path"])
                    self.models[model_id] = nlp
                    self.model_info[model_id] = config
                    logger.info(f"✅ Modèle par défaut chargé: {model_id}")
                elif os.path.exists(config["path"]):
                    nlp = spacy.load(config["path"])
                    self.models[model_id] = nlp
                    self.model_info[model_id] = config
                    logger.info(f"✅ Modèle entraîné chargé: {model_id}")
                else:
                    logger.info(f"⚠️ Modèle non trouvé: {config['path']}")
            except Exception as e:
                logger.warning(f"❌ Erreur chargement {model_id}: {e}")
        
        # Définir le modèle par défaut
        if "general" in self.models:
            self.current_model = "general"
        elif "spacy_default" in self.models:
            self.current_model = "spacy_default"
        else:
            self.current_model = list(self.models.keys())[0] if self.models else None
    
    def get_available_models(self) -> Dict[str, Dict]:
        """Retourne la liste des modèles disponibles avec leurs infos."""
        return {
            model_id: {
                "name": info["name"],
                "description": info["description"],
                "type": info["type"],
                "available": model_id in self.models
            }
            for model_id, info in self.model_info.items()
        }
    
    def set_model(self, model_id: str) -> bool:
        """Change le modèle actuel."""
        if model_id in self.models:
            self.current_model = model_id
            logger.info(f"🔄 Modèle changé vers: {self.model_info[model_id]['name']}")
            return True
        else:
            logger.error(f"❌ Modèle non disponible: {model_id}")
            return False
    
    def extract_with_model(self, text: str) -> Dict[str, Optional[str]]:
        """Extrait avec le modèle NER actuel."""
        if not self.current_model or self.current_model not in self.models:
            return {}
        
        try:
            nlp = self.models[self.current_model]
            doc = nlp(text)
            
            # Mapping des labels
            label_mapping = {
                "nom_personne": "nom_prenom",
                "reference_dossier": "reference_dossier",
                "type_analyse": "type_prelevement", 
                "date_prelevement": "date_prelevement",
                "service_demandeur": "service_demandeur"
            }
            
            results = {}
            for ent in doc.ents:
                if ent.label_ in label_mapping:
                    key = label_mapping[ent.label_]
                    if key not in results:
                        results[key] = ent.text.strip()
            
            logger.info(f"✅ Extraction modèle {self.current_model}: {len(results)} champs")
            return results
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur extraction modèle: {e}")
            return {}
    
    def extract_with_regex(self, text: str) -> Dict[str, Optional[str]]:
        """Extraction de fallback avec regex."""
        patterns = {
            "reference_dossier": [
                r"(?:Référence|Réf\.?|Reference|N°\s*dossier|IPP|Dossier)\s*:?\s*([\w\d\-\/]+)",
            ],
            "type_prelevement": [
                r"(?:Objet|Type\s*d'analyse|Analyse|Examen|Diagnostic|Test|Bilan)\s*:?\s*(.+?)(?:\n|$)",
            ],
            "date_prelevement": [
                r"(?:Date|Réalisé|Effectué|Prélevé)\s*[:\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4})",
            ],
            "service_demandeur": [
                r"(?:Service|Demandeur|Prescripteur|Unité|Département)\s*:?\s*([^:\n]+?)(?:\n|$)",
            ],
            "nom_prenom": [
                r"(?:Nom|Patient|Identité|Malade)\s*[:\s]*([A-Z][A-Z\s\-]+?)(?:\n|$)",
            ]
        }
        
        results = {}
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    value = match.group(1).strip()
                    if value and len(value) > 1:
                        results[field] = value
                        break
        
        logger.info(f"✅ Extraction regex: {len(results)} champs")
        return results
    
    def read_pdf(self, file_path: str) -> str:
        """Lit le contenu d'un PDF."""
        try:
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            logger.info(f"✅ PDF lu: {len(text)} caractères")
            return text
        except Exception as e:
            logger.error(f"❌ Erreur lecture PDF: {e}")
            raise
    
    def extract_from_pdf(self, file_path: str) -> Dict[str, Optional[str]]:
        """Extraction complète depuis un PDF."""
        # Lire le PDF
        text = self.read_pdf(file_path)
        
        # Extraction avec modèle
        model_results = self.extract_with_model(text)
        
        # Extraction avec regex (fallback)
        regex_results = self.extract_with_regex(text)
        
        # Fusionner les résultats (privilégier le modèle)
        final_results = {}
        fields = {"nom_prenom", "reference_dossier", "type_prelevement", "date_prelevement", "service_demandeur"}
        
        for field in fields:
            if field in model_results and model_results[field]:
                final_results[field] = model_results[field]
            elif field in regex_results and regex_results[field]:
                final_results[field] = regex_results[field]
            else:
                final_results[field] = None
        
        # Métadonnées
        final_results["_metadata"] = {
            "model_used": self.model_info.get(self.current_model, {}).get("name", "Inconnu"),
            "model_id": self.current_model,
            "extraction_method": "model" if model_results else "regex",
            "model_fields": len(model_results),
            "regex_fields": len(regex_results),
            "text_length": len(text)
        }
        
        logger.info(f"✅ Extraction terminée: {sum(1 for v in final_results.values() if v and not isinstance(v, dict))} champs")
        return final_results
    
    def get_model_performance(self) -> Dict:
        """Retourne les statistiques de performance des modèles."""
        return {
            "current_model": self.current_model,
            "available_models": len(self.models),
            "model_info": self.model_info.get(self.current_model, {})
        }

# Instance globale
extractor = MultiModelExtractor()

def get_available_models() -> List[str]:
    """Fonction de compatibilité."""
    models = []
    available = extractor.get_available_models()
    for model_id, info in available.items():
        if info["available"]:
            models.append(f"{info['name']} ({model_id})")
    return models

def extract_with_model(file_path: str, model_id: str = None) -> Dict:
    """Fonction d'extraction avec modèle spécifique."""
    if model_id:
        extractor.set_model(model_id)
    return extractor.extract_from_pdf(file_path)
