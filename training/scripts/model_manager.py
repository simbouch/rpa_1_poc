#!/usr/bin/env python3
"""
Gestionnaire de modèles pour l'extraction PDF.
Permet de gérer les versions, évaluer les performances et déployer les modèles.
"""

import os
import json
import shutil
import spacy
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    """Gestionnaire de modèles NER pour l'extraction PDF."""

    def __init__(self, base_path: str = "models"):
        self.base_path = Path(base_path)
        self.models_dir = Path(base_path)
        self.models_dir.mkdir(exist_ok=True)

        # Modèles disponibles
        self.available_models = {
            "general": "models/general_model",
            "medical": "models/medical_model",
            "legal": "models/legal_model"
        }
    
    def list_models(self) -> List[Dict]:
        """Liste tous les modèles disponibles avec leurs métadonnées."""
        models = []
        
        # Modèle actif
        if self.active_model_path.exists():
            info = self._get_model_info(self.active_model_path)
            info["name"] = "active"
            info["path"] = str(self.active_model_path)
            models.append(info)
        
        # Modèles archivés
        if self.models_dir.exists():
            for model_dir in self.models_dir.iterdir():
                if model_dir.is_dir():
                    info = self._get_model_info(model_dir)
                    info["name"] = model_dir.name
                    info["path"] = str(model_dir)
                    models.append(info)
        
        return models
    
    def _get_model_info(self, model_path: Path) -> Dict:
        """Récupère les informations d'un modèle."""
        info = {
            "created_at": None,
            "version": "unknown",
            "labels": [],
            "description": "",
            "performance": {}
        }
        
        # Lire le fichier d'info s'il existe
        info_file = model_path / "model_info.json"
        if info_file.exists():
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    saved_info = json.load(f)
                    info.update(saved_info)
            except Exception as e:
                logger.warning(f"Impossible de lire {info_file}: {e}")
        
        # Informations du système de fichiers
        if model_path.exists():
            info["size_mb"] = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file()) / (1024*1024)
            info["created_at"] = datetime.fromtimestamp(model_path.stat().st_mtime).isoformat()
        
        return info
    
    def archive_model(self, version_name: str, description: str = "") -> bool:
        """Archive le modèle actuel avec un nom de version."""
        if not self.active_model_path.exists():
            logger.error("Aucun modèle actif à archiver")
            return False
        
        archive_path = self.models_dir / version_name
        
        if archive_path.exists():
            logger.error(f"La version {version_name} existe déjà")
            return False
        
        try:
            # Copier le modèle
            shutil.copytree(self.active_model_path, archive_path)
            
            # Mettre à jour les métadonnées
            info = self._get_model_info(archive_path)
            info["version"] = version_name
            info["description"] = description
            info["archived_at"] = datetime.now().isoformat()
            
            info_file = archive_path / "model_info.json"
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Modèle archivé: {version_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'archivage: {e}")
            return False
    
    def restore_model(self, version_name: str) -> bool:
        """Restaure un modèle archivé comme modèle actif."""
        archive_path = self.models_dir / version_name
        
        if not archive_path.exists():
            logger.error(f"Version {version_name} non trouvée")
            return False
        
        try:
            # Sauvegarder le modèle actuel s'il existe
            if self.active_model_path.exists():
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.archive_model(backup_name, "Sauvegarde automatique avant restauration")
            
            # Supprimer le modèle actuel
            if self.active_model_path.exists():
                shutil.rmtree(self.active_model_path)
            
            # Copier le modèle archivé
            shutil.copytree(archive_path, self.active_model_path)
            
            logger.info(f"✅ Modèle {version_name} restauré comme modèle actif")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la restauration: {e}")
            return False
    
    def evaluate_model(self, model_path: Optional[str] = None) -> Dict:
        """Évalue les performances d'un modèle."""
        if model_path is None:
            model_path = str(self.active_model_path)
        
        if not os.path.exists(model_path):
            logger.error(f"Modèle non trouvé: {model_path}")
            return {}
        
        try:
            # Charger le modèle
            nlp = spacy.load(model_path)
            
            # Tests de base
            test_cases = [
                {
                    "text": "Nom : MARTIN JEAN\nRéférence : 2025-TEST/01-A\nObjet : Test d'analyse\nDate : 15/06/2025\nDemandeur : Service test",
                    "expected": {
                        "nom_personne": "MARTIN JEAN",
                        "reference_dossier": "2025-TEST/01-A",
                        "type_analyse": "Test d'analyse",
                        "date_prelevement": "15/06/2025",
                        "service_demandeur": "Service test"
                    }
                },
                {
                    "text": "Patient : DURAND MARIE\nDossier : 2025-LAB/02-B\nAnalyse : Examen sanguin\nPrélèvement : 20/06/2025\nService : Laboratoire",
                    "expected": {
                        "nom_personne": "DURAND MARIE",
                        "reference_dossier": "2025-LAB/02-B",
                        "type_analyse": "Examen sanguin",
                        "date_prelevement": "20/06/2025",
                        "service_demandeur": "Laboratoire"
                    }
                }
            ]
            
            results = {
                "total_tests": len(test_cases),
                "passed": 0,
                "failed": 0,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "details": []
            }
            
            total_expected = 0
            total_found = 0
            total_correct = 0
            
            for i, test_case in enumerate(test_cases):
                doc = nlp(test_case["text"])
                found_entities = {ent.label_: ent.text for ent in doc.ents}
                expected_entities = test_case["expected"]
                
                test_result = {
                    "test_id": i + 1,
                    "expected": expected_entities,
                    "found": found_entities,
                    "correct": 0,
                    "missing": [],
                    "extra": []
                }
                
                # Comparer les entités
                for label, expected_text in expected_entities.items():
                    total_expected += 1
                    if label in found_entities:
                        total_found += 1
                        if found_entities[label].strip().lower() == expected_text.strip().lower():
                            total_correct += 1
                            test_result["correct"] += 1
                        else:
                            test_result["missing"].append(f"{label}: expected '{expected_text}', got '{found_entities[label]}'")
                    else:
                        test_result["missing"].append(f"{label}: '{expected_text}'")
                
                # Entités supplémentaires
                for label in found_entities:
                    if label not in expected_entities:
                        test_result["extra"].append(f"{label}: '{found_entities[label]}'")
                
                if len(test_result["missing"]) == 0 and len(test_result["extra"]) == 0:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                
                results["details"].append(test_result)
            
            # Calculer les métriques
            if total_expected > 0:
                results["recall"] = total_correct / total_expected
            if total_found > 0:
                results["precision"] = total_correct / total_found
            if results["precision"] + results["recall"] > 0:
                results["f1_score"] = 2 * (results["precision"] * results["recall"]) / (results["precision"] + results["recall"])
            
            logger.info(f"✅ Évaluation terminée: {results['passed']}/{results['total_tests']} tests réussis")
            logger.info(f"📊 Métriques: P={results['precision']:.2f}, R={results['recall']:.2f}, F1={results['f1_score']:.2f}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'évaluation: {e}")
            return {"error": str(e)}
    
    def cleanup_old_models(self, keep_count: int = 5) -> int:
        """Supprime les anciens modèles archivés, en gardant les plus récents."""
        if not self.models_dir.exists():
            return 0
        
        # Lister tous les modèles avec leur date de création
        models = []
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                models.append((model_dir, model_dir.stat().st_mtime))
        
        # Trier par date (plus récent en premier)
        models.sort(key=lambda x: x[1], reverse=True)
        
        # Supprimer les anciens
        deleted_count = 0
        for model_dir, _ in models[keep_count:]:
            try:
                shutil.rmtree(model_dir)
                logger.info(f"🗑️ Modèle supprimé: {model_dir.name}")
                deleted_count += 1
            except Exception as e:
                logger.warning(f"⚠️ Impossible de supprimer {model_dir.name}: {e}")
        
        return deleted_count
    
    def export_model(self, output_path: str, version_name: Optional[str] = None) -> bool:
        """Exporte un modèle vers un fichier archive."""
        if version_name:
            source_path = self.models_dir / version_name
        else:
            source_path = self.active_model_path
        
        if not source_path.exists():
            logger.error(f"Modèle non trouvé: {source_path}")
            return False
        
        try:
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', source_path)
            logger.info(f"✅ Modèle exporté: {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'export: {e}")
            return False

def main():
    """Interface en ligne de commande pour le gestionnaire de modèles."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestionnaire de modèles NER")
    parser.add_argument("action", choices=["list", "archive", "restore", "evaluate", "cleanup", "export"])
    parser.add_argument("--name", help="Nom de version pour archive/restore")
    parser.add_argument("--description", help="Description pour l'archivage")
    parser.add_argument("--output", help="Chemin de sortie pour l'export")
    parser.add_argument("--keep", type=int, default=5, help="Nombre de modèles à garder lors du cleanup")
    
    args = parser.parse_args()
    
    manager = ModelManager()
    
    if args.action == "list":
        models = manager.list_models()
        print(f"📋 {len(models)} modèle(s) trouvé(s):")
        for model in models:
            print(f"  - {model['name']}: {model.get('description', 'Pas de description')}")
            print(f"    Créé: {model.get('created_at', 'Inconnu')}")
            print(f"    Taille: {model.get('size_mb', 0):.1f} MB")
    
    elif args.action == "archive":
        if not args.name:
            print("❌ --name requis pour l'archivage")
            return
        success = manager.archive_model(args.name, args.description or "")
        print("✅ Archivage réussi" if success else "❌ Échec de l'archivage")
    
    elif args.action == "restore":
        if not args.name:
            print("❌ --name requis pour la restauration")
            return
        success = manager.restore_model(args.name)
        print("✅ Restauration réussie" if success else "❌ Échec de la restauration")
    
    elif args.action == "evaluate":
        results = manager.evaluate_model()
        if "error" in results:
            print(f"❌ Erreur: {results['error']}")
        else:
            print(f"📊 Résultats: {results['passed']}/{results['total_tests']} tests réussis")
            print(f"   Précision: {results['precision']:.2f}")
            print(f"   Rappel: {results['recall']:.2f}")
            print(f"   F1-Score: {results['f1_score']:.2f}")
    
    elif args.action == "cleanup":
        deleted = manager.cleanup_old_models(args.keep)
        print(f"🗑️ {deleted} ancien(s) modèle(s) supprimé(s)")
    
    elif args.action == "export":
        if not args.output:
            print("❌ --output requis pour l'export")
            return
        success = manager.export_model(args.output, args.name)
        print("✅ Export réussi" if success else "❌ Échec de l'export")

if __name__ == "__main__":
    main()
