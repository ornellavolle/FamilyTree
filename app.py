"""
Arbre Généalogique · Famille Piponnier
Lancer avec : streamlit run app.py

Dépendances : streamlit, anthropic
Installation : pip install streamlit anthropic
"""

import streamlit as st
import anthropic
import json

st.set_page_config(
    page_title="Arbre Généalogique",
    page_icon="",
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
    1:  {"name": "François Piponnier",       "birth": "",           "death": "28/01/1870", "place": "Simandre", "gender": "m"},
    2:  {"name": "Claudine Varnois",          "birth": "",           "death": "",           "place": "",         "gender": "f"},
    3:  {"name": "Jean Claude Piponnier",     "birth": "02/08/1847", "death": "",           "place": "Catheniére commune de Simandre", "gender": "m"},
    4:  {"name": "Marie Catherine Laurent",   "birth": "05/03/1858", "death": "",           "place": "",         "gender": "f"},
    5:  {"name": "Jean Claude Piponnier",     "birth": "09/01/1879", "death": "4/10/1918",           "place": "Saint-Quentin, 02691, Aisne, Picardie, France",         "gender": "m"},
    6:  {"name": "Louise Piponnier",          "birth": "10/04/1884", "death": "après 1936",           "place": "Gigny-sur-Saône, 71219, Saône-et-Loire, Bourgogne, France",         "gender": "f"},
    7:  {"name": "Marie Piponnier",           "birth": "10/10/1885", "death": "",           "place": "",         "gender": "f"},
    8:  {"name": "Jean Marie Piponnier",      "birth": "30/10/1887", "death": "25/03/1977", "place": "Cuisery, France",         "gender": "m"},
    9:  {"name": "Henriette Morin",           "birth": "16/04/1891", "death": "",           "place": "",         "gender": "f"},
    10: {"name": "Francis Piponnier",         "birth": "30/08/1890", "death": "",           "place": "",         "gender": "m"},
    11: {"name": "Marguerite Piponnier",      "birth": "18/09/1895", "death": "",           "place": "",         "gender": "f"},
    12: {"name": "Hortense Piponnier",        "birth": "",           "death": "",           "place": "",         "gender": "f"},
    13: {"name": "Francis Pourprix",          "birth": "",           "death": "",           "place": "",         "gender": "m"},
    14: {"name": "Nicole Pourprix",           "birth": "22/08/1943", "death": "",           "place": "",         "gender": "f"},
    15: {"name": "Marie-France Pourprix",     "birth": "",           "death": "",           "place": "",         "gender": "f"},
    16: {"name": "Mohamed El raiani",        "birth": "05/07/1942",           "death": "22/12/2015",           "place": "Cuisery,France",         "gender": "m"},
    17: {"name": "Florence El raiani",       "birth": "",           "death": "",           "place": "",         "gender": "f"},
    18: {"name": "Natalie El raiani",        "birth": "",           "death": "",           "place": "",         "gender": "f"},
    19: {"name": "Sandrine El raiani",       "birth": "02/08/1973", "death": "",           "place": "",         "gender": "f"},
    20: {"name": "Régis Volle",               "birth": "23/03/1977", "death": "",           "place": "",         "gender": "m"},
    21: {"name": "Jeanne Marie DuBuisson",    "birth": "",           "death": "",           "place": "",         "gender": "f"},
    22 : {"name": "Jean Laurent",                "birth": "1830",           "death": "",           "place": "", "gender": "m"},
    23 : {"name": "Anne Viennois",             "birth": "1831",           "death": "",         "place": "", "gender" : "f"},
    24 : {"name": "Ornella Volle",             "birth": "29/12/2003",           "death": "",  "place": "", "gender" : "f"},
    25 : {"name": "Théotime Volle",             "birth": "23/08/2005",           "death": "",  "place": "", "gender" : "m"}, 
    26 : {"name": "Ombeline Volle",             "birth": "30/09/2007",           "death": "", "place": "", "gender" : "f"},
    27 : {"name": "Benedict Carter",             "birth": "",           "death": "", "place": "", "gender" : "m"},
    28 : {"name": "Éloise Carter",             "birth": "",           "death": "", "place": "", "gender" : "f"},
    29 : {"name": "Philibert Baconnet",             "birth": "",           "death": "", "place": "",    "gender" : "m"},
    30 : {"name": "Anne Marie Baconnet né()",             "birth": "",           "death": "", "place": "",    "gender" : "f"},
    31 : {"name": "Claude Marie Piponnier",             "birth": "11/03/1889",           "death": "21/05/1889", "place": "",    "gender" : "f"},
    32 : {"name": "Emile Piponnier",             "birth": "31/01/1892",           "death": "21/05", "place": "",    "gender" : "m"},
    33 : {"name": "Josephine Piponnier",             "birth": "02/12/1894",           "death": "10/03/1988", "place": "Lyon, France",    "gender" : "f"},
    34 : {"name": "Josephine Martinez",             "birth": "",           "death": "", "place": "",    "gender"    : "f"},
    35 : {"name": "Armand Martinez",             "birth": "",           "death": "", "place": "",    "gender"    : "m"},
    36 : {"name": "Agnes Volle",             "birth": "",           "death": "", "place": "",    "gender"    : "f"},
    37 : {"name": "Marcel Volle",             "birth": "",           "death": "", "place": "",    "gender"    : "m"},
    38 : {"name": "Jean Volle",             "birth": "",           "death": "", "place": "",    "gender"    : "m"},
    39 : {"name": "Isabelle Volle",             "birth": "",           "death": "", "place": "",    "gender"    : "f"},
    40 : {"name": "Jean-Nöel Volle",             "birth": "",           "death": "", "place": "",    "gender"    : "m"},
    41 : {"name": "Marie Claudine Laurent",             "birth": "01/07/1869",           "death": "", "place": "",    "gender"    : "f"},
    42: {"name": "Claude-Marie Laurent",     "birth": "1852", "death": " après 1911", "place": "", "gender": "m"},
    43: {"name": "Pierre Laurent",           "birth": "1855", "death": "1877", "place": "", "gender": "m"},
    45: {"name": "Jean Laurent",             "birth": "1863", "death": "1863", "place": "", "gender": "m"},
    46: {"name": "Jean Marie Laurent",       "birth": "1864", "death": "1867", "place": "", "gender": "m"},
    47 : {"name": "Marie Louise Laurent",      "birth": "1866", "death": "1867", "place": "","gender": "f"},
    48 : {"name": "Philibert Antoine Frerot",      "birth": "", "death": "", "place": "", "gender": "m"},
    49 : {"name": "Jeanne Mathilde Frerot",       "birth": "Née en 1906", "death": "après 1926", "place": "", "gender": "f"},
    50 : {"name": "Henri Guerin",       "birth": "", "death": "", "place": "", "gender": "m"},
    51 : {"name": "Claude-Marie Boumont (ou Benoit)",       "birth": "", "death": "", "place": "", "gender": "m"},
}   

