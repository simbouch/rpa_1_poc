import streamlit as st
from extraction import extraire_infos
import tempfile

st.title("Prototype IA : Extraction de données de documents PDF")

uploaded_file = st.file_uploader("📄 Télécharger un rapport PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        chemin_temp = tmp_file.name

    st.info("Extraction en cours...")
    donnees = extraire_infos(chemin_temp)
    
    st.success("Extraction réussie ✅")
    st.json(donnees)
