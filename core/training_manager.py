#!/usr/bin/env python3
"""
Gestionnaire d'entraînement pour créer de nouveaux modèles.
"""

import os
import json
import spacy
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingManager:
    """Gestionnaire pour l'entraînement de nouveaux modèles."""
    
    def __init__(self):
        self.training_dir = Path("training")
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        
        self.model_types = {
            "general": {
                "name": "Modèle général",
                "description": "Pour documents généraux et administratifs",
                "data_generator": "generate_synthetic_data.py"
            },
            "medical": {
                "name": "Modèle médical",
                "description": "Pour rapports et documents médicaux",
                "data_generator": "generate_medical_data.py"
            },
            "legal": {
                "name": "Modèle juridique", 
                "description": "Pour documents juridiques et légaux",
                "data_generator": "generate_legal_data.py"
            }
        }
    
    def list_available_training_types(self) -> Dict:
        """Liste les types d'entraînement disponibles."""
        return self.model_types
    
    def generate_training_data(self, model_type: str, num_examples: int = 500) -> bool:
        """Génère des données d'entraînement pour un type de modèle."""
        if model_type not in self.model_types:
            logger.error(f"❌ Type de modèle non supporté: {model_type}")
            return False
        
        generator_script = self.model_types[model_type]["data_generator"]
        script_path = self.training_dir / "scripts" / generator_script
        
        if not script_path.exists():
            logger.error(f"❌ Script générateur non trouvé: {script_path}")
            return False
        
        try:
            logger.info(f"🔄 Génération de données pour {model_type}...")
            result = subprocess.run([
                sys.executable, str(script_path)
            ], capture_output=True, text=True, cwd=str(self.training_dir.parent))
            
            if result.returncode == 0:
                logger.info(f"✅ Données générées pour {model_type}")
                return True
            else:
                logger.error(f"❌ Erreur génération: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la génération: {e}")
            return False
    
    def convert_training_data(self, model_type: str) -> bool:
        """Convertit les données JSON en format spaCy."""
        try:
            logger.info(f"🔄 Conversion des données pour {model_type}...")
            
            # Utiliser le script de conversion existant
            convert_script = self.training_dir / "scripts" / "convert_data.py"
            if not convert_script.exists():
                logger.error("❌ Script de conversion non trouvé")
                return False
            
            result = subprocess.run([
                sys.executable, str(convert_script)
            ], capture_output=True, text=True, cwd=str(self.training_dir.parent))
            
            if result.returncode == 0:
                logger.info(f"✅ Données converties pour {model_type}")
                return True
            else:
                logger.error(f"❌ Erreur conversion: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la conversion: {e}")
            return False
    
    def train_model(self, model_type: str, epochs: int = 50) -> bool:
        """Entraîne un nouveau modèle."""
        try:
            logger.info(f"🚀 Entraînement du modèle {model_type}...")
            
            # Utiliser le script d'entraînement simple
            train_script = self.training_dir / "simple_train.py"
            if not train_script.exists():
                logger.error("❌ Script d'entraînement non trouvé")
                return False
            
            result = subprocess.run([
                sys.executable, str(train_script)
            ], capture_output=True, text=True, cwd=str(self.training_dir.parent))
            
            if result.returncode == 0:
                logger.info(f"✅ Modèle {model_type} entraîné avec succès")
                
                # Déplacer le modèle vers le bon dossier
                source_path = self.training_dir / "model_output" / "model-best"
                target_path = self.models_dir / f"{model_type}_model"
                
                if source_path.exists():
                    if target_path.exists():
                        import shutil
                        shutil.rmtree(target_path)
                    
                    import shutil
                    shutil.move(str(source_path), str(target_path))
                    
                    # Créer les métadonnées du modèle
                    self.create_model_metadata(model_type, target_path)
                    
                    logger.info(f"✅ Modèle déplacé vers: {target_path}")
                    return True
                else:
                    logger.error("❌ Modèle entraîné non trouvé")
                    return False
            else:
                logger.error(f"❌ Erreur entraînement: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'entraînement: {e}")
            return False
    
    def create_model_metadata(self, model_type: str, model_path: Path):
        """Crée les métadonnées du modèle."""
        metadata = {
            "model_type": model_type,
            "model_name": self.model_types[model_type]["name"],
            "description": self.model_types[model_type]["description"],
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "labels": ["nom_personne", "reference_dossier", "type_analyse", "date_prelevement", "service_demandeur"],
            "training_info": {
                "framework": "spaCy",
                "base_model": "fr_core_news_md"
            }
        }
        
        metadata_path = model_path / "model_info.json"
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Métadonnées créées: {metadata_path}")
        except Exception as e:
            logger.warning(f"⚠️ Erreur création métadonnées: {e}")
    
    def train_new_model(self, model_type: str, num_examples: int = 500, epochs: int = 50) -> bool:
        """Pipeline complet d'entraînement d'un nouveau modèle."""
        logger.info(f"🚀 Démarrage entraînement complet pour {model_type}")
        
        # 1. Générer les données
        if not self.generate_training_data(model_type, num_examples):
            return False
        
        # 2. Convertir les données
        if not self.convert_training_data(model_type):
            return False
        
        # 3. Entraîner le modèle
        if not self.train_model(model_type, epochs):
            return False
        
        logger.info(f"🎉 Entraînement complet terminé pour {model_type}")
        return True
    
    def list_trained_models(self) -> List[Dict]:
        """Liste les modèles entraînés disponibles."""
        models = []
        
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                metadata_path = model_dir / "model_info.json"
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        models.append({
                            "id": model_dir.name,
                            "name": metadata.get("model_name", model_dir.name),
                            "description": metadata.get("description", ""),
                            "created_at": metadata.get("created_at", ""),
                            "version": metadata.get("version", "1.0.0")
                        })
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur lecture métadonnées {model_dir}: {e}")
        
        return models
    
    def delete_model(self, model_id: str) -> bool:
        """Supprime un modèle entraîné."""
        model_path = self.models_dir / model_id
        
        if not model_path.exists():
            logger.error(f"❌ Modèle non trouvé: {model_id}")
            return False
        
        try:
            import shutil
            shutil.rmtree(model_path)
            logger.info(f"✅ Modèle supprimé: {model_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur suppression: {e}")
            return False

# Instance globale
training_manager = TrainingManager()
