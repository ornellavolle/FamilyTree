import streamlit as st
import json

st.set_page_config(
    page_title="Arbre Généalogique · Famille Piponnier",
    page_icon="🌳",
    layout="wide",
)

# ─── CSS global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500&family=Inter:wght@300;400;500&display=swap');
html, body, [class*="css"]          { font-family: 'Inter', sans-serif; }
.main                               { background: #FAF8F5; }
.block-container                    { padding-top: 1.5rem; padding-bottom: 1rem; }
section[data-testid="stSidebar"]    { background: #FFFFFF; border-right: 1px solid #E8E5E0; }
section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
h1 { font-family:'Playfair Display',serif!important; font-weight:400!important; color:#2A2A2A!important; }
.relation-box  { background:#FAF8F5; border:1px solid #E8E5E0; border-radius:8px; padding:12px 14px; font-size:13px; color:#555; line-height:1.9; }
.legend-dot    { display:inline-block; width:12px; height:12px; border-radius:2px; margin-right:6px; vertical-align:middle; }
.detail-card   { background:#FFF; border:1px solid #E8E5E0; border-radius:10px; padding:16px; margin-top:12px; }
.detail-avatar { width:52px; height:52px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:600; margin-bottom:12px; }
.detail-name   { font-size:16px; font-weight:600; color:#2A2A2A; margin-bottom:2px; }
.detail-role   { font-size:12px; color:#999; margin-bottom:12px; }
.detail-row    { display:flex; gap:6px; font-size:13px; color:#555; margin-bottom:6px; }
.detail-label  { color:#999; min-width:80px; font-size:12px; }
.detail-sect   { font-size:11px; letter-spacing:1px; text-transform:uppercase; color:#999; margin:10px 0 5px; }
.rel-tag       { font-size:10px; color:#999; background:#F3F4F6; padding:1px 6px; border-radius:10px; }
.story-area    { background:#FAF8F5; border:1px solid #E8E5E0; border-radius:8px; padding:14px; margin-top:10px; font-size:13px; color:#444; line-height:1.8; }
hr             { border:none; border-top:1px solid #EEE; margin:1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── DONNÉES ──────────────────────────────────────────────────────────────────
PERSONS = {
    1: {"name": "François Piponnier", "birth": "", "death": "28/01/1870", "place": "Simandre", "gender": "m"},
    2: {"name": "Claudine Varnois", "birth": "", "death": "", "place": "", "gender": "f"},
    3: {"name": "Jean Claude Piponnier", "birth": "03/08/1847", "death": "", "place": "Simandre", "gender": "m"},
    4: {"name": "Marie Catherine Laurent", "birth": "05/03/1839", "death": "", "place": "", "gender": "f"},
    5: {"name": "Jean Claude Piponnier", "birth": "09/07/1876", "death": "", "place": "", "gender": "m"},
    6: {"name": "Louise Piponnier", "birth": "10/04/1884", "death": "", "place": "", "gender": "f"},
    7: {"name": "Marie Piponnier", "birth": "10/10/1885", "death": "", "place": "", "gender": "f"},
    8: {"name": "Jean Marie Piponnier", "birth": "30/10/1888", "death": "", "place": "", "gender": "m"},
    9: {"name": "Henriette Morin", "birth": "", "death": "", "place": "", "gender": "f"},
    10: {"name": "Francis Piponnier", "birth": "30/08/1890", "death": "", "place": "", "gender": "m"},
    11: {"name": "Marguerite Piponnier", "birth": "18/09/1895", "death": "", "place": "", "gender": "f"},
    12: {"name": "Hortense Piponnier", "birth": "", "death": "", "place": "", "gender": "f"},
    13: {"name": "Francis Pourprix", "birth": "", "death": "", "place": "", "gender": "m"},
    14: {"name": "Nicole Pourprix", "birth": "23/08/1943", "death": "", "place": "", "gender": "f"},
    15: {"name": "Marie-France Pourprix", "birth": "", "death": "", "place": "", "gender": "f"},
    16: {"name": "Mohamed El ralenti", "birth": "", "death": "", "place": "", "gender": "m"},
    17: {"name": "Florence El ralenti", "birth": "", "death": "", "place": "", "gender": "f"},
    18: {"name": "Natalie El ralenti", "birth": "", "death": "", "place": "", "gender": "f"},
    19: {"name": "Barchive El ralenti", "birth": "02/05/1972", "death": "", "place": "", "gender": "f"},
    20: {"name": "Régis Volle", "birth": "23/03/1977", "death": "", "place": "", "gender": "m"},
    21: {"name": "Jeanne Marie DuBuisson", "birth": "", "death": "", "place": "", "gender": "f"},
}

FILIATIONS = [
    (1,3),(2,3),
    (3,5),(4,5),(3,6),(4,6),(3,7),(4,7),(3,8),(4,8),(3,10),(4,10),(3,11),(4,11),
    (8,12),(9,12),
    (12,14),(13,14),(12,15),(13,15),
    (14,17),(16,17),(14,18),(16,18),(14,19),(16,19),
]

UNIONS = {
    "1-2": {"a": 1, "b": 2, "date": ""},
    "3-4": {"a": 3, "b": 4, "date": "ca. 1875"},
    "8-9": {"a": 8, "b": 9, "date": ""},
    "10-21": {"a": 10, "b": 21, "date": ""},
    "12-13": {"a": 12, "b": 13, "date": ""},
    "14-16": {"a": 14, "b": 16, "date": "ca. 1970"},
    "19-20": {"a": 19, "b": 20, "date": "ca. 2000"},
}

ROLE_STYLES = {
    "self": {"fill": "#FEF3C7", "stroke": "#D97706", "text": "#92400E"},
    "parent": {"fill": "#DBEAFE", "stroke": "#3B82F6", "text": "#1E40AF"},
    "grand-parent": {"fill": "#C7D7FD", "stroke": "#4F46E5", "text": "#312E81"},
    "arrière grand-parent": {"fill": "#B5C5FB", "stroke": "#3730A3", "text": "#1E1B4B"},
    "conjoint(e)": {"fill": "#FCE7F3", "stroke": "#EC4899", "text": "#831843"},
    "enfant": {"fill": "#D1FAE5", "stroke": "#10B981", "text": "#064E3B"},
    "neutre": {"fill": "#F3F4F6", "stroke": "#9CA3AF", "text": "#374151"},
}

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "chosen_id" not in st.session_state:
    st.session_state.chosen_id = 18
if "view_all" not in st.session_state:
    st.session_state.view_all = False

# ─── TITRE ────────────────────────────────────────────────────────────────────
st.markdown("# 🌳 Arbre Généalogique · Famille Piponnier")

st.info("Version simplifiée : génération d’histoires supprimée.")

# 👉 Ici ton arbre HTML/JS reste IDENTIQUE (inchangé)
# (je ne le réécris pas pour éviter 2000 lignes inutiles)

# ─── PANNEAU DÉTAIL ───────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 👤 Fiche détaillée")

    detail_name = st.selectbox(
        "Sélectionner une personne",
        [p["name"] for p in PERSONS.values()],
    )

    detail_id = [k for k,v in PERSONS.items() if v["name"] == detail_name][0]
    info = PERSONS[detail_id]

    st.markdown(f"""
    <div class='detail-card'>
        <div class='detail-name'>{info["name"]}</div>
        <div class='detail-role'>{'Homme' if info['gender']=='m' else 'Femme'}</div>
        <div class='detail-row'><span class='detail-label'>Naissance</span>{info['birth']}</div>
        <div class='detail-row'><span class='detail-label'>Décès</span>{info['death']}</div>
        <div class='detail-row'><span class='detail-label'>Lieu</span>{info['place']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📖 Récit de vie")
    st.markdown(
        "<div class='story-area'>"
        "Fonction supprimée (génération d’histoire désactivée)."
        "</div>",
        unsafe_allow_html=True,
    )