FILIATIONS = [
    (1,3),(2,3),
    (3,5),(4,5),(3,6),(4,6),(3,7),(4,7),(3,8),(4,8),(3,10),(4,10),(3,11),(4,11),(3,31),(4,31),(3,32),(4,32),(3,33),(4,33),
    (8,12),(9,12),
    (12,14),(13,14),(12,15),(13,15),
    (14,17),(16,17),(14,18),(16,18),(14,19),(16,19),
    (22,4), (23,4), (20,24), 
    (19,24), (20,25), (19,25), (20,26), (19,26), (18,27), (18, 28),
    (29,9), (30,9), (17,34), (17,35),
    (36,39), (37,39), (36,40), (37,40),(36,20), (37,20),
    (22,41), (23,41),(22,42), (23,42),(22,43), (23,43),(22,45), (23,45),(22,46), (23,46),(22,48), (23,48),
    (6,49), (48,49),
]

UNIONS = {
    "1-2":   {"a": 1,  "b": 2,  "date": ""},
    "3-4":   {"a": 3,  "b": 4,  "date": "mariage le 28/02/1878"},
    "8-9":   {"a": 8,  "b": 9,  "date": ""},
    "10-21": {"a": 10, "b": 21, "date": ""},
    "12-13": {"a": 12, "b": 13, "date": ""},
    "14-16": {"a": 14, "b": 16, "date": "ca. 1970"},
    "19-20": {"a": 19, "b": 20, "date": "ca. 2000"},
    "22-23": {"a": 22, "b": 23, "date": "19/01/1852", "place": "Simandre, Saône-et-Loire, France"},
    "36-37": {"a": 36, "b": 37, "date": ""},
    "6-48":   {"a": 6,  "b": 48, "date": "27 août 1904", "place": "Loisy, 71261, Saône-et-Loire, Bourgogne, France"},
    "49-50":   {"a": 49,  "b": 50, "date": "entre 1921 et 1926", "place": "Gigny-sur-Saône, 71219, Saône-et-Loire, Bourgogne, France "},
    "7-51":   {"a": 7,  "b": 51, "date": "01/02/1906", "place": "Loisy, 71261, Saône-et-Loire, Bourgogne, France "},
}

