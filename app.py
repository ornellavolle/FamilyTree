import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Arbre Généalogique · Famille Piponnier",
    page_icon="🌳",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500&family=Inter:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #FAF8F5; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E8E5E0; }
section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
h1 { font-family: 'Playfair Display', serif !important; font-weight: 400 !important; color: #2A2A2A !important; }
.relation-box { background: #FAF8F5; border: 1px solid #E8E5E0; border-radius: 8px; padding: 12px 14px; font-size: 13px; color: #555; line-height: 1.9; }
.legend-dot { display: inline-block; width: 12px; height: 12px; border-radius: 2px; margin-right: 6px; vertical-align: middle; }
hr { border: none; border-top: 1px solid #EEE; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ── DONNÉES ───────────────────────────────────────────────────────────────────
PERSONS = {
    1:  {"name": "François Piponnier",       "birth": "",           "death": "28/01/1870", "place": "Simandre", "gender": "m"},
    2:  {"name": "Claudine Viennois",          "birth": "",           "death": "",           "place": "",         "gender": "f"},
    3:  {"name": "Jean Claude Piponnier",     "birth": "02/08/1847", "death": "",           "place": "Simandre", "gender": "m"},
    4:  {"name": "Marie Catherine Laurent",   "birth": "05/03/1839", "death": "",           "place": "",         "gender": "f"},
    5:  {"name": "Jean Claude Piponnier",     "birth": "09/07/1876", "death": "",           "place": "",         "gender": "m"},
    6:  {"name": "Louise Piponnier",          "birth": "10/04/1884", "death": "",           "place": "",         "gender": "f"},
    7:  {"name": "Marie Piponnier",           "birth": "10/10/1885", "death": "",           "place": "",         "gender": "f"},
    8:  {"name": "Jean Marie Piponnier",      "birth": "30/10/1887", "death": "25/03/1977", "place": "",         "gender": "m"},
    9:  {"name": "Henriette Morin",           "birth": "",           "death": "",           "place": "",         "gender": "f"},
    10: {"name": "Francis Piponnier",         "birth": "30/08/1890", "death": "",           "place": "",         "gender": "m"},
    11: {"name": "Marguerite Piponnier",      "birth": "18/09/1895", "death": "",           "place": "",         "gender": "f"},
    12: {"name": "Hortense Piponnier",        "birth": "",           "death": "",           "place": "",         "gender": "f"},
    13: {"name": "Francis Pourprix",          "birth": "",           "death": "",           "place": "",         "gender": "m"},
    14: {"name": "Nicole Pourprix",           "birth": "22/08/1943", "death": "",           "place": "",         "gender": "f"},
    15: {"name": "Marie-France Pourprix",     "birth": "",           "death": "",           "place": "",         "gender": "f"},
    16: {"name": "Mohamed El raiani",        "birth": "",           "death": "",           "place": "",         "gender": "m"},
    17: {"name": "Florence El raiani",       "birth": "",           "death": "",           "place": "",         "gender": "f"},
    18: {"name": "Natalie El raiani",        "birth": "",           "death": "",           "place": "",         "gender": "f"},
    19: {"name": "Sandrine El raiani",       "birth": "02/08/1973", "death": "",           "place": "",         "gender": "f"},
    20: {"name": "Régis Volle",               "birth": "23/03/1977", "death": "",           "place": "",         "gender": "m"},
    21: {"name": "Jeanne Marie DuBuisson",    "birth": "",           "death": "",           "place": "",         "gender": "f"},
    22 : {"name": "Anne Viennois",               "birth": "",           "death": "",           "place": "", "gender": "f"},
}

FILIATIONS = [
    (1,3),(2,3),
    (3,5),(4,5),(3,6),(4,6),(3,7),(4,7),(3,8),(4,8),(3,10),(4,10),(3,11),(4,11),
    (8,12),(9,12),
    (12,14),(13,14),(12,15),(13,15),
    (14,17),(16,17),(14,18),(16,18),(14,19),(16,19),
]

UNIONS = [(1,2),(3,4),(8,9),(10,21),(12,13),(14,16),(19,20)]

POSITIONS = {
    1:(0.52,0.04), 2:(0.38,0.04),
    3:(0.55,0.18), 4:(0.41,0.18),
    5:(0.04,0.34), 6:(0.16,0.34), 7:(0.28,0.34),
    8:(0.44,0.34), 9:(0.58,0.34),
    10:(0.72,0.34), 11:(0.86,0.34), 21:(0.93,0.34),
    12:(0.44,0.52), 13:(0.30,0.52),
    14:(0.30,0.68), 15:(0.52,0.68), 16:(0.14,0.68),
    17:(0.04,0.84), 18:(0.18,0.84), 19:(0.34,0.84), 20:(0.48,0.84),
}

ROLE_STYLES = {
    "self":                 {"fill":"#FFF3CD","stroke":"#C8960C","text":"#7A5A00"},
    "parent":               {"fill":"#DCEEF9","stroke":"#3B7EC8","text":"#0C447C"},
    "grand-parent":         {"fill":"#C8DFF7","stroke":"#185FA5","text":"#042C53"},
    "arrière grand-parent": {"fill":"#B5D4F4","stroke":"#0C447C","text":"#042C53"},
    "conjoint(e)":          {"fill":"#FCE8F3","stroke":"#C83B6E","text":"#72243E"},
    "enfant":               {"fill":"#E1F5EE","stroke":"#1D9E75","text":"#04342C"},
    "petit-enfant":         {"fill":"#C5EDDF","stroke":"#0F6E56","text":"#04342C"},
    "frère/sœur":           {"fill":"#FDE8D8","stroke":"#D85A30","text":"#4A1B0C"},
    "gendre/bru":           {"fill":"#F3E8FD","stroke":"#7F77DD","text":"#26215C"},
    "neveu/nièce":          {"fill":"#FEF0E0","stroke":"#BA7517","text":"#412402"},
}

LEGEND_ORDER = [
    ("self","Vous"),
    ("conjoint(e)","Conjoint(e)"),
    ("parent","Parent"),
    ("grand-parent","Grand-parent"),
    ("arrière grand-parent","Arrière grand-parent"),
    ("frère/sœur","Frère / Sœur"),
    ("enfant","Enfant"),
    ("petit-enfant","Petit-enfant"),
    ("gendre/bru","Gendre / Bru"),
    ("neveu/nièce","Neveu / Nièce"),
]

def get_relations(pid):
    roles = {pid: "self"}
    parents = {p for p,c in FILIATIONS if c == pid}
    for p in parents:
        roles[p] = "parent"
        for gp,gc in FILIATIONS:
            if gc == p:
                roles[gp] = "grand-parent"
                for ggp,ggc in FILIATIONS:
                    if ggc == gp:
                        roles[ggp] = "arrière grand-parent"
    for a,b in UNIONS:
        if a == pid: roles.setdefault(b,"conjoint(e)")
        if b == pid: roles.setdefault(a,"conjoint(e)")
    children = {c for p,c in FILIATIONS if p == pid}
    for c in children:
        roles[c] = "enfant"
        for p2,c2 in FILIATIONS:
            if p2 == c: roles[c2] = "petit-enfant"
    siblings = {c2 for p in parents for p2,c2 in FILIATIONS if p2==p and c2!=pid}
    for s in siblings:
        roles[s] = "frère/sœur"
    for a,b in UNIONS:
        if a in children: roles.setdefault(b,"gendre/bru")
        if b in children: roles.setdefault(a,"gendre/bru")
    for p in parents:
        for a,b in UNIONS:
            if a==p: roles.setdefault(b,"parent")
            if b==p: roles.setdefault(a,"parent")
    for s in siblings:
        for p2,c2 in FILIATIONS:
            if p2==s: roles.setdefault(c2,"neveu/nièce")
    return roles

def build_figure(pid):
    roles = get_relations(pid)
    visible = set(roles.keys())
    fig = go.Figure()

    # Lignes d'union (tirets)
    for a,b in UNIONS:
        if a not in visible or b not in visible: continue
        ax,ay = POSITIONS.get(a,(0.5,0.5))
        bx,by = POSITIONS.get(b,(0.5,0.5))
        fig.add_shape(type="line",x0=ax,y0=ay,x1=bx,y1=by,
                      line=dict(color="#BBBBBB",width=1.5,dash="dot"),
                      xref="paper",yref="paper")

    # Lignes de filiation (L)
    for p,c in FILIATIONS:
        if p not in visible or c not in visible: continue
        px_,py_ = POSITIONS.get(p,(0.5,0.5))
        cx_,cy_ = POSITIONS.get(c,(0.5,0.5))
        my = (py_+cy_)/2
        for x0,y0,x1,y1 in [(px_,py_,px_,my),(px_,my,cx_,my),(cx_,my,cx_,cy_)]:
            fig.add_shape(type="line",x0=x0,y0=y0,x1=x1,y1=y1,
                          line=dict(color="#AAAAAA",width=1),xref="paper",yref="paper")

    # Noeuds
    xs,ys,texts,hovers,fills,strokes = [],[],[],[],[],[]
    for p2 in visible:
        info = PERSONS[p2]
        role = roles[p2]
        st2 = ROLE_STYLES.get(role, ROLE_STYLES["self"])
        x,y = POSITIONS.get(p2,(0.5,0.5))
        name = info["name"]
        parts = name.split()
        label = (" ".join(parts[:len(parts)//2])+"<br>"+" ".join(parts[len(parts)//2:])) if len(parts)>3 else name
        tip = [f"<b>{name}</b>",f"<i>{role.capitalize()}</i>"]
        if info["birth"]: tip.append(f"Né(e) le {info['birth']}")
        if info["death"]: tip.append(f"Décédé(e) le {info['death']}")
        if info["place"]: tip.append(f"Lieu : {info['place']}")
        xs.append(x); ys.append(y); texts.append(label)
        hovers.append("<br>".join(tip))
        fills.append(st2["fill"]); strokes.append(st2["stroke"])

    fig.add_trace(go.Scatter(
        x=xs,y=ys,mode="markers+text",text=texts,
        textposition="middle center",
        textfont=dict(size=10,color="#222",family="Georgia, serif"),
        hovertext=hovers,hoverinfo="text",
        marker=dict(symbol="square",size=54,color=fills,
                    line=dict(color=strokes,width=2)),
        hoverlabel=dict(bgcolor="white",bordercolor="#DDD",
                        font=dict(size=13,family="Georgia, serif")),
    ))
    fig.update_layout(
        paper_bgcolor="#FAF8F5",plot_bgcolor="#FAF8F5",
        margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(visible=False,range=[-0.04,1.04]),
        yaxis=dict(visible=False,range=[-0.04,1.0]),
        showlegend=False,height=700,dragmode="pan",
        font=dict(family="Georgia, serif"),
    )
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌳 Famille Piponnier")
    st.markdown("<p style='font-size:12px;color:#AAA;margin-top:-10px;'>6 générations · 21 membres</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<p style='font-size:11px;letter-spacing:1.5px;color:#888;text-transform:uppercase;font-family:sans-serif;'>Je suis…</p>", unsafe_allow_html=True)

    sorted_names = sorted(PERSONS.items(), key=lambda x: x[1]["name"])
    options = {v["name"]: k for k,v in sorted_names}
    chosen_name = st.selectbox("", list(options.keys()), index=list(options.keys()).index("Natalie El ralenti"), label_visibility="collapsed")
    chosen_id = options[chosen_name]

    st.markdown("---")

    # Résumé des relations
    roles = get_relations(chosen_id)
    first = PERSONS[chosen_id]["name"].split()[0]
    counts = {}
    for r in roles.values():
        if r != "self": counts[r] = counts.get(r,0)+1

    summary_lines = [f"<b>Vue de {first}</b><br>"]
    for role,label in LEGEND_ORDER:
        if role in counts:
            n = counts[role]
            summary_lines.append(f"· {n} {label}{'s' if n>1 and not label.endswith(')') else ''}")
    st.markdown(f"<div class='relation-box'>{'<br>'.join(summary_lines)}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Légende
    st.markdown("<p style='font-size:11px;letter-spacing:1.5px;color:#888;text-transform:uppercase;font-family:sans-serif;'>Légende</p>", unsafe_allow_html=True)
    for role,label in LEGEND_ORDER:
        st2 = ROLE_STYLES[role]
        st.markdown(
            f"<span class='legend-dot' style='background:{st2['fill']};border:2px solid {st2['stroke']};'></span>"
            f"<span style='font-size:12px;color:#444;'>{label}</span>",
            unsafe_allow_html=True
        )

# ── ARBRE ─────────────────────────────────────────────────────────────────────
fig = build_figure(chosen_id)
st.plotly_chart(fig, use_container_width=True, config={
    "scrollZoom": True,
    "displayModeBar": True,
    "modeBarButtonsToRemove": ["select2d","lasso2d","autoScale2d"],
    "displaylogo": False,
})
