import os

def create_training_structure(base_path="training"):
    folders = [
        "data/raw",              # Textes bruts à annoter
        "data/spacy_format",     # Fichiers .spacy convertis
        "model_output",          # Modèle entraîné
        "scripts"                # Scripts d'entraînement, conversion, etc.
    ]

    for folder in folders:
        full_path = os.path.join(base_path, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"✅ Dossier créé : {full_path}")

if __name__ == "__main__":
    create_training_structure()