ROLE_STYLES = {
    "self":                 {"fill": "#FEF3C7", "stroke": "#D97706", "text": "#92400E"},
    "parent":               {"fill": "#DBEAFE", "stroke": "#3B82F6", "text": "#1E40AF"},
    "grand-parent":         {"fill": "#C7D7FD", "stroke": "#4F46E5", "text": "#312E81"},
    "arrière grand-parent": {"fill": "#B5C5FB", "stroke": "#3730A3", "text": "#1E1B4B"},
    "conjoint(e)":          {"fill": "#FCE7F3", "stroke": "#EC4899", "text": "#831843"},
    "enfant":               {"fill": "#D1FAE5", "stroke": "#10B981", "text": "#064E3B"},
    "petit-enfant":         {"fill": "#A7F3D0", "stroke": "#059669", "text": "#064E3B"},
    "frère/sœur":           {"fill": "#FFEDD5", "stroke": "#F97316", "text": "#7C2D12"},
    "gendre/bru":           {"fill": "#EDE9FE", "stroke": "#8B5CF6", "text": "#4C1D95"},
    "neveu/nièce":          {"fill": "#FEF3C7", "stroke": "#F59E0B", "text": "#78350F"},
    "neutre":               {"fill": "#F3F4F6", "stroke": "#9CA3AF", "text": "#374151"},
}

LEGEND_ORDER = [
    ("self",                 "Vous"),
    ("conjoint(e)",          "Conjoint(e)"),
    ("parent",               "Parent"),
    ("grand-parent",         "Grand-parent"),
    ("arrière grand-parent", "Arrière grand-parent"),
    ("frère/sœur",           "Frère / Sœur"),
    ("enfant",               "Enfant"),
    ("petit-enfant",         "Petit-enfant"),
    ("gendre/bru",           "Gendre / Bru"),
    ("neveu/nièce",          "Neveu / Nièce"),
]

# ─── LOGIQUE RELATIONS ────────────────────────────────────────────────────────
def get_relations(pid: int) -> dict:
    roles = {pid: "self"}
    parents = [p for p, c in FILIATIONS if c == pid]
    for p in parents:
        roles[p] = "parent"
        for gp, gc in FILIATIONS:
            if gc == p:
                roles[gp] = "grand-parent"
                for ggp, ggc in FILIATIONS:
                    if ggc == gp:
                        roles[ggp] = "arrière grand-parent"
    for u in UNIONS.values():
        if u["a"] == pid: roles.setdefault(u["b"], "conjoint(e)")
        if u["b"] == pid: roles.setdefault(u["a"], "conjoint(e)")
    children = [c for p, c in FILIATIONS if p == pid]
    for c in children:
        roles[c] = "enfant"
        for p2, c2 in FILIATIONS:
            if p2 == c: roles[c2] = "petit-enfant"
    siblings = {c2 for p in parents for p2, c2 in FILIATIONS if p2 == p and c2 != pid}
    for s in siblings:
        roles.setdefault(s, "frère/sœur")
    for c in children:
        for u in UNIONS.values():
            if u["a"] == c: roles.setdefault(u["b"], "gendre/bru")
            if u["b"] == c: roles.setdefault(u["a"], "gendre/bru")
    for p in parents:
        for u in UNIONS.values():
            if u["a"] == p: roles.setdefault(u["b"], "parent")
            if u["b"] == p: roles.setdefault(u["a"], "parent")
    for s in siblings:
        for p2, c2 in FILIATIONS:
            if p2 == s: roles.setdefault(c2, "neveu/nièce")
    return roles


def get_union_key(a: int, b: int):
    for k, u in UNIONS.items():
        if (u["a"] == a and u["b"] == b) or (u["a"] == b and u["b"] == a):
            return k
    return None


