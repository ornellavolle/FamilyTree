import streamlit as st
import json

st.set_page_config(
    page_title="Arbre Généalogique · Famille Piponnier",
    page_icon="",
    layout="wide",
)

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
    "1-2": {"a":1,"b":2,"date":""},
    "3-4": {"a":3,"b":4,"date":"ca. 1875"},
    "8-9": {"a":8,"b":9,"date":""},
    "10-21": {"a":10,"b":21,"date":""},
    "12-13": {"a":12,"b":13,"date":""},
    "14-16": {"a":14,"b":16,"date":"ca. 1970"},
    "19-20": {"a":19,"b":20,"date":"ca. 2000"},
}

# ─── STORY SANS IA ────────────────────────────────────────────────────────────
def generate_story(pid: int) -> str:
    info = PERSONS[pid]
    name = info["name"]
    birth = info["birth"] or "au XIXe siècle"
    place = info["place"] or "dans sa région natale"

    return f"""
{name} est né(e) {birth} {place}. Issu(e) de la famille Piponnier, il/elle a grandi dans un environnement marqué par les traditions et la transmission.

Au fil du temps, {name.split()[0]} a construit sa vie entouré(e) de ses proches. Les relations familiales ont joué un rôle central dans son parcours.

Son histoire s'inscrit dans une lignée familiale riche, reliant les générations entre elles avec continuité et mémoire.
"""

# ─── JSON FIX ─────────────────────────────────────────────────────────────────
persons_json = json.dumps(PERSONS)
filiations_json = json.dumps(FILIATIONS)

unions_json = json.dumps({
    k: {"a": v["a"], "b": v["b"], "date": v["date"]}
    for k, v in UNIONS.items()
})

# ─── UI ───────────────────────────────────────────────────────────────────────
st.title("🌳 Arbre Généalogique · Famille Piponnier")

tree_html = f"""
<div id="wrap">
<svg viewBox="0 0 800 400"></svg>
</div>

<script>
const P = {persons_json};
const FILIATIONS = {filiations_json};
const UNIONS = {unions_json};

console.log("OK :", P, FILIATIONS, UNIONS);
</script>
"""

st.components.v1.html(tree_html, height=400)

# ─── TEST STORY ───────────────────────────────────────────────────────────────
st.markdown("## 📖 Test récit")
pid = st.selectbox("Choisir une personne", list(PERSONS.keys()))
if st.button("Générer"):
    st.write(generate_story(pid))