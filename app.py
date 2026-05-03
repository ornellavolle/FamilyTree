import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Arbre Généalogique", layout="wide")

# ───────────────────────── STYLE ─────────────────────────
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🌳 Arbre généalogique</h1>", unsafe_allow_html=True)

# ───────────────────────── DONNÉES COMPLETES ─────────────────────────
PERSONS = {
    1: {"name":"François Piponnier","death":"29/01/1870","place":"Simandre","gender":"m"},
    2: {"name":"Claudine Viennois","gender":"f"},
    3: {"name":"Jean Claude Piponnier","birth":"02/08/1847","place":"Simandre","gender":"m"},
    4: {"name":"Marie Catherine Laurent","birth":"05/03/1839","gender":"f"},
    5: {"name":"Jean Claude Piponnier","birth":"09/07/1876","gender":"m"},
    6: {"name":"Louise Piponnier","birth":"10/04/1884","gender":"f"},
    7: {"name":"Marie Piponnier","birth":"10/10/1885","gender":"f"},
    8: {"name":"Jean Marie Piponnier","birth":"30/10/1887","death":"25/03/1977","gender":"m"},
    9: {"name":"Henriette Morin","gender":"f"},
    10: {"name":"Francis Piponnier","birth":"30/08/1890","gender":"m"},
    11: {"name":"Marguerite Piponnier","birth":"18/09/1895","gender":"f"},
    12: {"name":"Hortense Piponnier","gender":"f"},
    13: {"name":"Francis Pourprix","gender":"m"},
    14: {"name":"Nicole Pourprix","birth":"22/08/1943","gender":"f"},
    15: {"name":"Marie-France Pourprix","gender":"f"},
    16: {"name":"Mohamed El raiani","gender":"m"},
    17: {"name":"Florence El raiani","gender":"f"},
    18: {"name":"Natalie El raiani","gender":"f"},
    19: {"name":"Sandrine El raiani","birth":"02/08/1973","gender":"f"},
    20: {"name":"Régis Volle","birth":"23/03/1977","gender":"m"},
    21: {"name":"Jeanne Marie DuBuisson","gender":"f"},
}

FILIATIONS = [
    (1,3),(2,3),
    (3,5),(4,5),(3,6),(4,6),(3,7),(4,7),(3,8),(4,8),(3,10),(4,10),(3,11),(4,11),
    (8,12),(9,12),
    (12,14),(13,14),(12,15),(13,15),
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

# positions identiques à ton arbre initial
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

# ───────────────────────── UTILS ─────────────────────────
def get_gender_style(g):
    return {"m":("#DCEEF9","#3B7EC8","♂"),"f":("#FCE8F3","#C83B6E","♀")}.get(g,("#EEE","#999","?"))

def format_name(name):
    parts = name.split()
    if len(parts)<=2: return name
    mid=len(parts)//2
    return "<br>".join([" ".join(parts[:mid])," ".join(parts[mid:])])

def get_box_size(name):
    width = min(0.18, 0.06 + len(name)*0.0025)
    height = 0.05 + (0.015 if len(name)>18 else 0)
    return width,height

# ───────────────────────── FIGURE ─────────────────────────
def build_figure():
    fig = go.Figure()

    # unions
    for u in UNIONS:
        a,b=u["a"],u["b"]
        ax,ay=POSITIONS[a]
        bx,by=POSITIONS[b]

        fig.add_shape(type="line",x0=ax,y0=ay,x1=bx,y1=by,
                      line=dict(color="#BBB",dash="dot"),
                      xref="paper",yref="paper")

        if u["marriage"]:
            fig.add_annotation(
                x=(ax+bx)/2,
                y=(ay+by)/2+0.015,
                text=f"💍 {u['marriage']}",
                showarrow=False,
                font=dict(size=10,color="#666")
            )

    # filiations
    for p,c in FILIATIONS:
        px,py=POSITIONS[p]
        cx,cy=POSITIONS[c]
        my=(py+cy)/2

        fig.add_shape(type="line",x0=px,y0=py,x1=px,y1=my,line=dict(color="#AAA"))
        fig.add_shape(type="line",x0=px,y0=my,x1=cx,y1=my,line=dict(color="#AAA"))
        fig.add_shape(type="line",x0=cx,y0=my,x1=cx,y1=cy,line=dict(color="#AAA"))

    xs,ys,hovers=[],[],[]

    for pid,info in PERSONS.items():
        x,y=POSITIONS[pid]
        w,h=get_box_size(info["name"])
        fill,border,icon=get_gender_style(info.get("gender"))

        fig.add_shape(
            type="rect",
            x0=x-w/2,x1=x+w/2,y0=y-h/2,y1=y+h/2,
            line=dict(color=border,width=2),
            fillcolor=fill,
            xref="paper",yref="paper"
        )

        fig.add_annotation(
            x=x,y=y,
            text=f"{icon} {format_name(info['name'])}",
            showarrow=False,
            font=dict(size=11),
            align="center"
        )

        tip=f"<b>{info['name']}</b><br>"
        if info.get("birth"): tip+=f"🎂 {info['birth']}<br>"
        if info.get("death"): tip+=f"⚰️ {info['death']}<br>"
        if info.get("place"): tip+=f"📍 {info['place']}<br>"

        xs.append(x); ys.append(y); hovers.append(tip)

    fig.add_trace(go.Scatter(
        x=xs,y=ys,
        mode="markers",
        marker=dict(size=20,opacity=0),
        hovertext=hovers,
        hoverinfo="text"
    ))

    fig.update_layout(
        paper_bgcolor="#F7F5F2",
        plot_bgcolor="#F7F5F2",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=700
    )

    return fig

# ───────────────────────── APP ─────────────────────────
fig = build_figure()
st.plotly_chart(fig, use_container_width=True)