def build_context(pid: int) -> str:
    info = PERSONS[pid]
    parents  = [PERSONS[p]["name"] for p, c in FILIATIONS if c == pid]
    children = [PERSONS[c]["name"] for p, c in FILIATIONS if p == pid]
    spouses  = []
    for u in UNIONS.values():
        if u["a"] == pid:
            spouses.append({"name": PERSONS[u["b"]]["name"], "date": u["date"]})
        elif u["b"] == pid:
            spouses.append({"name": PERSONS[u["a"]]["name"], "date": u["date"]})
    parent_ids = [p for p, c in FILIATIONS if c == pid]
    siblings = [
        PERSONS[c]["name"]
        for par in parent_ids
        for p2, c in FILIATIONS
        if p2 == par and c != pid
    ]
    ctx = f"Nom : {info['name']}\nGenre : {'Homme' if info['gender']=='m' else 'Femme'}"
    if info["birth"]: ctx += f"\nNaissance : {info['birth']}"
    if info["death"]: ctx += f"\nDécès : {info['death']}"
    if info["place"]: ctx += f"\nLieu : {info['place']}"
    if parents:  ctx += f"\nParents : {' et '.join(parents)}"
    if spouses:
        sp_str = ", ".join(
            s["name"] + (f" (mariage {s['date']})" if s["date"] else "")
            for s in spouses
        )
        ctx += f"\nConjoint(e)(s) : {sp_str}"
    if siblings:  ctx += f"\nFrères/sœurs : {', '.join(siblings)}"
    if children:  ctx += f"\nEnfants : {', '.join(children)}"
    return ctx


def generate_story(pid: int) -> str:
    ctx = build_context(pid)
    prompt = (
        "Tu es un généalogiste conteur. À partir de ces informations sur un membre "
        "de la famille Piponnier, rédige un récit de vie court, chaleureux et plausible "
        "en français (3-4 paragraphes, 3e personne). Invente des détails vraisemblables "
        "selon l'époque et les liens familiaux. Ne mentionne pas que tu inventes.\n\n"
        f"{ctx}\n\nRécit de vie :"
    )
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "chosen_id" not in st.session_state:
    st.session_state.chosen_id = 18
if "view_all" not in st.session_state:
    st.session_state.view_all = False
if "story" not in st.session_state:
    st.session_state.story = {}

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Arbre Généalogique")
    st.markdown(
        "<p style='font-size:12px;color:#AAA;margin-top:-10px;'>6 générations · 21 membres</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if st.button(
        "🌐 Voir tout l'arbre" if not st.session_state.view_all else "Vue individuelle",
        use_container_width=True,
    ):
        st.session_state.view_all = not st.session_state.view_all
        st.rerun()

    st.markdown(
        "<p style='font-size:11px;letter-spacing:1.5px;color:#888;text-transform:uppercase;'>Je suis…</p>",
        unsafe_allow_html=True,
    )

    sorted_names = sorted(PERSONS.items(), key=lambda x: x[1]["name"])
    options = {v["name"]: k for k, v in sorted_names}
    chosen_name = st.selectbox(
        "",
        list(options.keys()),
        index=list(options.keys()).index(PERSONS[st.session_state.chosen_id]["name"]),
        label_visibility="collapsed",
    )
    new_id = options[chosen_name]
    if new_id != st.session_state.chosen_id:
        st.session_state.chosen_id = new_id
        st.session_state.view_all = False
        st.rerun()

    chosen_id = st.session_state.chosen_id
    st.markdown("---")

    roles = get_relations(chosen_id) if not st.session_state.view_all else {k: "neutre" for k in PERSONS}
    if not st.session_state.view_all:
        roles[chosen_id] = "self"

    if st.session_state.view_all:
        st.markdown(
            "<div class='relation-box'>Tous les membres de la famille sont affichés.</div>",
            unsafe_allow_html=True,
        )
    else:
        first = PERSONS[chosen_id]["name"].split()[0]
        counts = {}
        for r in roles.values():
            if r != "self":
                counts[r] = counts.get(r, 0) + 1
        lines = [f"<b>Vue de {first}</b><br>"]
        for role, label in LEGEND_ORDER:
            if role in counts:
                n = counts[role]
                lines.append(f"· {n} {label}")
        st.markdown(
            f"<div class='relation-box'>{'<br>'.join(lines)}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:11px;letter-spacing:1.5px;color:#888;text-transform:uppercase;'>Légende</p>",
        unsafe_allow_html=True,
    )
    for role, label in LEGEND_ORDER:
        st2 = ROLE_STYLES[role]
        st.markdown(
            f"<span class='legend-dot' style='background:{st2['fill']};border:2px solid {st2['stroke']};'></span>"
            f"<span style='font-size:12px;color:#444;'>{label}</span>",
            unsafe_allow_html=True,
        )

