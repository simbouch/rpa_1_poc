import pdfplumber
import spacy
import re

nlp = spacy.load("fr_core_news_md")

def lire_pdf(chemin_fichier):
    with pdfplumber.open(chemin_fichier) as pdf:
        texte = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return texte

def extraire_infos(chemin_fichier):
    texte = lire_pdf(chemin_fichier)
    doc = nlp(texte)

    # Initialisation
    nom_prenom = None
    reference = re.search(r"Référence\s?:\s?([\w\d\-\/]+)", texte)
    type_analyse = re.search(r"Objet\s?:\s?(.+)", texte)
    
    # Détection avancée de la date de prélèvement
    date = re.search(r"(Date de prélèvement|Date)\s?:\s?(\d{2}/\d{2}/\d{4})", texte)
    date_prelevement = date.group(2) if date else None

    # Détection du service demandeur
    service = re.search(r"Demandeur\s?:\s?(Police|Gendarmerie)", texte, re.IGNORECASE)
    service_demandeur = service.group(1).capitalize() if service else None

    # Détection robuste du nom : d'abord le champ "Nom :", sinon NLP
    champ_nom = re.search(r"Nom\s?:\s?([A-Z\s\-]+)", texte)
    if champ_nom:
        nom_prenom = champ_nom.group(1).strip()
    else:
        # Cherche la première entité de type "PER" hors contexte "Agent" ou "Demandeur"
        for ent in doc.ents:
            if ent.label_ == "PER" and "agent" not in ent.sent.text.lower() and "demandeur" not in ent.sent.text.lower():
                nom_prenom = ent.text.upper()
                break

    return {
        "nom_prenom": nom_prenom,
        "reference_dossier": reference.group(1) if reference else None,
        "type_prelevement": type_analyse.group(1).strip() if type_analyse else None,
        "date_prelevement": date_prelevement,
        "service_demandeur": service_demandeur
    }
