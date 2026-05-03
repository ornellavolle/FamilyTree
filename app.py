import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Arbre Généalogique · Famille Piponnier",
    page_icon="🌳",
    layout="wide",
)

# ── STYLE UI ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main {
    background: linear-gradient(180deg, #FAF8F5 0%, #F3F0EA 100%);
}
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #EEE;
}
.relation-box {
    background: white;
    border-radius: 12px;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    font-size: 13px;
}
.legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 4px;
    margin-right: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;'>🌳 Arbre généalogique</h1>
<p style='text-align:center;color:#777;'>Famille Piponnier</p>
""", unsafe_allow_html=True)

# ── DONNÉES ────────────────────────────────────────────────────────────────
PERSONS = {
    1: {"name":"François Piponnier","birth":"","death":"29/01/1870","place":"Simandre"},
    2: {"name":"Claudine Viennois","birth":"","death":"","place":""},
    3: {"name":"Jean Claude Piponnier","birth":"02/08/1847","death":"","place":"Simandre"},
    4: {"name":"Marie Catherine Laurent","birth":"05/03/1839","death":"","place":""},
    5: {"name":"Jean Claude Piponnier","birth":"09/07/1876","death":"","place":""},
    6: {"name":"Louise Piponnier","birth":"10/04/1884","death":"","place":""},
    7: {"name":"Marie Piponnier","birth":"10/10/1885","death":"","place":""},
    8: {"name":"Jean Marie Piponnier","birth":"30/10/1887","death":"25/03/1977","place":""},
    9: {"name":"Henriette Morin","birth":"","death":"","place":""},
    10: {"name":"Francis Piponnier","birth":"30/08/1890","death":"","place":""},
    11: {"name":"Marguerite Piponnier","birth":"18/09/1895","death":"","place":""},
    12: {"name":"Hortense Piponnier","birth":"","death":"","place":""},
    13: {"name":"Francis Pourprix","birth":"","death":"","place":""},
    14: {"name":"Nicole Pourprix","birth":"22/08/1943","death":"","place":""},
    15: {"name":"Marie-France Pourprix","birth":"","death":"","place":""},
    16: {"name":"Mohamed El raiani","birth":"","death":"","place":""},
    17: {"name":"Florence El raiani","birth":"","death":"","place":""},
    18: {"name":"Natalie El raiani","birth":"","death":"","place":""},
    19: {"name":"Sandrine El raiani","birth":"02/08/1973","death":"","place":""},
    20: {"name":"Régis Volle","birth":"23/03/1977","death":"","place":""},
    21: {"name":"Jeanne Marie DuBuisson","birth":"","death":"","place":""},
}

FILIATIONS = [
    (1,3),(2,3),(3,5),(4,5),(3,6),(4,6),(3,7),(4,7),
    (3,8),(4,8),(3,10),(4,10),(3,11),(4,11),
    (8,12),(9,12),(12,14),(13,14),(12,15),(13,15),
    (14,17),(16,17),(14,18),(16,18),(14,19),(16,19),
]

UNIONS = [
    {"a":1,"b":2,"marriage":"1850"},
    {"a":3,"b":4,"marriage":"1875"},
    {"a":8,"b":9,"marriage":""},
    {"a":10,"b":21,"marriage":""},
    {"a":12,"b":13,"marriage":""},
    {"a":14,"b":16,"marriage":""},
    {"a":19,"b":20,"marriage":"2000"},
]

POSITIONS = {
    1:(0.52,0.04),2:(0.38,0.04),
    3:(0.55,0.18),4:(0.41,0.18),
    5:(0.04,0.34),6:(0.16,0.34),7:(0.28,0.34),
    8:(0.44,0.34),9:(0.58,0.34),
    10:(0.72,0.34),11:(0.86,0.34),21:(0.93,0.34),
    12:(0.44,0.52),13:(0.30,0.52),
    14:(0.30,0.68),15:(0.52,0.68),16:(0.14,0.68),
    17:(0.04,0.84),18:(0.18,0.84),19:(0.34,0.84),20:(0.48,0.84),
}

ROLE_PRIORITY = {
    "self":100,"conjoint(e)":90,"frère/sœur":85,
    "parent":80,"enfant":80,"gendre/bru":75,
    "grand-parent":70,"petit-enfant":70,"neveu/nièce":65,
    "arrière grand-parent":60,
}

def set_role(roles, pid, role):
    if pid not in roles or ROLE_PRIORITY[role] > ROLE_PRIORITY[roles[pid]]:
        roles[pid] = role

def get_relations(pid):
    roles = {pid:"self"}

    parents = {p for p,c in FILIATIONS if c==pid}
    for p in parents:
        set_role(roles,p,"parent")

    children = {c for p,c in FILIATIONS if p==pid}
    for c in children:
        set_role(roles,c,"enfant")

    for a,b in UNIONS:
        if a==pid: set_role(roles,b,"conjoint(e)")
        if b==pid: set_role(roles,a,"conjoint(e)")

    siblings = {c2 for p in parents for p2,c2 in FILIATIONS if p2==p and c2!=pid}
    for s in siblings:
        set_role(roles,s,"frère/sœur")

    return roles

def build_figure(pid):
    if pid == 0:
        visible = set(PERSONS.keys())
        roles = {p:"self" for p in PERSONS}
    else:
        roles = get_relations(pid)
        visible = set(roles.keys())

    fig = go.Figure()

    # unions
    for u in UNIONS:
        a,b = u["a"],u["b"]
        if a not in visible or b not in visible: continue
        ax,ay = POSITIONS[a]
        bx,by = POSITIONS[b]

        fig.add_shape(type="line",x0=ax,y0=ay,x1=bx,y1=by,
                      line=dict(color="#BBB",width=1.5,dash="dot"),
                      xref="paper",yref="paper")

        if u["marriage"]:
            mx,my=(ax+bx)/2,(ay+by)/2
            fig.add_annotation(x=mx,y=my+0.02,text=f"💍 {u['marriage']}",
                               showarrow=False,font=dict(size=10,color="#666"),
                               xref="paper",yref="paper")

    # filiations
    for p,c in FILIATIONS:
        if p not in visible or c not in visible: continue
        px,py=POSITIONS[p]; cx,cy=POSITIONS[c]
        my=(py+cy)/2
        fig.add_shape(type="line",x0=px,y0=py,x1=px,y1=my,
                      line=dict(color="#AAA"),xref="paper",yref="paper")
        fig.add_shape(type="line",x0=px,y0=my,x1=cx,y1=my,
                      line=dict(color="#AAA"),xref="paper",yref="paper")
        fig.add_shape(type="line",x0=cx,y0=my,x1=cx,y1=cy,
                      line=dict(color="#AAA"),xref="paper",yref="paper")

    xs,ys,texts,hovers=[],[],[],[]
    for p in visible:
        info=PERSONS[p]
        x,y=POSITIONS[p]

        tip=[f"<b>{info['name']}</b>"]
        if info["birth"]: tip.append(f"Né(e): {info['birth']}")
        if info["death"]: tip.append(f"Décédé(e): {info['death']}")

        for u in UNIONS:
            if p in (u["a"],u["b"]) and u["marriage"]:
                tip.append(f"💍 {u['marriage']}")

        xs.append(x); ys.append(y)
        texts.append(info["name"])
        hovers.append("<br>".join(tip))

    fig.add_trace(go.Scatter(
        x=xs,y=ys,mode="markers+text",
        text=texts,textposition="middle center",
        hovertext=hovers,hoverinfo="text",
        marker=dict(size=50,color="#FFF",line=dict(color="#333",width=2))
    ))

    fig.update_layout(
        paper_bgcolor="#FAF8F5",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=700
    )

    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Famille Piponnier")

    sorted_names = sorted(PERSONS.items(), key=lambda x:x[1]["name"])
    options = {"🌳 Voir tout l'arbre":0}
    options.update({v["name"]:k for k,v in sorted_names})

    choice = st.selectbox("Je suis…", list(options.keys()))
    chosen_id = options[choice]

# ── GRAPH ─────────────────────────────────────────────────────────────────
fig = build_figure(chosen_id)
st.plotly_chart(fig, use_container_width=True)