# ─── PRÉPARER LES JSON POUR LE JS (évite les conflits d'accolades dans les f-strings) ───
persons_json    = json.dumps(PERSONS)
filiations_list = [[p, c] for p, c in FILIATIONS]
filiations_json = json.dumps(filiations_list)
unions_clean    = {k: {"a": v["a"], "b": v["b"], "date": v["date"]} for k, v in UNIONS.items()}
unions_json     = json.dumps(unions_clean)
styles_json     = json.dumps(ROLE_STYLES)
view_all_js     = "true" if st.session_state.view_all else "false"

# ─── ARBRE HTML+JS ────────────────────────────────────────────────────────────
tree_html = """
<style>
*{box-sizing:border-box;margin:0;padding:0;}
#wrap{width:100%;height:680px;background:#FAF8F5;border-radius:10px;border:1px solid #E8E5E0;overflow:hidden;position:relative;}
#tree-svg{width:100%;height:100%;cursor:grab;display:block;}
#tree-svg:active{cursor:grabbing;}
.ng{cursor:pointer;}
.ng:hover .nr{opacity:.82;}
#tt{position:absolute;background:#fff;border:1px solid #DDD;border-radius:8px;padding:8px 10px;font-size:12px;font-family:Inter,sans-serif;pointer-events:none;opacity:0;transition:opacity .15s;max-width:210px;z-index:5;}
#tt.show{opacity:1;}
#tt strong{font-weight:600;display:block;margin-bottom:3px;color:#222;}
#tt span{color:#666;font-size:11px;display:block;line-height:1.6;}
</style>
<div id="wrap">
  <svg id="tree-svg" viewBox="0 0 1300 680" preserveAspectRatio="xMidYMid meet">
    <g id="LL"></g>
    <g id="NL"></g>
  </svg>
  <div id="tt"></div>
</div>
<script>
""" + f"""
const P = {persons_json};
const FILIATIONS = {filiations_json};
const UNIONS = {unions_json};
const ROLE_STYLES = {styles_json};
const SEL_ID = {chosen_id};
const VIEW_ALL = {view_all_js};
""" + """
const CW=7.5, PAD=18, HGAP=50, ROW_H=52, ROW_GAP=80;

const ROWS=[
  {y:40+(ROW_H+ROW_GAP)*1, ids:[23,22,2,1]}, 
  {y:40+(ROW_H+ROW_GAP)*2, ids:[42,43,45,46,48,41, 4,3,  29,30]},
  {y:40+(ROW_H+ROW_GAP)*3, ids:[5,6,48,7,31,32,33,10,21,11,8,9]},
  {y:40+(ROW_H+ROW_GAP)*4, ids:[50,49,13,12]},
  {y:40+(ROW_H+ROW_GAP)*5, ids:[16,14,15, 36, 37]},
  {y:40+(ROW_H+ROW_GAP)*6, ids:[17,18,19,20,39,40]},
  {y:40+(ROW_H+ROW_GAP)*7, ids:[34,35,27,28,24,25,26]},
];

function measure(name){
  const words=name.split(' ');
  if(words.length<=2) return {lines:[name], w:Math.max(name.length*CW+PAD*2,72), h:34};
  const h=Math.ceil(words.length/2);
  const l1=words.slice(0,h).join(' '), l2=words.slice(h).join(' ');
  return {lines:[l1,l2], w:Math.max(Math.max(l1.length,l2.length)*CW+PAD*2,72), h:46};
}

function layoutRow(ids){
  const ms=ids.map(id=>measure(P[id].name));
  const total=ms.reduce((s,m)=>s+m.w,0)+(ids.length-1)*HGAP;
  let cx=(1300-total)/2;
  const pos={};
  ids.forEach((id,i)=>{pos[id]={x:cx+ms[i].w/2, m:ms[i]}; cx+=ms[i].w+HGAP;});
  return pos;
}

const COORDS={};
ROWS.forEach(row=>{
  const pos=layoutRow(row.ids);
  row.ids.forEach(id=>{COORDS[id]={x:pos[id].x, y:row.y+pos[id].m.h/2, m:pos[id].m};});
});

function getRels(pid){
  const roles={[pid]:"self"};
  const parents=FILIATIONS.filter(([p,c])=>c===pid).map(([p])=>p);
  parents.forEach(p=>{
    roles[p]="parent";
    FILIATIONS.filter(([gp,gc])=>gc===p).forEach(([gp])=>{
      roles[gp]="grand-parent";
      FILIATIONS.filter(([ggp,ggc])=>ggc===gp).forEach(([ggp])=>{roles[ggp]="arrière grand-parent";});
    });
  });
  Object.values(UNIONS).forEach(u=>{
    if(u.a===pid) roles[u.b]=roles[u.b]||"conjoint(e)";
    if(u.b===pid) roles[u.a]=roles[u.a]||"conjoint(e)";
  });
  const children=FILIATIONS.filter(([p])=>p===pid).map(([,c])=>c);
  children.forEach(c=>{
    roles[c]="enfant";
    FILIATIONS.filter(([p2])=>p2===c).forEach(([,c2])=>{roles[c2]="petit-enfant";});
  });
  const siblings=new Set(parents.flatMap(par=>FILIATIONS.filter(([p])=>p===par).map(([,c])=>c).filter(c=>c!==pid)));
  siblings.forEach(s=>{roles[s]=roles[s]||"frère/sœur";});
  children.forEach(c=>{Object.values(UNIONS).forEach(u=>{
    if(u.a===c) roles[u.b]=roles[u.b]||"gendre/bru";
    if(u.b===c) roles[u.a]=roles[u.a]||"gendre/bru";
  });});
  parents.forEach(p=>{Object.values(UNIONS).forEach(u=>{
    if(u.a===p) roles[u.b]=roles[u.b]||"parent";
    if(u.b===p) roles[u.a]=roles[u.a]||"parent";
  });});
  siblings.forEach(s=>{FILIATIONS.filter(([p2])=>p2===s).forEach(([,c2])=>{roles[c2]=roles[c2]||"neveu/nièce";});});
  return roles;
}

const curRoles=VIEW_ALL
  ? Object.fromEntries(Object.keys(P).map(k=>[k,"neutre"]))
  : getRels(SEL_ID);
if(!VIEW_ALL) curRoles[SEL_ID]="self";

function mkEl(tag){return document.createElementNS('http://www.w3.org/2000/svg',tag);}

const LL=document.getElementById('LL'), NL=document.getElementById('NL');
const vis=new Set(Object.keys(curRoles).map(Number));

Object.values(UNIONS).forEach(u=>{
  if(!vis.has(u.a)||!vis.has(u.b)) return;
  const A=COORDS[u.a], B=COORDS[u.b];
  const line=mkEl('line');
  line.setAttribute('x1',A.x); line.setAttribute('y1',A.y);
  line.setAttribute('x2',B.x); line.setAttribute('y2',B.y);
  line.setAttribute('stroke','#CCCCCC'); line.setAttribute('stroke-width','1.5');
  line.setAttribute('stroke-dasharray','4 3');
  LL.appendChild(line);
  if(u.date){
    const tx=(A.x+B.x)/2, ty=(A.y+B.y)/2;
    const bg=mkEl('rect');
    bg.setAttribute('x',tx-26); bg.setAttribute('y',ty-9);
    bg.setAttribute('width',52); bg.setAttribute('height',14);
    bg.setAttribute('rx',3); bg.setAttribute('fill','#FAF8F5');
    LL.appendChild(bg);
    const dt=mkEl('text');
    dt.setAttribute('x',tx); dt.setAttribute('y',ty+1);
    dt.setAttribute('text-anchor','middle'); dt.setAttribute('font-size','9');
    dt.setAttribute('fill','#AAA'); dt.setAttribute('font-family','Inter,sans-serif');
    dt.textContent=u.date;
    LL.appendChild(dt);
  }
});

FILIATIONS.forEach(([pp,c])=>{
  if(!vis.has(pp)||!vis.has(c)) return;
  const A=COORDS[pp], B=COORDS[c];
  const my=(A.y+B.y)/2;
  const path=mkEl('path');
  path.setAttribute('d',`M${A.x},${A.y} L${A.x},${my} L${B.x},${my} L${B.x},${B.y}`);
  path.setAttribute('fill','none'); path.setAttribute('stroke','#DDD'); path.setAttribute('stroke-width','1');
  LL.appendChild(path);
});

vis.forEach(pid=>{
  const info=P[pid], role=curRoles[pid]||"neutre", st=ROLE_STYLES[role]||ROLE_STYLES["neutre"];
  const C=COORDS[pid]; if(!C) return;
  const m=C.m, nw=m.w, nh=m.h, nx=C.x-nw/2, ny=C.y-nh/2;
  const g=mkEl('g'); g.setAttribute('class','ng');
  const rect=mkEl('rect'); rect.setAttribute('class','nr');
  rect.setAttribute('x',nx); rect.setAttribute('y',ny);
  rect.setAttribute('width',nw); rect.setAttribute('height',nh);
  rect.setAttribute('rx',7); rect.setAttribute('fill',st.fill);
  rect.setAttribute('stroke',st.stroke); rect.setAttribute('stroke-width','1.5');
  g.appendChild(rect);
  if(m.lines.length===1){
    const t=mkEl('text');
    t.setAttribute('x',C.x); t.setAttribute('y',C.y);
    t.setAttribute('text-anchor','middle'); t.setAttribute('dominant-baseline','central');
    t.setAttribute('font-size','11'); t.setAttribute('fill',st.text);
    t.setAttribute('font-family','Inter,sans-serif'); t.setAttribute('font-weight','500');
    t.textContent=m.lines[0]; g.appendChild(t);
  } else {
    m.lines.forEach((ln,i)=>{
      const t=mkEl('text');
      t.setAttribute('x',C.x); t.setAttribute('y',ny+(i===0?13:29));
      t.setAttribute('text-anchor','middle'); t.setAttribute('dominant-baseline','central');
      t.setAttribute('font-size','11'); t.setAttribute('fill',st.text);
      t.setAttribute('font-family','Inter,sans-serif'); t.setAttribute('font-weight','500');
      t.textContent=ln; g.appendChild(t);
    });
  }
  const icon=mkEl('text');
  icon.setAttribute('x',nx+nw-4); icon.setAttribute('y',ny+4);
  icon.setAttribute('text-anchor','end'); icon.setAttribute('dominant-baseline','hanging');
  icon.setAttribute('font-size','10'); icon.setAttribute('fill',st.stroke);
  icon.setAttribute('font-family','Inter,sans-serif');
  icon.textContent=info.gender==='m'?'♂':'♀';
  g.appendChild(icon);
  if(role==='self'){
    const star=mkEl('text');
    star.setAttribute('x',nx+4); star.setAttribute('y',ny+3);
    star.setAttribute('dominant-baseline','hanging'); star.setAttribute('font-size','10');
    star.setAttribute('fill',st.stroke); star.textContent='★';
    g.appendChild(star);
  }
  g.addEventListener('mouseenter',e=>showTT(e,pid));
  g.addEventListener('mousemove',e=>moveTT(e));
  g.addEventListener('mouseleave',hideTT);
  NL.appendChild(g);
});

function showTT(e,pid){
  const info=P[pid], role=curRoles[pid]||"", tip=document.getElementById('tt');
  let html=`<strong>${info.name}</strong>`;
  if(role&&role!=='neutre') html+=`<span>${role.charAt(0).toUpperCase()+role.slice(1)}</span>`;
  html+=`<span>${info.gender==='m'?'Homme':'Femme'}</span>`;
  if(info.birth) html+=`<span>Né(e) : ${info.birth}</span>`;
  if(info.death) html+=`<span>Décédé(e) : ${info.death}</span>`;
  if(info.place) html+=`<span>Lieu : ${info.place}</span>`;
  tip.innerHTML=html; tip.classList.add('show'); moveTT(e);
}
function moveTT(e){
  const r=document.getElementById('wrap').getBoundingClientRect(), tip=document.getElementById('tt');
  let x=e.clientX-r.left+12, y=e.clientY-r.top-10;
  if(x+215>r.width) x=e.clientX-r.left-215;
  tip.style.left=x+'px'; tip.style.top=y+'px';
}
function hideTT(){document.getElementById('tt').classList.remove('show');}

let isDrag=false, ds={x:0,y:0}, vo={x:0,y:0}, dOrig={x:0,y:0};
const svg=document.getElementById('tree-svg');
svg.addEventListener('mousedown',e=>{
  if(e.target.closest('.ng')) return;
  isDrag=true; ds={x:e.clientX,y:e.clientY}; dOrig={...vo};
});
window.addEventListener('mousemove',e=>{
  if(!isDrag) return;
  vo.x=dOrig.x+(e.clientX-ds.x); vo.y=dOrig.y+(e.clientY-ds.y);
  NL.setAttribute('transform',`translate(${vo.x},${vo.y})`);
  LL.setAttribute('transform',`translate(${vo.x},${vo.y})`);
});
window.addEventListener('mouseup',()=>isDrag=false);
</script>
"""

