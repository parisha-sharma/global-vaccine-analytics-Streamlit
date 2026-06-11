"""
Global Vaccination Analysis Dashboard
A premium data story built with WHO immunization data
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os, sys

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ── Brand palette ─────────────────────────────────────────────────────────────
GOLD   = "#C5AA6D"
CREAM  = "#F7E7CE"
BLUSH  = "#E7C1B3"
DARK   = "#7C6657"
BLACK  = "#1a1a1a"
REGION_COLORS = [GOLD, BLUSH, DARK, CREAM, "#a08c5b", "#d4b896"]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG + CSS
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Global Vaccination Analysis",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

:root {
    --bg:    #1a1a1a;
    --bg2:   #111111;
    --bg3:   #1e1e1e;
    --gold:  #C5AA6D;
    --cream: #F7E7CE;
    --blush: #E7C1B3;
    --dark:  #7C6657;
}
html, body, #root { background: var(--bg) !important; }
.stApp, .stApp > header { background: var(--bg) !important; }
.stApp [data-testid="stAppViewContainer"],
.stApp [data-testid="stAppViewContainer"] > section,
.stApp [data-testid="stAppViewContainer"] > section > div { background: var(--bg) !important; }
[data-testid="block-container"], .block-container {
    background: var(--bg) !important;
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1400px;
}
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
[data-testid="stMarkdownContainer"],
.element-container, .stMarkdown,
div[class*="st-emotion-cache"] { background: transparent !important; }
p, span, li, a, label, div { color: var(--cream) !important; font-family: 'Lato', sans-serif !important; }

/* Sidebar */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: var(--bg2) !important;
    border-right: 1px solid #2a2a2a !important;
    min-width: 240px !important;
}
section[data-testid="stSidebar"] * { color: var(--cream) !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.88rem;
    padding: 5px 0;
    cursor: pointer;
}
.stRadio > div { background: transparent !important; }

/* Hide header/toolbar */
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],
button[aria-label="Collapse sidebar"],
button[aria-label="Open sidebar"] {
    display: none !important; visibility: hidden !important;
}
section[data-testid="stSidebar"] {
    transform: none !important;
    width: 244px !important; min-width: 244px !important; max-width: 244px !important;
    left: 0 !important; position: relative !important;
    display: block !important; visibility: visible !important;
}

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--gold) !important; }
hr { border-color: #2a2a2a !important; }
#MainMenu, footer, header { visibility: hidden; }
iframe { background: #1a1a1a !important; border: none !important; }

.kpi-card {
    background: linear-gradient(135deg, #1f1f1f, #222);
    border: 1px solid #2a2a2a;
    border-top: 3px solid var(--gold);
    border-radius: 4px;
    padding: 1.4rem 1rem 1rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
    height: 100%;
}
.kpi-card:hover { transform: translateY(-3px); border-color: var(--gold); }
.kpi-number {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.1rem; font-weight: 700;
    color: var(--gold) !important; line-height: 1.1;
}
.kpi-label { font-size: 0.75rem; color: var(--blush) !important; margin-top: 0.4rem;
    line-height: 1.4; text-transform: uppercase; letter-spacing: 0.07em; }
.kpi-source { font-size: 0.62rem; color: var(--dark) !important; margin-top: 0.5rem; }

.story-text { font-size: 1.08rem; line-height: 1.95; color: var(--cream) !important; max-width: 860px; }
.story-text b { color: var(--gold) !important; }

.pull-quote {
    border-left: 3px solid var(--gold);
    padding: 0.8rem 1.5rem; margin: 1.8rem 0;
    font-family: 'Playfair Display', serif !important;
    font-style: italic; font-size: 1.12rem;
    color: var(--cream) !important;
    background: rgba(197,170,109,0.07);
    border-radius: 0 4px 4px 0;
}
.insight-box {
    background: rgba(197,170,109,0.07);
    border: 1px solid rgba(197,170,109,0.22);
    border-radius: 4px; padding: 1.2rem 1.5rem; margin: 1.2rem 0;
    font-size: 0.97rem; line-height: 1.78; color: var(--cream) !important;
}
.insight-box b { color: var(--gold) !important; }
.section-label { font-size: 0.68rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--dark) !important; margin-bottom: 0.2rem; }
.chart-caption { font-size: 0.8rem; color: var(--dark) !important; text-align: center;
    margin-top: 0.3rem; font-style: italic; }
.chapter-card {
    padding: 1.2rem; margin-bottom: 1rem;
    border: 1px solid #2a2a2a; border-radius: 4px;
    background: #1e1e1e; cursor: pointer;
    transition: border-color 0.2s, transform 0.15s;
}
.chapter-card:hover { border-color: var(--gold); transform: translateY(-2px); }
.stat-strip {
    background: #1e1e1e; border: 1px solid #2a2a2a; border-radius: 4px;
    padding: 1rem 1.5rem; display: flex; align-items: center; gap: 1rem; margin: 0.5rem 0;
}
.stat-strip-num { font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem; color: var(--gold) !important; min-width: 90px; font-weight: 700; }
.stat-strip-label { font-size: 0.85rem; color: var(--cream) !important; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    cov   = pd.read_excel(os.path.join(DATA_DIR, "coverage_data_cleaned.xlsx"))
    inc   = pd.read_excel(os.path.join(DATA_DIR, "incidence_rate_data_cleaned.xlsx"))
    cases = pd.read_excel(os.path.join(DATA_DIR, "reported_cases_data_cleaned.xlsx"))
    vi    = pd.read_excel(os.path.join(DATA_DIR, "vaccine_introduction_data_cleaned.xlsx"))
    vs    = pd.read_excel(os.path.join(DATA_DIR, "vaccine_schedule_data_cleaned.xlsx"))
    return cov, inc, cases, vi, vs

cov, inc, cases, vi, vs = load_data()

# ── Derived datasets (pre-computed for speed) ─────────────────────────────────

# Global coverage trend (WUENIC, all years)
gw = cov[(cov["GROUP"] == "GLOBAL") & (cov["COVERAGE_CATEGORY"] == "WUENIC")]

def global_trend(antigen):
    return gw[gw["ANTIGEN"] == antigen].sort_values("YEAR")[["YEAR", "COVERAGE"]]

# WHO region coverage 2023
who_cov_2023 = cov[
    (cov["GROUP"] == "WHO_REGIONS") & (cov["COVERAGE_CATEGORY"] == "WUENIC") & (cov["YEAR"] == 2023)
]
region_pivot = who_cov_2023[who_cov_2023["ANTIGEN"].isin(["DTPCV3","MCV1","BCG","POL3"])].pivot_table(
    index="NAME", columns="ANTIGEN", values="COVERAGE"
).reset_index()
region_pivot.columns = ["Region", "BCG", "DTP3", "MCV1", "Polio3"]

# Measles global cases by year
measles_cases = cases[(cases["DISEASE"] == "MEASLES") & (cases["GROUP"] == "COUNTRIES")].groupby("YEAR")["CASES"].sum().reset_index()

# Polio cases by year
polio_cases = cases[(cases["DISEASE"] == "POLIO") & (cases["GROUP"] == "COUNTRIES")].groupby("YEAR")["CASES"].sum().reset_index()

# Disease burden 2023 — countries
disease_2023 = cases[(cases["GROUP"] == "COUNTRIES") & (cases["YEAR"] == 2023)]
top_measles_2023 = disease_2023[disease_2023["DISEASE"] == "MEASLES"].nlargest(10, "CASES")[["NAME", "CASES"]]

# Vaccine introduction counts 2023
vi_2023_yes = vi[(vi["YEAR"] == 2023) & (vi["INTRO"] == "Yes")]
intro_counts = vi_2023_yes.groupby("DESCRIPTION")["COUNTRYNAME"].nunique().sort_values(ascending=False).reset_index()
intro_counts.columns = ["Vaccine", "Countries"]

# Development status DTP3
dev_cov = cov[(cov["GROUP"] == "DEVELOPMENT_STATUS") & (cov["COVERAGE_CATEGORY"] == "WUENIC") & (cov["YEAR"] == 2023) & (cov["ANTIGEN"] == "DTPCV3")]

# COVID dip: global DTPCV3 2018-2023
dtp3_trend = global_trend("DTPCV3")
mcv1_trend = global_trend("MCV1")
bcg_trend  = global_trend("BCG")
pol3_trend = global_trend("POL3")

# HPV cumulative intro by year
hpv_intro = vi[vi["DESCRIPTION"].str.contains("HPV", na=False) & (vi["INTRO"] == "Yes")]
hpv_cumul = hpv_intro.groupby("YEAR")["COUNTRYNAME"].nunique().sort_index().cumsum().reset_index()
hpv_cumul.columns = ["Year", "Countries"]

# WHO region incidence 2023
who_measles_inc = inc[
    (inc["DISEASE"] == "MEASLES") & (inc["GROUP"] == "WHO_REGIONS") & (inc["YEAR"] == 2023)
][["NAME", "INCIDENCE_RATE"]].copy()
who_measles_inc.columns = ["Region", "Incidence"]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def plotly_layout(fig, height=480, margin_r=60):
    fig.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=height,
        font=dict(color=CREAM, family="Lato"),
        margin=dict(l=10, r=margin_r, t=50, b=30),
    )
    return fig

def kpi_card(number, label, source=""):
    src = f'<div class="kpi-source">{source}</div>' if source else ""
    return f"""<div class="kpi-card">
        <div class="kpi-number">{number}</div>
        <div class="kpi-label">{label}</div>
        {src}</div>"""

def story(text):
    st.markdown(f'<div class="story-text">{text}</div>', unsafe_allow_html=True)

def pull_quote(text):
    st.markdown(f'<div class="pull-quote">{text}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def page_header(eyebrow, title, subtitle=""):
    st.markdown(f'<p class="section-label">{eyebrow}</p>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f'<p style="color:#E7C1B3 !important;font-size:1.05rem;margin-top:-0.6rem;max-width:780px;line-height:1.6;">{subtitle}</p>', unsafe_allow_html=True)
    st.markdown("---")

def glass_bar(fig):
    """Apply glassy look to bar charts with gradient colors"""
    for trace in fig.data:
        if hasattr(trace, 'marker'):
            trace.marker.update(
                opacity=0.88,
                line=dict(color="rgba(255,255,255,0.08)", width=0.5)
            )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 1.8rem;border-bottom:1px solid #2a2a2a;margin-bottom:1.5rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.05rem;
                    color:#C5AA6D !important;letter-spacing:0.12em;text-transform:uppercase;">
            VACCINATION REPORT
        </div>
        <div style="font-size:0.65rem;color:#7C6657 !important;letter-spacing:0.1em;margin-top:3px;">
            WHO Global Immunization Data
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;color:#7C6657;margin-bottom:0.5rem;">The Report</p>', unsafe_allow_html=True)

    pages = [
        "✦  The Story Begins",
        "01  Global Coverage Trends",
        "02  The COVID Disruption",
        "03  Disease Burden & Impact",
        "04  Where Gaps Persist",
        "05  New Vaccines, New Frontiers",
        "06  The Road to Eradication",
    ]

    if "page_select" not in st.session_state:
        st.session_state.page_select = pages[0]

    page = st.radio("", pages, label_visibility="collapsed", key="nav_radio",
                    index=pages.index(st.session_state.page_select))
    st.session_state.page_select = page

    st.markdown("""
    <div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #2a2a2a;">
        <p style="font-size:0.62rem;color:#555 !important;line-height:1.7;">
            Data sources:<br>
            WHO Immunization Data &bull;<br>
            WUENIC Estimates &bull;<br>
            WHO-UNICEF Joint Coverage<br><br>
            Coverage period: 1980–2023
        </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — THE STORY BEGINS
