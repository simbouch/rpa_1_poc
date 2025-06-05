import streamlit as st
import tempfile
import os
import json
from datetime import datetime
from extraction_enhanced import PDFExtractor, get_available_models

# Configuration de la page
st.set_page_config(
    page_title="🧠 IA : Extraction PDF",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🧠 Prototype IA : Extraction de données de documents PDF")
st.markdown("### 🚀 Extraction automatique d'informations depuis des rapports PDF")
st.markdown("---")

# Sidebar pour la configuration
st.sidebar.header("⚙️ Configuration")

# Sélection du modèle
available_models = get_available_models()
if available_models:
    model_options = {}
    for model in available_models:
        if "model-best" in model:
            model_options["🎯 Modèle entraîné (recommandé)"] = model
        else:
            model_options["📚 Modèle par défaut (fr_core_news_md)"] = model

    if len(model_options) > 0:
        selected_model_name = st.sidebar.selectbox(
            "Choisir le modèle d'extraction:",
            options=list(model_options.keys()),
            index=0 if "🎯 Modèle entraîné (recommandé)" in model_options else 0
        )
        selected_model_path = model_options[selected_model_name]
    else:
        st.sidebar.error("❌ Aucun modèle disponible")
        st.stop()
else:
    st.sidebar.error("❌ Aucun modèle disponible")
    st.stop()

# Options d'affichage
show_metadata = st.sidebar.checkbox("Afficher les métadonnées", value=True)
show_confidence = st.sidebar.checkbox("Afficher les scores de confiance", value=False)

# Informations sur le modèle sélectionné
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Informations du modèle")
if "model-best" in selected_model_path:
    st.sidebar.success("✅ Modèle personnalisé actif")
    model_info_path = "training/model_output/model_info.json"
    if os.path.exists(model_info_path):
        try:
            with open(model_info_path, 'r', encoding='utf-8') as f:
                model_info = json.load(f)
            st.sidebar.info(f"Version: {model_info.get('version', 'N/A')}")
            st.sidebar.info(f"Créé: {model_info.get('created_at', 'N/A')}")
        except:
            pass
else:
    st.sidebar.info("📚 Modèle spaCy par défaut")

# Chargement du modèle
@st.cache_resource(show_spinner=False)
def load_extractor(model_path):
    """Charge l'extracteur avec le modèle spécifié."""
    try:
        if "fr_core_news_md" in model_path:
            return PDFExtractor(None)  # Utilise le modèle par défaut
        else:
            return PDFExtractor(model_path)
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle: {e}")
        return None

# Interface principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📄 Upload de document")
    uploaded_file = st.file_uploader(
        "Télécharger un rapport PDF à analyser",
        type=["pdf"],
        help="Formats supportés: PDF uniquement"
    )

with col2:
    st.header("🎯 Champs extraits")
    st.markdown("""
    - **Nom/Prénom** de la personne
    - **Référence** du dossier
    - **Type d'analyse** ou prélèvement
    - **Date** de prélèvement
    - **Service** demandeur
    """)

# Traitement du fichier
if uploaded_file:
    # Charger l'extracteur
    extracteur = load_extractor(selected_model_path)
    if not extracteur:
        st.stop()
    
    # Enregistrement temporaire du PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        chemin_temp = tmp_file.name

    # Affichage des informations du fichier
    st.markdown("---")
    st.subheader("📋 Informations du fichier")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nom du fichier", uploaded_file.name)
    with col2:
        st.metric("Taille", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("Type", uploaded_file.type)

    # Extraction
    st.markdown("---")
    st.subheader("🔍 Résultats de l'extraction")
    
    with st.spinner("Analyse en cours..."):
        try:
            start_time = datetime.now()
            donnees = extracteur.extraire_infos(chemin_temp)
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
        except Exception as e:
            st.error(f"❌ Une erreur est survenue lors de l'extraction :\n{e}")
            st.stop()

    # Affichage des résultats
    if donnees:
        st.success(f"✅ Extraction réussie en {processing_time:.2f} secondes")
        
        # Métadonnées
        metadata = donnees.pop("_metadata", {})
        
        # Résultats principaux
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Données extraites")
            
            # Affichage structuré des résultats
            for field, value in donnees.items():
                if value:
                    st.success(f"**{field.replace('_', ' ').title()}**: {value}")
                else:
                    st.warning(f"**{field.replace('_', ' ').title()}**: Non trouvé")
        
        with col2:
            st.markdown("### 📁 Export des données")
            
            # Bouton de téléchargement JSON
            json_data = json.dumps(donnees, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Télécharger en JSON",
                data=json_data,
                file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Bouton de téléchargement CSV
            csv_data = "\n".join([f"{k},{v}" for k, v in donnees.items()])
            st.download_button(
                label="📊 Télécharger en CSV",
                data=csv_data,
                file_name=f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Métadonnées (si activées)
        if show_metadata and metadata:
            st.markdown("---")
            st.subheader("🔧 Métadonnées techniques")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Méthode", metadata.get("extraction_method", "N/A"))
            with col2:
                st.metric("Champs modèle", metadata.get("model_fields", 0))
            with col3:
                st.metric("Champs regex", metadata.get("regex_fields", 0))
            with col4:
                st.metric("Longueur texte", f"{metadata.get('text_length', 0)} chars")
        
        # Affichage JSON complet
        with st.expander("🔍 Voir les données brutes (JSON)"):
            st.json(donnees)
    
    else:
        st.warning("⚠️ Aucune donnée extraite du document")

# Nettoyage
try:
    if 'chemin_temp' in locals():
        os.unlink(chemin_temp)
except:
    pass

# Footer avec informations
st.markdown("---")
st.markdown("""
### 📚 À propos
Cette application utilise l'intelligence artificielle pour extraire automatiquement des informations 
structurées depuis des documents PDF. Elle combine des modèles de traitement du langage naturel (NLP) 
avec des techniques de reconnaissance d'entités nommées (NER).

**Technologies utilisées:**
- spaCy pour le traitement du langage naturel
- pdfplumber pour l'extraction de texte PDF
- Streamlit pour l'interface utilisateur

**Développé par:** Équipe RPA - Prototype v1.0
""")
