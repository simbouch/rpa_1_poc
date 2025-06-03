import streamlit as st
import tempfile
import spacy
from extraction import extraire_infos

# Titre de l’application
st.set_page_config(page_title="IA : Extraction PDF", layout="centered")
st.title("Prototype IA : Extraction de données de documents PDF")

# Chargement du modèle SpaCy au démarrage
@st.cache_resource(show_spinner=False)
def load_spacy_model():
    try:
        return spacy.load("fr_core_news_md")
    except OSError:
        st.error(
            "❌ Le modèle SpaCy 'fr_core_news_md' n'est pas installé en production.\n"
            "Ajoutez dans `requirements.txt` :\n"
            "    spacy>=3.0.0\n"
            "    fr_core_news_md @ https://github.com/explosion/spacy-models/releases/download/"
            "fr_core_news_md-3.8.0/fr_core_news_md-3.8.0-py3-none-any.whl\n"
            "Puis redeployez l’application."
        )
        return None

nlp = load_spacy_model()
if not nlp:
    st.stop()

# Uploader de fichier PDF
uploaded_file = st.file_uploader("📄 Télécharger un rapport PDF", type=["pdf"])

if uploaded_file:
    # Enregistrement temporaire du PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        chemin_temp = tmp_file.name

    # Indicateur de traitement
    with st.spinner("Extraction en cours..."):
        try:
            donnees = extraire_infos(chemin_temp)
        except Exception as e:
            st.error(f"❌ Une erreur est survenue lors de l'extraction :\n{e}")
        else:
            st.success("Extraction réussie ✅")
            st.json(donnees)