st.markdown("# Arbre Généalogique")
st.components.v1.html(tree_html, height=700, scrolling=False)

# ─── PANNEAU DE DÉTAIL ────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Renseignement de la Personne")
    sorted_names_detail = sorted(PERSONS.items(), key=lambda x: x[1]["name"])
    options_detail = {v["name"]: k for k, v in sorted_names_detail}
    detail_name = st.selectbox(
        "Sélectionner une personne",
        list(options_detail.keys()),
        index=list(options_detail.keys()).index(PERSONS[chosen_id]["name"]),
        key="detail_select",
    )
    detail_id = options_detail[detail_name]
    info = PERSONS[detail_id]
    role = get_relations(chosen_id).get(detail_id, "neutre") if not st.session_state.view_all else "neutre"
    st2 = ROLE_STYLES.get(role, ROLE_STYLES["neutre"])
    initials = "".join(n[0] for n in info["name"].split()[:2])

    st.markdown(
        f"""<div class='detail-card'>
        <div class='detail-avatar' style='background:{st2["fill"]};border:2px solid {st2["stroke"]};color:{st2["stroke"]}'>{initials}</div>
        <div class='detail-name'>{info["name"]}</div>
        <div class='detail-role'>{role.capitalize() if role != 'neutre' else ''} · {'Homme' if info['gender']=='m' else 'Femme'}</div>
        {"<div class='detail-row'><span class='detail-label'>Naissance</span><span>"+info['birth']+"</span></div>" if info['birth'] else ''}
        {"<div class='detail-row'><span class='detail-label'>Décès</span><span>"+info['death']+"</span></div>" if info['death'] else ''}
        {"<div class='detail-row'><span class='detail-label'>Lieu</span><span>"+info['place']+"</span></div>" if info['place'] else ''}
        </div>""",
        unsafe_allow_html=True,
    )

    parents_ids  = [p for p, c in FILIATIONS if c == detail_id]
    children_ids = [c for p, c in FILIATIONS if p == detail_id]
    spouses_ids  = [u["b"] if u["a"]==detail_id else u["a"] for u in UNIONS.values() if u["a"]==detail_id or u["b"]==detail_id]
    sibling_ids  = {c for par in parents_ids for p2, c in FILIATIONS if p2 == par and c != detail_id}

    def rel_section(title, ids, tag):
        if not ids: return ""
        lines = f"<div class='detail-sect'>{title}</div>"
        for sid in ids:
            lines += f"<div><span class='rel-tag'>{tag}</span> <span style='font-size:12px;color:#3B82F6'>{PERSONS[sid]['name']}</span></div>"
        return lines

    marriage_html = ""
    for sp in spouses_ids:
        uk = get_union_key(detail_id, sp)
        if uk and UNIONS[uk]["date"]:
            marriage_html += f"<div class='detail-row'><span class='detail-label'>Mariage</span><span>{UNIONS[uk]['date']}</span></div>"

    rel_html = marriage_html
    rel_html += rel_section("Conjoint(e)", spouses_ids, "conjoint")
    rel_html += rel_section("Parents", parents_ids, "parent")
    rel_html += rel_section("Frères & sœurs", list(sibling_ids), "fratrie")
    rel_html += rel_section("Enfants", children_ids, "enfant")

    if rel_html:
        st.markdown(f"<div class='detail-card'>{rel_html}</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("✍️ Générer le récit de vie", use_container_width=True, key="story_btn"):
        with st.spinner("Génération du récit en cours…"):
            story_text = generate_story(detail_id)
            st.session_state.story[detail_id] = story_text

with col2:
    st.markdown("### 📖 Récit de vie")
    if detail_id in st.session_state.story:
        paragraphs = st.session_state.story[detail_id].strip().split("\n")
        story_html = "".join(
            f"<p style='margin-bottom:10px'>{p}</p>" for p in paragraphs if p.strip()
        )
        st.markdown(f"<div class='story-area'>{story_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='story-area' style='color:#AAA;font-style:italic'>"
            "Cliquez sur « Générer le récit de vie » pour créer l'histoire de cette personne."
            "</div>",
            unsafe_allow_html=True,
        )