# ══════════════════════════════════════════════════════════════════════════════

if page == "✦  The Story Begins":

    st.markdown("""
    <div style="padding:3rem 0 1.5rem;">
        <p style="font-size:0.68rem;letter-spacing:0.22em;text-transform:uppercase;
                  color:#7C6657 !important;margin-bottom:0.6rem;">
            Global Health Intelligence &nbsp;✦&nbsp; WHO Data Report &nbsp;✦&nbsp; 2024
        </p>
        <h1 style="font-family:'Playfair Display',serif !important;font-size:3rem;
                   color:#C5AA6D !important;line-height:1.15;margin-bottom:0.8rem;">
            The Global Vaccination Analysis
        </h1>
        <p style="font-size:1.12rem;color:#E7C1B3 !important;max-width:700px;
                  line-height:1.75;margin-bottom:0;">
            A data investigation into 40 years of global immunization — which vaccines
            are winning, which diseases are retreating, and where the gaps remain.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    story("""
    Every year, vaccines prevent an estimated <b>3.5 to 5 million deaths</b> globally.
    Yet 14.3 million children in 2022 received none of the vaccines in routine immunization
    schedules — they are the "zero-dose" children, invisible to the system.
    <br><br>
    This report draws on four decades of WHO immunization data to answer one question:
    <b>what does the real trajectory of global vaccination look like — and where is the work still unfinished?</b>
    """)

    pull_quote(
        "In 1980, just 20% of children globally received the DTP3 vaccine. By 2023, that number is 84%. "
        "The ascent took 43 years. A single pandemic nearly reversed a decade of progress in two."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gauges row ────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">At a Glance — 2023</p>', unsafe_allow_html=True)
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    gauges = [
        (col_g1, 84, "DTP3 global coverage",    "WHO WUENIC 2023"),
        (col_g2, 83, "MCV1 global coverage",    "WHO WUENIC 2023"),
        (col_g3, 87, "BCG global coverage",     "WHO WUENIC 2023"),
        (col_g4, 83, "Polio3 global coverage",  "WHO WUENIC 2023"),
    ]
    for i, (col, val, label, source) in enumerate(gauges):
        with col:
            st.markdown(f'<p style="font-size:0.72rem;text-align:center;color:{CREAM};letter-spacing:0.04em;margin-bottom:0;line-height:1.4;">{label}</p>', unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val,
                number=dict(suffix="%", font=dict(color=GOLD, size=28, family="Playfair Display")),
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor=CREAM, tickfont=dict(color=CREAM, size=8)),
                    bar=dict(color=GOLD if val >= 80 else BLUSH, thickness=0.28),
                    bgcolor=BLACK, borderwidth=0,
                    steps=[dict(range=[0, 100], color="#222")],
                    threshold=dict(line=dict(color=CREAM, width=1.5), thickness=0.7, value=val),
                ),
            ))
            fig_g.update_layout(paper_bgcolor=BLACK, height=155, margin=dict(l=15,r=15,t=10,b=5), font=dict(color=CREAM))
            st.plotly_chart(
                fig_g,
                key=f"gauge_{i}",
                use_container_width=True,
            )
            st.markdown(f'<p class="chart-caption">{source}</p>', unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI grid ──────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">The Scale of What We Are Talking About</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    kpis = [
        ("5M+",  "deaths prevented by vaccines every year globally",      "WHO 2023"),
        ("84%",  "DTP3 global coverage in 2023 — up from 20% in 1980",   "WUENIC 2023"),
        ("14.3M","zero-dose children in 2022 — received no vaccines at all", "WHO 2023"),
        ("74%",  "Africa DTP3 coverage — lowest of any WHO region",       "WUENIC 2023"),
        ("95%",  "European Region DTP3 coverage — highest globally",      "WUENIC 2023"),
        ("133",  "countries have introduced HPV vaccine as of 2023",      "WHO 2023"),
        ("2M+",  "measles cases reported globally in 2023",               "WHO 2023"),
        ("538",  "polio cases in 2023 — down from 350,000 in 1988",       "WHO 2023"),
        ("121",  "countries now offer rotavirus vaccine in schedules",    "WHO 2023"),
        ("20pp", "COVID drop — DTP3 fell from 86% to 83% in two years",  "WUENIC 2021"),
        ("2034", "WHO target: 90% DTP3 in every country by this year",   "Immunization Agenda 2030"),
        ("194",  "countries offering IPV in 2023",                        "WHO 2023"),
    ]
    for row_start in range(0, len(kpis), 4):
        cols = st.columns(4)
        for col, (num, label, src) in zip(cols, kpis[row_start:row_start+4]):
            with col:
                st.markdown(kpi_card(num, label, src), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Snapshot overview chart ───────────────────────────────────────────────
    st.markdown('<p class="section-label">The Landscape at a Glance</p>', unsafe_allow_html=True)
    st.markdown("### WHO Region Coverage — Four Core Vaccines (2023)")
    story("Six regions. Four vaccines. The gap between Europe and Africa captures 40 years of inequity in a single chart.")
    st.markdown("<br>", unsafe_allow_html=True)

    fig_snap = go.Figure()
    vaccines = ["BCG", "DTP3", "MCV1", "Polio3"]
    vac_labels = {"BCG": "BCG (TB)", "DTP3": "DTP3", "MCV1": "Measles 1st", "Polio3": "Polio 3rd"}
    for i, (region_row) in region_pivot.iterrows():
        region = region_row["Region"]
        vals = [region_row.get(v, 0) for v in vaccines]
        fig_snap.add_trace(go.Bar(
            name=region, x=vaccines, y=vals,
            marker_color=REGION_COLORS[i % len(REGION_COLORS)],
            marker_opacity=0.88,
            marker_line=dict(color="rgba(255,255,255,0.08)", width=0.5),
            text=[f"{v:.0f}%" for v in vals], textposition="outside",
            textfont=dict(color=CREAM, size=9),
        ))
    fig_snap.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=420,
        barmode="group", margin=dict(l=10, r=10, t=30, b=30),
        font=dict(color=CREAM, family="Lato"),
        xaxis=dict(color=CREAM, gridcolor="#222"),
        yaxis=dict(color=CREAM, ticksuffix="%", gridcolor="#222", range=[0, 110]),
        legend=dict(bgcolor="#1e1e1e", bordercolor=DARK, borderwidth=1,
                    font=dict(color=CREAM, size=9), orientation="h", y=-0.15),
    )
    st.plotly_chart(fig_snap, key="fig_snap", use_container_width=True)
    st.markdown('<p class="chart-caption">WHO WUENIC estimates 2023. Six WHO regions, four core vaccines.</p>', unsafe_allow_html=True)

    pull_quote(
        "Europe sits at 95% DTP3. Africa sits at 74%. "
        "That 21-point gap represents millions of unvaccinated children and thousands of preventable deaths every year."
    )

    # ── Chapter cards ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-label">What This Report Covers</p>', unsafe_allow_html=True)
    st.markdown("## Six Chapters. The Full Story.")
    st.markdown("<br>", unsafe_allow_html=True)

    page_keys = {
        "01": "01  Global Coverage Trends",
        "02": "02  The COVID Disruption",
        "03": "03  Disease Burden & Impact",
        "04": "04  Where Gaps Persist",
        "05": "05  New Vaccines, New Frontiers",
        "06": "06  The Road to Eradication",
    }

    chapters = [
        ("01", "Global Coverage Trends",   "From 20% in 1980 to 84% in 2023. Four decades of progress across every core vaccine."),
        ("02", "The COVID Disruption",      "The pandemic reversed a decade of gains in 18 months. The recovery is still incomplete."),
        ("03", "Disease Burden and Impact", "Measles resurged to 2 million cases in 2023. Where vaccination fell, disease followed."),
        ("04", "Where Gaps Persist",        "Africa trails Europe by 21 points. Least-developed nations sit 20 points behind the global average."),
        ("05", "New Vaccines, New Frontiers","133 countries now offer HPV. 121 offer rotavirus. The schedule is growing."),
        ("06", "The Road to Eradication",   "Polio went from 350,000 cases in 1988 to 538 in 2023. What comes next?"),
    ]

    col_a, col_b = st.columns(2)
    for i, (num, title, desc) in enumerate(chapters):
        with (col_a if i % 2 == 0 else col_b):
            st.markdown(f"""
            <div class="chapter-card">
                <span class="section-label">Chapter {num}</span>
                <p style="font-family:'Playfair Display',serif !important;color:#C5AA6D !important;
                           font-size:1rem;margin:0.3rem 0 0.5rem;">{title}</p>
                <p style="font-size:0.88rem;color:#F7E7CE !important;line-height:1.65;margin:0 0 0.7rem 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Read Chapter {num} →", key=f"ch_btn_{num}", use_container_width=True):
                st.session_state.page_select = page_keys[num]
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — GLOBAL COVERAGE TRENDS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "01  Global Coverage Trends":

    page_header("Chapter 01", "Global Coverage Trends",
                "From 20% in 1980 to 84% in 2023. Forty-three years of immunization progress visualised.")

    story("""
    In 1980, the WHO recorded that just <b>20% of the world's children</b> were receiving the DTP3 vaccine.
    Healthcare infrastructure was sparse, cold chains were unreliable, and whole populations had never been
    reached by any formal health service. What followed was one of the largest coordinated health
    interventions in human history.
    """)

    pull_quote(
        "The rise from 20% to 84% DTP3 coverage did not happen by accident. "
        "It took four decades of sustained investment, political will, and last-mile logistics "
        "to reach children in the most remote corners of the world."
    )

    # ── Multi-vaccine trend chart ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Forty Years of Progress — Core Vaccines Global Coverage")

    fig_trend = go.Figure()
    vaccine_series = [
        (dtp3_trend, "DTP3", GOLD),
        (mcv1_trend, "MCV1 (Measles)", BLUSH),
        (bcg_trend,  "BCG (TB)", DARK),
        (pol3_trend, "Polio3", CREAM),
    ]
    for df_v, label, color in vaccine_series:
        df_v = df_v[df_v["YEAR"] >= 1980].copy()
        fig_trend.add_trace(go.Scatter(
            x=df_v["YEAR"], y=df_v["COVERAGE"],
            mode="lines", name=label,
            line=dict(color=color, width=2.2),
            fill="none",
            hovertemplate=f"<b>{label}</b><br>Year: %{{x}}<br>Coverage: %{{y}}%<extra></extra>",
        ))

    # COVID annotation
    fig_trend.add_vrect(x0=2019.5, x1=2021.5,
        fillcolor="rgba(231,193,179,0.08)", line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font=dict(color=BLUSH, size=9))

    fig_trend.add_annotation(x=2020, y=68, text="Coverage dip",
        showarrow=True, arrowhead=2, arrowcolor=BLUSH,
        font=dict(color=BLUSH, size=9), ax=40, ay=-30)

    fig_trend.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=440,
        margin=dict(l=10, r=10, t=30, b=30),
        font=dict(color=CREAM, family="Lato"),
        xaxis=dict(color=CREAM, gridcolor="#222", dtick=5),
        yaxis=dict(color=CREAM, ticksuffix="%", gridcolor="#222", range=[10, 105]),
        legend=dict(bgcolor="#1e1e1e", bordercolor=DARK, borderwidth=1,
                    font=dict(color=CREAM, size=10), x=0.01, y=0.99),
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, key="fig_trend", use_container_width=True)
    st.markdown('<p class="chart-caption">WUENIC global estimates 1980–2023. Sources: WHO/UNICEF Joint Coverage Estimates.</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── WHO region comparison ─────────────────────────────────────────────────
    st.markdown("### Where Each Region Stands Today — DTP3 Coverage 2023")
    st.markdown("<br>", unsafe_allow_html=True)

    region_dtp3 = who_cov_2023[who_cov_2023["ANTIGEN"] == "DTPCV3"][["NAME","COVERAGE"]].sort_values("COVERAGE", ascending=True)

    fig_reg = go.Figure(go.Bar(
        y=region_dtp3["NAME"], x=region_dtp3["COVERAGE"],
        orientation="h",
        marker=dict(
            color=[GOLD if v >= 90 else (BLUSH if v >= 80 else DARK) for v in region_dtp3["COVERAGE"]],
            opacity=0.9,
            line=dict(color="rgba(255,255,255,0.07)", width=0.5),
        ),
        text=[f"{v:.0f}%" for v in region_dtp3["COVERAGE"]],
        textposition="outside",
        textfont=dict(color=CREAM, size=11),
        hovertemplate="<b>%{y}</b><br>DTP3 Coverage: %{x}%<extra></extra>",
    ))
    fig_reg.add_vline(x=84, line_dash="dot", line_color=DARK, line_width=1.5,
                      annotation_text="Global avg 84%",
                      annotation_font=dict(color=CREAM, size=9))
    fig_reg.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=340,
        margin=dict(l=10, r=80, t=30, b=20),
        font=dict(color=CREAM, family="Lato"),
        xaxis=dict(range=[0, 110], color=CREAM, gridcolor="#222", ticksuffix="%"),
        yaxis=dict(color=CREAM),
        showlegend=False,
    )
    st.plotly_chart(fig_reg, key="fig_reg", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Development status strip
    st.markdown('<p class="section-label">Development Status vs. Coverage — 2023</p>', unsafe_allow_html=True)
    for _, row in dev_cov.iterrows():
        color = GOLD if row["COVERAGE"] >= 90 else (BLUSH if row["COVERAGE"] >= 80 else DARK)
        st.markdown(f"""<div class="stat-strip">
            <div class="stat-strip-num" style="color:{color} !important;">{row['COVERAGE']:.0f}%</div>
            <div class="stat-strip-label">{row['NAME']} — DTP3 coverage</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    insight("""
    <b>The equity gap in four numbers:</b><br><br>
    Developed economies sit at 94%. Economies in transition at 96%. Developing economies at 86%.
    Least-developed nations at 74%. The global headline of 84% masks a 22-point gap
    between the most and least developed nations. That gap represents the majority of the world's
    unvaccinated children. Reaching them requires not just vaccines, but roads, refrigerators,
    trained health workers, and community trust built over years.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — THE COVID DISRUPTION
# ══════════════════════════════════════════════════════════════════════════════

elif page == "02  The COVID Disruption":

    page_header("Chapter 02", "The COVID Disruption",
                "The pandemic did not just disrupt COVID care. It disrupted every vaccine for every child.")

    story("""
    When COVID-19 hit, health systems around the world pivoted overnight.
    Routine immunization clinics were closed. Supply chains broke down.
    Health workers were redeployed. Parents stayed home, afraid to bring
    their children to health facilities.
    <br><br>
    The result: <b>global DTP3 coverage fell from 86% in 2019 to 81% in 2021</b>
    — the largest single drop in the 40-year dataset. Measles coverage fell identically.
    """)

    pull_quote(
        "25 million children missed routine vaccines in 2021 alone. "
        "It was the largest sustained decline in childhood vaccination in 30 years — WHO, 2022."
    )

    # ── COVID dip focus chart ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    fig_covid = go.Figure()
    dtp3_recent = dtp3_trend[dtp3_trend["YEAR"] >= 2010].copy()
    mcv1_recent = mcv1_trend[mcv1_trend["YEAR"] >= 2010].copy()

    fig_covid.add_trace(go.Scatter(
        x=dtp3_recent["YEAR"], y=dtp3_recent["COVERAGE"],
        mode="lines+markers", name="DTP3",
        line=dict(color=GOLD, width=2.5),
        marker=dict(size=7, color=GOLD, line=dict(color=BLACK, width=1)),
        fill="tozeroy", fillcolor="rgba(197,170,109,0.08)",
        hovertemplate="<b>DTP3</b> %{x}: %{y}%<extra></extra>",
    ))
    fig_covid.add_trace(go.Scatter(
        x=mcv1_recent["YEAR"], y=mcv1_recent["COVERAGE"],
        mode="lines+markers", name="MCV1 (Measles)",
        line=dict(color=BLUSH, width=2.5),
        marker=dict(size=7, color=BLUSH, line=dict(color=BLACK, width=1)),
        fill="tozeroy", fillcolor="rgba(231,193,179,0.05)",
        hovertemplate="<b>MCV1</b> %{x}: %{y}%<extra></extra>",
    ))

    for yr, txt, ax, ay in [
        (2020, "COVID begins", -50, -40),
        (2021, "25M missed vaccines", 40, -50),
        (2023, "Recovery underway", 30, -40),
    ]:
        fig_covid.add_annotation(x=yr, y=dtp3_trend[dtp3_trend["YEAR"]==yr]["COVERAGE"].values[0],
            text=txt, showarrow=True, arrowhead=2, arrowcolor=CREAM,
            font=dict(color=CREAM, size=9), bgcolor=BLACK, bordercolor=DARK,
            borderwidth=1, ax=ax, ay=ay)

    fig_covid.add_vrect(x0=2019.8, x1=2022.2,
        fillcolor="rgba(231,193,179,0.06)", line_width=0)

    fig_covid.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=400,
        margin=dict(l=10, r=20, t=40, b=30),
        font=dict(color=CREAM, family="Lato"),
        xaxis=dict(color=CREAM, gridcolor="#222", dtick=1),
        yaxis=dict(color=CREAM, ticksuffix="%", gridcolor="#222", range=[70, 92]),
        legend=dict(bgcolor="#1e1e1e", bordercolor=DARK, borderwidth=1,
                    font=dict(color=CREAM, size=10)),
        hovermode="x unified",
        title=dict(text="Global DTP3 and MCV1 Coverage 2010–2023 — The COVID Drop",
                   font=dict(color=GOLD, size=13), x=0.5),
    )
    st.plotly_chart(fig_covid, key="fig_covid", use_container_width=True)
    st.markdown('<p class="chart-caption">Coverage fell in 2020–2021 across all vaccines simultaneously. The recovery in 2022–2023 is partial.</p>', unsafe_allow_html=True)

    # ── Before / after comparison ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### The Drop and the Recovery — Side by Side")
    c1, c2 = st.columns(2)

    pre_covid = {"DTP3": 86, "MCV1": 86, "BCG": 89, "POL3": 86, "HepB3": 86}
    nadir     = {"DTP3": 81, "MCV1": 81, "BCG": 85, "POL3": 81, "HepB3": 81}
    current   = {"DTP3": 84, "MCV1": 83, "BCG": 87, "POL3": 83, "HepB3": 83}

    with c1:
        fig_before = go.Figure()
        x_vals = list(pre_covid.keys())
        fig_before.add_trace(go.Bar(name="2019 (Pre-COVID)", x=x_vals,
            y=list(pre_covid.values()), marker_color=GOLD, marker_opacity=0.85,
            marker_line=dict(color="rgba(255,255,255,0.08)", width=0.5),
            text=[f"{v}%" for v in pre_covid.values()], textposition="outside",
            textfont=dict(color=CREAM, size=9)))
        fig_before.add_trace(go.Bar(name="2021 (COVID trough)", x=x_vals,
            y=list(nadir.values()), marker_color=DARK, marker_opacity=0.85,
            marker_line=dict(color="rgba(255,255,255,0.08)", width=0.5),
            text=[f"{v}%" for v in nadir.values()], textposition="outside",
            textfont=dict(color=CREAM, size=9)))
        fig_before.update_layout(
            paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=300, barmode="group",
            margin=dict(l=10,r=10,t=40,b=20), font=dict(color=CREAM, size=10),
            title=dict(text="Pre-COVID vs. COVID Trough", font=dict(color=GOLD, size=11), x=0.5),
            xaxis=dict(color=CREAM, gridcolor="#222"),
            yaxis=dict(color=CREAM, ticksuffix="%", gridcolor="#222", range=[70, 96]),
            legend=dict(bgcolor="#1e1e1e", font=dict(color=CREAM, size=9),
                        bordercolor=DARK, borderwidth=1),
        )
        st.plotly_chart(fig_before, key="fig_before", use_container_width=True)

    with c2:
        recovery = {k: current[k] - nadir[k] for k in pre_covid}
        remaining_gap = {k: pre_covid[k] - current[k] for k in pre_covid}
        fig_rec = go.Figure()
        fig_rec.add_trace(go.Bar(name="Recovered (pp)", x=list(recovery.keys()),
            y=list(recovery.values()), marker_color=GOLD, marker_opacity=0.85,
            marker_line=dict(color="rgba(255,255,255,0.08)", width=0.5),
            text=[f"+{v}pp" for v in recovery.values()], textposition="inside",
            textfont=dict(color=BLACK, size=9, family="Lato")))
        fig_rec.add_trace(go.Bar(name="Still behind pre-COVID (pp)", x=list(remaining_gap.keys()),
            y=list(remaining_gap.values()), marker_color=BLUSH, marker_opacity=0.7,
            marker_line=dict(color="rgba(255,255,255,0.08)", width=0.5),
            text=[f"-{v}pp" for v in remaining_gap.values()], textposition="inside",
            textfont=dict(color=BLACK, size=9, family="Lato")))
        fig_rec.update_layout(
            paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=300, barmode="stack",
            margin=dict(l=10,r=10,t=40,b=20), font=dict(color=CREAM, size=10),
            title=dict(text="Recovery Progress — How Much Remains?", font=dict(color=GOLD, size=11), x=0.5),
            xaxis=dict(color=CREAM, gridcolor="#222"),
            yaxis=dict(color=CREAM, ticksuffix="pp", gridcolor="#222"),
            legend=dict(bgcolor="#1e1e1e", font=dict(color=CREAM, size=9),
                        bordercolor=DARK, borderwidth=1),
        )
        st.plotly_chart(fig_rec, key="fig_rec", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    insight("""
    <b>The recovery is real but incomplete:</b><br><br>
    All five core vaccines have partially recovered since the 2021 trough.
    But none has returned to pre-COVID levels. <b>DTP3 stands at 84% in 2023 — two points below its 2019 peak.</b>
    Those two points represent roughly 2.7 million additional children per year who are not receiving this vaccine
    compared to the pre-pandemic baseline. The immunization system is healing, but the wound is not fully closed.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DISEASE BURDEN AND IMPACT
# ══════════════════════════════════════════════════════════════════════════════

elif page == "03  Disease Burden & Impact":

    page_header("Chapter 03", "Disease Burden and Impact",
                "When coverage falls, disease returns. The data makes this relationship brutally clear.")

    story("""
    The purpose of vaccination is to prevent disease. When vaccines work, diseases disappear.
    When vaccines are missed, diseases return. This chapter examines the actual disease burden
    data alongside coverage trends — <b>the relationship is direct and unforgiving.</b>
    """)

    pull_quote(
        "Measles cases globally surged to 1.99 million in 2023 — more than four times the 2016 low. "
        "The correlation with the COVID-driven coverage drop is not coincidence. It is cause and effect."
    )

    # ── Measles trend ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    measles_recent = measles_cases[measles_cases["YEAR"] >= 2000].copy()

    c1, c2 = st.columns([1.5, 1])
    with c1:
        fig_measles = go.Figure()
        colors_m = [GOLD if v < 700000 else BLUSH if v < 1500000 else DARK for v in measles_recent["CASES"]]
        fig_measles.add_trace(go.Bar(
            x=measles_recent["YEAR"], y=measles_recent["CASES"],
            marker=dict(color=colors_m, opacity=0.88,
                        line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
            text=[f"{v/1e6:.1f}M" if v > 1e6 else f"{v/1e3:.0f}K" for v in measles_recent["CASES"]],
            textposition="outside", textfont=dict(color=CREAM, size=8),
            hovertemplate="<b>%{x}</b><br>Cases: %{y:,}<extra></extra>",
        ))
        fig_measles.add_annotation(x=2023, y=1991498,
            text="1.99M in 2023", showarrow=True, arrowhead=2, arrowcolor=DARK,
            font=dict(color=DARK, size=9), ax=40, ay=-35)
        fig_measles.update_layout(
            paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=320,
            margin=dict(l=10,r=30,t=40,b=20), font=dict(color=CREAM, size=9),
            title=dict(text="Global Measles Cases 2000–2023",
                       font=dict(color=GOLD, size=12), x=0.5),
            xaxis=dict(color=CREAM, gridcolor="#222", dtick=2),
            yaxis=dict(color=CREAM, gridcolor="#222",
                       tickformat=",", title="Cases"),
            showlegend=False,
        )
        st.plotly_chart(fig_measles, key="fig_measles", use_container_width=True)

    with c2:
        # WHO region incidence 2023
        who_meas_sorted = who_measles_inc.sort_values("Incidence", ascending=True)
        inc_colors = [GOLD if v < 10 else (BLUSH if v < 100 else DARK) for v in who_meas_sorted["Incidence"]]
        fig_inc = go.Figure(go.Bar(
            y=who_meas_sorted["Region"], x=who_meas_sorted["Incidence"],
            orientation="h",
            marker=dict(color=inc_colors, opacity=0.88,
                        line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
            text=[f"{v:.0f}" for v in who_meas_sorted["Incidence"]],
            textposition="outside", textfont=dict(color=CREAM, size=10),
            hovertemplate="<b>%{y}</b><br>Incidence: %{x} per 1M<extra></extra>",
        ))
        fig_inc.update_layout(
            paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=320,
            margin=dict(l=10,r=50,t=40,b=20), font=dict(color=CREAM, size=9),
            title=dict(text="Measles Incidence by Region 2023<br><sup>per 1,000,000 population</sup>",
                       font=dict(color=GOLD, size=12), x=0.5),
            xaxis=dict(color=CREAM, gridcolor="#222"),
            yaxis=dict(color=CREAM),
            showlegend=False,
        )
        st.plotly_chart(fig_inc, key="fig_inc", use_container_width=True)

    # ── Top countries ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Where Measles Hit Hardest — Top 10 Countries 2023")

    top10 = top_measles_2023.sort_values("CASES", ascending=True)
    colors_top = [DARK if v < 20000 else (BLUSH if v < 50000 else GOLD) for v in top10["CASES"]]
    fig_top = go.Figure(go.Bar(
        y=top10["NAME"], x=top10["CASES"], orientation="h",
        marker=dict(color=colors_top, opacity=0.88,
                    line=dict(color="rgba(255,255,255,0.06)", width=0.5)),
        text=[f"{v:,}" for v in top10["CASES"]],
        textposition="outside", textfont=dict(color=CREAM, size=10),
        hovertemplate="<b>%{y}</b><br>Cases: %{x:,}<extra></extra>",
    ))
    fig_top.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=340,
        margin=dict(l=10,r=80,t=30,b=20), font=dict(color=CREAM, family="Lato"),
        xaxis=dict(color=CREAM, gridcolor="#222", tickformat=","),
        yaxis=dict(color=CREAM),
        showlegend=False,
    )
    st.plotly_chart(fig_top, key="fig_top", use_container_width=True)
    st.markdown('<p class="chart-caption">DRC led with 311,500 cases in 2023 — a direct consequence of chronically low MCV coverage. Source: WHO.</p>', unsafe_allow_html=True)

    # ── Polio trend ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Polio — The Near-Eradication Story")
    polio_recent = polio_cases[polio_cases["YEAR"] >= 1988].copy()

    fig_polio = go.Figure()
    fig_polio.add_trace(go.Scatter(
        x=polio_recent["YEAR"], y=polio_recent["CASES"],
        mode="lines+markers", fill="tozeroy",
        fillcolor="rgba(197,170,109,0.10)",
        line=dict(color=GOLD, width=2.5),
        marker=dict(size=6, color=GOLD, line=dict(color=BLACK, width=1)),
        hovertemplate="<b>%{x}</b><br>Polio cases: %{y:,}<extra></extra>",
    ))
    for yr, cases_val, txt, ax, ay in [
        (1988, 350000, "~350,000 cases (est.)", 50, -30),
        (2016, 42,     "42 cases", 50, -40),
        (2023, 538,    "538 cases", 40, -40),
    ]:
        fig_polio.add_annotation(x=yr, y=cases_val, text=txt,
            showarrow=True, arrowhead=2, arrowcolor=CREAM,
            font=dict(color=CREAM, size=9), bgcolor=BLACK, bordercolor=DARK, borderwidth=1,
            ax=ax, ay=ay)

    fig_polio.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=320,
        margin=dict(l=10,r=20,t=40,b=30), font=dict(color=CREAM, family="Lato"),
        title=dict(text="Global Wild Polio Cases — The Long Road Down",
                   font=dict(color=GOLD, size=13), x=0.5),
        xaxis=dict(color=CREAM, gridcolor="#222", dtick=4),
        yaxis=dict(color=CREAM, gridcolor="#222", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig_polio, key="fig_polio_ch3", use_container_width=True)

    insight("""
    <b>The measles-polio contrast:</b><br><br>
    Polio is a story of sustained success — from 350,000 cases to 538 over 35 years of relentless
    vaccination campaigns. Measles is a story of fragile progress: it was nearly eliminated in many
    regions by 2016, then COVID unravelled a decade of gains and cases surged fourfold.
    The difference is not the vaccine — both are highly effective. It is the consistency of delivery.
    <b>Measles requires 95% coverage to prevent outbreaks. The world is at 83%.</b>
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — WHERE GAPS PERSIST
# ══════════════════════════════════════════════════════════════════════════════

elif page == "04  Where Gaps Persist":

    page_header("Chapter 04", "Where Gaps Persist",
                "The global headline hides a 21-point chasm between the most and least vaccinated regions.")

    story("""
    The 84% global DTP3 coverage sounds reassuring until you disaggregate it.
    The European Region reaches 95%. The African Region reaches 74%.
    Every year that gap remains, hundreds of thousands of children in Africa
    contract diseases that a simple, inexpensive vaccine would have prevented.
    """)

    pull_quote(
        "The Democratic Republic of Congo reported 311,500 measles cases in 2023. "
        "Its MCV1 coverage was 57%. The vaccine exists. The delivery system is the gap."
    )

    # ── Heatmap: all regions, all vaccines ───────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    heat_antigens = ["BCG", "DTPCV3", "MCV1", "POL3", "HEPB3", "PCV3", "ROTAC"]
    heat_labels   = {"BCG": "BCG (TB)", "DTPCV3": "DTP3", "MCV1": "Measles 1st",
                     "POL3": "Polio 3rd", "HEPB3": "HepB 3rd", "PCV3": "PCV 3rd", "ROTAC": "Rotavirus"}

    heat_data = []
    for antigen in heat_antigens:
        row = who_cov_2023[who_cov_2023["ANTIGEN"] == antigen][["NAME","COVERAGE"]]
        if not row.empty:
            heat_data.append(row.set_index("NAME")["COVERAGE"].rename(antigen))
    if heat_data:
        heat_df = pd.concat(heat_data, axis=1).fillna(0)
        heat_df = heat_df.rename(columns=heat_labels)
        heat_df.index = [r.replace("Region of the ", "").replace(" Region", "").replace("Eastern Mediterranean", "E. Mediterranean").replace("South-East Asia", "SE Asia").replace("Western Pacific", "W. Pacific") for r in heat_df.index]

        fig_heat = go.Figure(go.Heatmap(
            z=heat_df.values,
            x=list(heat_df.columns),
            y=list(heat_df.index),
            text=[[f"{v:.0f}%" for v in row] for row in heat_df.values],
            texttemplate="%{text}",
            textfont=dict(size=11, color=BLACK),
            colorscale=[[0, "#2a2a2a"], [0.5, DARK], [0.75, BLUSH], [1, GOLD]],
            zmin=40, zmax=100,
            showscale=True,
            colorbar=dict(
                tickfont=dict(color=CREAM, size=9),
                title=dict(text="Coverage %", font=dict(color=CREAM, size=9)),
                outlinecolor=DARK, outlinewidth=1,
            ),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.0f}%<extra></extra>",
        ))
        fig_heat.update_layout(
            paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=380,
            margin=dict(l=10,r=60,t=40,b=20),
            font=dict(color=CREAM, family="Lato"),
            title=dict(text="WHO Region Coverage Heatmap — 7 Vaccines, 2023",
                       font=dict(color=GOLD, size=12), x=0.5),
            xaxis=dict(color=CREAM, tickangle=-20),
            yaxis=dict(color=CREAM),
        )
        st.plotly_chart(fig_heat, key="fig_heat", use_container_width=True)
        st.markdown('<p class="chart-caption">Gold = high coverage. Dark = low coverage. Every empty cell is a gap in delivery. Sources: WHO WUENIC 2023.</p>', unsafe_allow_html=True)

    # ── Divergence chart ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### The Coverage Gap — Each Region vs. Global Average (DTP3)")

    region_dtp3 = who_cov_2023[who_cov_2023["ANTIGEN"] == "DTPCV3"][["NAME","COVERAGE"]].copy()
    global_avg = 84
    region_dtp3["Delta"] = region_dtp3["COVERAGE"] - global_avg
    region_dtp3 = region_dtp3.sort_values("Delta")

    fig_div = go.Figure()
    for _, row in region_dtp3.iterrows():
        color = GOLD if row["Delta"] > 0 else BLUSH
        fig_div.add_trace(go.Bar(
            x=[row["Delta"]], y=[row["NAME"]], orientation="h",
            marker_color=color, marker_opacity=0.88,
            marker_line=dict(color="rgba(255,255,255,0.07)", width=0.5),
            text=f"{'+' if row['Delta']>0 else ''}{row['Delta']:.0f}pp",
            textposition="outside", textfont=dict(color=CREAM, size=10),
            hovertemplate=f"<b>{row['NAME']}</b><br>Coverage: {row['COVERAGE']:.0f}%<extra></extra>",
            showlegend=False,
        ))
    fig_div.add_vline(x=0, line_color=CREAM, line_width=1.5,
                      annotation_text=f"Global avg {global_avg}%",
                      annotation_font=dict(color=CREAM, size=9), annotation_position="top")
    fig_div.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=320,
        margin=dict(l=10,r=80,t=40,b=20), font=dict(color=CREAM, family="Lato"),
        xaxis=dict(range=[-15, 15], color=CREAM, gridcolor="#222", zeroline=False),
        yaxis=dict(color=CREAM), showlegend=False,
    )
    st.plotly_chart(fig_div, key="fig_div", use_container_width=True)

    insight("""
    <b>The regional divide in plain terms:</b><br><br>
    <b>European Region (+11pp above average):</b> Near-universal coverage, strong health systems, mandatory schedules in many countries.<br><br>
    <b>Western Pacific (+8pp):</b> Strong NIP programs, high urbanization aiding reach.<br><br>
    <b>African Region (-10pp below average):</b> Conflict zones, weak cold chains, healthcare worker shortages,
    and vast rural populations without access to routine services.
    Closing this gap is the central challenge of Immunization Agenda 2030.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — NEW VACCINES, NEW FRONTIERS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "05  New Vaccines, New Frontiers":

    page_header("Chapter 05", "New Vaccines, New Frontiers",
                "The immunization schedule is expanding. HPV, rotavirus, PCV — a new era of protection.")

    story("""
    The original EPI (Expanded Programme on Immunization) in 1974 included six vaccines.
    By 2023, national schedules in high-income countries often include 14 or more.
    <b>Three vaccines define this new frontier</b>: HPV against cervical cancer,
    PCV against pneumonia, and rotavirus vaccine against the leading cause of child diarrheal death.
    """)

    pull_quote(
        "133 countries have now introduced HPV vaccine. In 2006, it was zero. "
        "That expansion represents one of the fastest rollouts of a new vaccine in history."
    )

    # ── Introduction counts chart ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    top_intro = intro_counts.head(12).sort_values("Countries", ascending=True)

    colors_intro = [GOLD if v >= 150 else (BLUSH if v >= 100 else DARK) for v in top_intro["Countries"]]
    fig_intro = go.Figure(go.Bar(
        y=top_intro["Vaccine"], x=top_intro["Countries"],
        orientation="h",
        marker=dict(color=colors_intro, opacity=0.88,
                    line=dict(color="rgba(255,255,255,0.07)", width=0.5)),
        text=[f"{v}" for v in top_intro["Countries"]],
        textposition="outside", textfont=dict(color=CREAM, size=10),
        hovertemplate="<b>%{y}</b><br>Countries: %{x}<extra></extra>",
    ))
    fig_intro.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=400,
        margin=dict(l=10,r=60,t=40,b=20), font=dict(color=CREAM, family="Lato"),
        title=dict(text="Countries That Have Introduced Each Vaccine — 2023",
                   font=dict(color=GOLD, size=12), x=0.5),
        xaxis=dict(range=[0, 220], color=CREAM, gridcolor="#222",
                   title="Number of countries"),
        yaxis=dict(color=CREAM), showlegend=False,
    )
    st.plotly_chart(fig_intro, key="fig_intro", use_container_width=True)
    st.markdown('<p class="chart-caption">IPV leads with 194 countries, followed by Hib (193) and HepB (190). HPV, rotavirus, and PCV are newer but expanding rapidly. Source: WHO 2023.</p>', unsafe_allow_html=True)

    # ── HPV cumulative rollout ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### HPV Vaccine Rollout — Cumulative Country Introductions")

    hpv_plot = hpv_cumul[hpv_cumul["Year"] >= 2006].copy()
    fig_hpv = go.Figure()
    fig_hpv.add_trace(go.Scatter(
        x=hpv_plot["Year"], y=hpv_plot["Countries"],
        mode="lines+markers", fill="tozeroy",
        fillcolor="rgba(197,170,109,0.10)",
        line=dict(color=GOLD, width=2.5),
        marker=dict(size=7, color=GOLD, line=dict(color=BLACK, width=1)),
        hovertemplate="<b>%{x}</b><br>Countries with HPV: %{y}<extra></extra>",
    ))
    fig_hpv.add_annotation(x=2006, y=hpv_plot[hpv_plot["Year"]==2006]["Countries"].values[0] if 2006 in hpv_plot["Year"].values else 0,
        text="First introductions<br>(2006)", showarrow=True, arrowhead=2, arrowcolor=BLUSH,
        font=dict(color=BLUSH, size=9), ax=50, ay=-40)

    fig_hpv.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=300,
        margin=dict(l=10,r=20,t=40,b=30), font=dict(color=CREAM, family="Lato"),
        title=dict(text="HPV Vaccine: Cumulative Country Rollout 2006–2023",
                   font=dict(color=GOLD, size=12), x=0.5),
        xaxis=dict(color=CREAM, gridcolor="#222", dtick=2),
        yaxis=dict(color=CREAM, gridcolor="#222", title="Countries (cumulative)"),
        showlegend=False,
    )
    st.plotly_chart(fig_hpv, key="fig_hpv", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        new_vax = {
            "HPV (Cervical Cancer)": 133,
            "PCV (Pneumonia)": 159,
            "Rotavirus": 121,
            "HepB birth dose": 115,
            "IPV 2nd dose": 151,
            "Influenza (seasonal)": 128,
        }
        fig_bubble = go.Figure(go.Scatter(
            x=list(range(len(new_vax))),
            y=[50] * len(new_vax),
            mode="markers+text",
            marker=dict(
                size=[c/3.5 for c in new_vax.values()],
                color=[GOLD, BLUSH, DARK, CREAM, "#a08c5b", BLUSH],
                opacity=0.8,
                line=dict(color="rgba(255,255,255,0.12)", width=1.5),
            ),
            text=list(new_vax.keys()),
            textposition="top center",
            textfont=dict(color=CREAM, size=8, family="Lato"),
            hovertemplate="<b>%{text}</b><br>Countries: " + "<br>".join([f"{v}" for v in new_vax.values()]) + "<extra></extra>",
        ))
        # Override hover to show per-vaccine count
        for i, (vax, cnt) in enumerate(new_vax.items()):
            fig_bubble.data[0].customdata = [[cnt]] * len(new_vax)
        fig_bubble.update_layout(
            paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=260,
            margin=dict(l=10,r=10,t=40,b=50),
            title=dict(text="Bubble size = countries adopting",
                       font=dict(color=GOLD, size=11), x=0.5),
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            showlegend=False, font=dict(color=CREAM),
        )
        st.plotly_chart(fig_bubble, key="fig_bubble", use_container_width=True)

    with c2:
        story("""
        <b>PCV leads with 159 countries</b> — pneumococcal disease kills hundreds of thousands
        of children annually, and the vaccine rollout has been accelerated by GAVI support
        for lower-income nations.<br><br>
        <b>HPV at 133 countries</b> — from zero in 2006 to more than two-thirds of all nations.
        But HPV coverage in the countries that have introduced it still lags for girls in
        low-income settings — infrastructure and cold chain remain the bottleneck.
        """)

    insight("""
    <b>Why these three vaccines matter beyond their individual diseases:</b><br><br>
    PCV, rotavirus, and HPV together address three of the top causes of child and adolescent mortality
    globally — pneumonia, diarrheal disease, and cervical cancer. Their rapid adoption shows
    what is possible when global health financing mechanisms like GAVI work effectively.
    The challenge now is ensuring that introduction translates to high coverage —
    a country can introduce a vaccine and still only reach 40% of its children.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — THE ROAD TO ERADICATION
# ══════════════════════════════════════════════════════════════════════════════

elif page == "06  The Road to Eradication":

    page_header("Chapter 06", "The Road to Eradication",
                "Polio went from 350,000 cases to 538. Measles nearly did the same — then fell back. What comes next?")

    story("""
    The word <b>"eradication"</b> has only been achieved once in human history — smallpox, in 1980.
    Polio is the second candidate, within reach but not yet crossed. Measles is the third
    candidate, a possibility for some regions, a distant goal globally.
    <br><br>
    This chapter looks at the trajectory of both diseases and what the data says about
    whether eradication — or at least elimination — is achievable.
    """)

    pull_quote(
        "Smallpox was eradicated in 1980 after 10 years of coordinated global effort. "
        "The polio campaign began in 1988. In 2025, we are still not across the finish line. "
        "The last mile is always the longest."
    )

    # ── Polio full timeline ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    all_polio = polio_cases.copy()
    all_polio = all_polio[all_polio["YEAR"] >= 1988]

    fig_polio = go.Figure()
    fig_polio.add_trace(go.Scatter(
        x=all_polio["YEAR"], y=all_polio["CASES"],
        mode="lines+markers", fill="tozeroy",
        fillcolor="rgba(197,170,109,0.10)",
        line=dict(color=GOLD, width=2.5),
        marker=dict(size=6, color=GOLD, line=dict(color=BLACK, width=1)),
        hovertemplate="<b>%{x}</b><br>Polio cases: %{y:,}<extra></extra>",
    ))

    milestones = [
        (1988, 350000, "GPEI launches<br>~350K cases (est.)", 60, -35),
        (2000, 2971,   "2,971 cases<br>2000", 50, -40),
        (2016, 42,     "42 cases — all-time low", 50, -40),
        (2020, 1113,   "COVID year: 1,113", 50, 40),
        (2023, 538,    "538 in 2023", 50, -40),
    ]
    for yr, val, txt, ax, ay in milestones:
        matching = all_polio[all_polio["YEAR"] == yr]["CASES"]
        if not matching.empty:
            fig_polio.add_annotation(x=yr, y=matching.values[0], text=txt,
                showarrow=True, arrowhead=2, arrowcolor=BLUSH,
                font=dict(color=BLUSH, size=8), bgcolor=BLACK, bordercolor=DARK,
                borderwidth=1, ax=ax, ay=ay)

    fig_polio.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=380,
        margin=dict(l=10,r=20,t=50,b=30), font=dict(color=CREAM, family="Lato"),
        title=dict(text="Global Polio Cases 1988–2023 — 35 Years of Progress",
                   font=dict(color=GOLD, size=13), x=0.5),
        xaxis=dict(color=CREAM, gridcolor="#222", dtick=4),
        yaxis=dict(color=CREAM, gridcolor="#222", tickformat=",", title="Cases"),
        showlegend=False,
    )
    st.plotly_chart(fig_polio, key="fig_polio_ch6", use_container_width=True)

    # ── Measles + target lines ────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Measles — Proof That Progress Is Fragile")

    fig_meas2 = go.Figure()
    measles_all = measles_cases[measles_cases["YEAR"] >= 2000].copy()
    fig_meas2.add_trace(go.Scatter(
        x=measles_all["YEAR"], y=measles_all["CASES"],
        mode="lines+markers", fill="tozeroy",
        fillcolor="rgba(231,193,179,0.08)",
        line=dict(color=BLUSH, width=2.5),
        marker=dict(size=6, color=BLUSH, line=dict(color=BLACK, width=1)),
        hovertemplate="<b>%{x}</b><br>Measles cases: %{y:,}<extra></extra>",
    ))
    fig_meas2.add_hline(y=500000, line_dash="dot", line_color=DARK, line_width=1.5,
                        annotation_text="IA2030 target threshold",
                        annotation_font=dict(color=DARK, size=9))

    for yr, txt, ax, ay in [(2016, "397K — historic low", 50, -40), (2019, "2.6M — resurgence", 50, 35), (2023, "1.99M in 2023", 40, -40)]:
        matching = measles_all[measles_all["YEAR"] == yr]["CASES"]
        if not matching.empty:
            fig_meas2.add_annotation(x=yr, y=matching.values[0], text=txt,
                showarrow=True, arrowhead=2, arrowcolor=GOLD,
                font=dict(color=GOLD, size=9), bgcolor=BLACK, bordercolor=DARK,
                borderwidth=1, ax=ax, ay=ay)

    fig_meas2.update_layout(
        paper_bgcolor=BLACK, plot_bgcolor=BLACK, height=350,
        margin=dict(l=10,r=20,t=50,b=30), font=dict(color=CREAM, family="Lato"),
        title=dict(text="Global Measles Cases 2000–2023 — The Rise, the Fall, the Resurgence",
                   font=dict(color=GOLD, size=12), x=0.5),
        xaxis=dict(color=CREAM, gridcolor="#222", dtick=2),
        yaxis=dict(color=CREAM, gridcolor="#222", tickformat=","),
        showlegend=False,
    )
    st.plotly_chart(fig_meas2, key="fig_meas2", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── What it will take cards ───────────────────────────────────────────────
    st.markdown('<p class="section-label">What Eradication Actually Requires</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card("95%", "MCV coverage needed globally to stop measles transmission", "Scientific consensus"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("83%", "current global MCV1 coverage — 12 points short of the threshold", "WHO WUENIC 2023"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("2030", "WHO Immunization Agenda target — close gaps in 20 lowest-coverage nations", "WHO IA2030"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    insight("""
    <b>What the data tells us about what comes next:</b><br><br>
    Polio eradication is within reach. Only two countries still had wild poliovirus in 2023 — Pakistan and Afghanistan.
    The challenge is geopolitical as much as logistical.<br><br>
    Measles elimination is possible region by region but faces a structural problem: measles requires 95% coverage
    and the world sits at 83%. Every outbreak — in conflict zones, in communities with vaccine hesitancy,
    in zero-dose populations — sets the clock back.<br><br>
    <b>The gap between 83% and 95% is not a vaccine science problem. It is a delivery system, equity, and trust problem.</b>
    Solving it requires sustained investment in health systems, not just in the vaccines themselves.
    """)

    # Footer
    st.markdown("""
    <div style="margin-top:3rem;padding:2rem 2.5rem;border:1px solid #2a2a2a;
                border-radius:4px;background:#1e1e1e;text-align:center;">
        <p style="font-family:'Playfair Display',serif !important;color:#C5AA6D !important;
                  font-size:1.05rem;letter-spacing:0.1em;margin-bottom:0.4rem;">
            GLOBAL VACCINATION ANALYSIS
        </p>
        <p style="font-size:0.65rem;color:#7C6657 !important;letter-spacing:0.16em;
                  text-transform:uppercase;margin-bottom:1rem;">
            Data-Driven Global Health Intelligence
        </p>
        <p style="font-size:0.82rem;color:#F7E7CE !important;margin-bottom:0.5rem;">
            Data: WHO Immunization Data Portal &bull; WUENIC Joint Coverage Estimates &bull; WHO-UNICEF &bull; 1980–2023
        </p>
        <p style="font-size:0.78rem;color:#7C6657 !important;">
            Coverage &bull; Incidence &bull; Reported Cases &bull; Vaccine Introduction &bull; Schedule Data
        </p>
    </div>
    """, unsafe_allow_html=True)