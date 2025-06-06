import streamlit as st
import tempfile
import os
import json
from datetime import datetime
from extraction_enhanced import PDFExtractor

# Configuration de la page
st.set_page_config(
    page_title="🧠 IA : Extraction PDF Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🧠 Prototype IA : Extraction de données de documents PDF")
st.markdown("### 🚀 Système professionnel multi-modèles pour l'extraction automatique")
st.markdown("---")

# Sidebar pour la configuration
st.sidebar.header("⚙️ Configuration du modèle")

# Fonction pour détecter les modèles disponibles
@st.cache_data
def get_available_models():
    """Détecte tous les modèles disponibles."""
    models = {}

    # Modèle spaCy par défaut
    try:
        import spacy
        spacy.load("fr_core_news_md")
        models["spacy_default"] = {
            "name": "📚 Modèle spaCy par défaut",
            "description": "Modèle français général de spaCy",
            "path": None,
            "type": "default"
        }
    except:
        pass

    # Modèle général entraîné
    if os.path.exists("models/general_model"):
        models["general"] = {
            "name": "🎯 Modèle général entraîné",
            "description": "Modèle entraîné pour documents généraux",
            "path": "models/general_model",
            "type": "trained"
        }

    # Modèle médical
    if os.path.exists("models/medical_model"):
        models["medical"] = {
            "name": "🏥 Modèle médical spécialisé",
            "description": "Modèle spécialisé pour rapports médicaux",
            "path": "models/medical_model",
            "type": "trained"
        }

    # Modèle juridique
    if os.path.exists("models/legal_model"):
        models["legal"] = {
            "name": "⚖️ Modèle juridique spécialisé",
            "description": "Modèle spécialisé pour documents juridiques",
            "path": "models/legal_model",
            "type": "trained"
        }

    return models

# Chargement des modèles disponibles
available_models = get_available_models()

if not available_models:
    st.sidebar.error("❌ Aucun modèle disponible")
    st.stop()

# Sélection du modèle
selected_model_id = st.sidebar.selectbox(
    "Choisir le modèle d'extraction:",
    options=list(available_models.keys()),
    format_func=lambda x: available_models[x]["name"],
    index=0
)

selected_model = available_models[selected_model_id]

# Affichage des informations du modèle
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Informations du modèle")
st.sidebar.info(f"**Type:** {selected_model['description']}")

if selected_model["type"] == "trained" and selected_model["path"]:
    metadata_path = f"{selected_model['path']}/model_info.json"
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            st.sidebar.success("✅ Modèle personnalisé actif")
            st.sidebar.info(f"**Version:** {metadata.get('version', 'N/A')}")
            st.sidebar.info(f"**Créé:** {metadata.get('created_at', 'N/A')[:10]}")
            if "performance" in metadata:
                perf = metadata["performance"]
                st.sidebar.info(f"**Précision:** {perf.get('precision', 0):.2%}")
        except:
            pass
else:
    st.sidebar.info("📚 Modèle spaCy par défaut")

# Options d'affichage
st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Options d'affichage")
show_metadata = st.sidebar.checkbox("Afficher les métadonnées", value=True)
show_confidence = st.sidebar.checkbox("Afficher les scores", value=False)

# Section gestion des modèles
st.sidebar.markdown("---")
st.sidebar.subheader("🚀 Gestion des modèles")
st.sidebar.info(f"**Modèles disponibles:** {len(available_models)}")

if st.sidebar.button("🔄 Actualiser les modèles"):
    st.cache_data.clear()
    st.rerun()

# Fonction pour charger l'extracteur
@st.cache_resource
def load_extractor(model_path):
    """Charge l'extracteur avec le modèle spécifié."""
    try:
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
        help="Formats supportés: PDF uniquement. Taille max: 200MB"
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

    # Statistiques du modèle
    if selected_model["type"] == "trained":
        st.markdown("### 📊 Performances")
        metadata_path = f"{selected_model['path']}/model_info.json"
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                if "performance" in metadata:
                    perf = metadata["performance"]
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Précision", f"{perf.get('precision', 0):.1%}")
                    with col_b:
                        st.metric("Rappel", f"{perf.get('recall', 0):.1%}")
            except:
                pass

# Traitement du fichier
if uploaded_file:
    # Charger l'extracteur avec le modèle sélectionné
    model_path = selected_model["path"]
    extracteur = load_extractor(model_path)

    if not extracteur:
        st.stop()

    # Enregistrement temporaire du PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        chemin_temp = tmp_file.name

    # Affichage des informations du fichier
    st.markdown("---")
    st.subheader("📋 Informations du fichier")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nom", uploaded_file.name[:20] + "..." if len(uploaded_file.name) > 20 else uploaded_file.name)
    with col2:
        st.metric("Taille", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("Type", uploaded_file.type)
    with col4:
        st.metric("Modèle", selected_model["name"].split()[1])

    # Extraction
    st.markdown("---")
    st.subheader("🔍 Résultats de l'extraction")

    with st.spinner(f"Analyse en cours avec {selected_model['name']}..."):
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

            # Statistiques d'extraction
            st.info(f"**Méthode utilisée:** {metadata.get('extraction_method', 'N/A').title()}")

            # Boutons de téléchargement
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # JSON
            json_data = json.dumps(donnees, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Télécharger JSON",
                data=json_data,
                file_name=f"extraction_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )

            # CSV
            csv_data = "Champ,Valeur\n" + "\n".join([f'"{k}","{v}"' for k, v in donnees.items()])
            st.download_button(
                label="📊 Télécharger CSV",
                data=csv_data,
                file_name=f"extraction_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
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
        os.unlink(chemin_temp)
    except:
        pass

# Footer avec informations
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📚 Technologies")
    st.markdown("""
    - **spaCy** - NLP et NER
    - **pdfplumber** - Extraction PDF
    - **Streamlit** - Interface web
    - **Python** - Backend
    """)

with col2:
    st.markdown("### 🎯 Modèles disponibles")
    for model_id, model_info in available_models.items():
        icon = "✅" if model_id == selected_model_id else "⚪"
        st.markdown(f"{icon} {model_info['name']}")

with col3:
    st.markdown("### 🚀 Fonctionnalités")
    st.markdown("""
    - **Multi-modèles** - Choix du modèle
    - **Extraction robuste** - NER + Regex
    - **Export multiple** - JSON, CSV
    - **Interface moderne** - Streamlit
    """)

st.markdown("---")
st.markdown("**Développé par :** Équipe RPA - Prototype v2.0 Professional")
