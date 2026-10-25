"""
UI Components and Visualizations for FoodVerse AI
Modern Glassmorphism & High-Impact Food Science Dashboard Styling
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

CUSTOM_CSS = """
<style>
/* Modern Font & Dashboard Styling */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background & Main Canvas */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.04) 0%, transparent 40%),
                #0B1120;
    color: #F1F5F9;
}

/* Main Container spacing */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3.5rem;
    max-width: 1280px;
}

/* Glassmorphism Card Component */
.fv-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.fv-card:hover {
    border-color: rgba(16, 185, 129, 0.3);
    transform: translateY(-2px);
}

/* Hero Banner */
.fv-hero-header {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(14, 165, 233, 0.12) 50%, rgba(99, 102, 241, 0.08) 100%);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 20px;
    padding: 30px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.fv-hero-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: rgba(16, 185, 129, 0.2);
    color: #34D399;
    border: 1px solid rgba(52, 211, 153, 0.35);
    margin-bottom: 12px;
}

.fv-hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 20%, #A7F3D0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 10px 0;
    line-height: 1.2;
}

.fv-hero-subtitle {
    color: #94A3B8;
    font-size: 1.05rem;
    max-width: 820px;
    line-height: 1.6;
    margin: 0;
}

/* Metric Display Cards */
.fv-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin: 16px 0;
}

.fv-metric-box {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

.fv-metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #F8FAFC;
    line-height: 1;
    margin: 6px 0;
    font-family: 'JetBrains Mono', monospace;
}

.fv-metric-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94A3B8;
    font-weight: 600;
}

/* Status Badges */
.badge-fresh {
    background: rgba(16, 185, 129, 0.18);
    color: #34D399;
    border: 1px solid rgba(52, 211, 153, 0.4);
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    display: inline-block;
}

.badge-moderate {
    background: rgba(245, 158, 11, 0.18);
    color: #FBBF24;
    border: 1px solid rgba(251, 191, 36, 0.4);
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    display: inline-block;
}

.badge-spoiled {
    background: rgba(239, 68, 68, 0.18);
    color: #F87171;
    border: 1px solid rgba(248, 113, 113, 0.4);
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    display: inline-block;
}

/* Health Score Pill */
.health-score-pill {
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 0.9rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.score-high {
    background: rgba(16, 185, 129, 0.2);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.score-medium {
    background: rgba(245, 158, 11, 0.2);
    color: #F59E0B;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.score-low {
    background: rgba(239, 68, 68, 0.2);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

/* Violation Pill */
.violation-pill-critical {
    background: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    border-left: 4px solid #EF4444;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.violation-pill-warning {
    background: rgba(245, 158, 11, 0.15);
    color: #FDE68A;
    border-left: 4px solid #F59E0B;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

.violation-pill-pass {
    background: rgba(16, 185, 129, 0.15);
    color: #A7F3D0;
    border-left: 4px solid #10B981;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    font-size: 0.9rem;
}

/* Streamlit Native Enhancements */
.stButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 700;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px -2px rgba(16, 185, 129, 0.4);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px -2px rgba(16, 185, 129, 0.6);
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 23, 42, 0.7);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 18px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 0.9rem;
}

.stTabs [aria-selected="true"] {
    background-color: #1E293B !important;
    color: #34D399 !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.6);
    border: 2px dashed rgba(52, 211, 153, 0.3);
    border-radius: 14px;
    padding: 14px;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0D1527;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}
</style>
"""

def inject_custom_css():
    """Injects high-impact custom CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero_banner():
    """Renders the top branding hero banner."""
    html = """
    <div class="fv-hero-header">
        <span class="fv-hero-badge">⚡ PLATFORM ID: 6ac4ca021dcde6d7857c169a &bull; SKILL WALLET CAPSTONE 3</span>
        <h1 class="fv-hero-title">🥗 FoodVerse AI</h1>
        <p class="fv-hero-subtitle">
            Enterprise Multimodal Food Intelligence Ecosystem &bull; Real-time Dish Recognition,
            Macronutrient Scoring, Spoilage Diagnostics, Kitchen Safety Compliance & Adaptive TDEE Meal Synthesis.
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, subtext: str = "", delta_color: str = "#10B981"):
    """Renders a single metric box."""
    html = f"""
    <div class="fv-metric-box">
        <div class="fv-metric-label">{label}</div>
        <div class="fv-metric-value" style="color: {delta_color};">{value}</div>
        <div style="font-size: 0.72rem; color: #64748B;">{subtext}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def plot_macro_donut(protein_g: float, carbs_g: float, fats_g: float, fiber_g: float = 0.0):
    """
    Renders an interactive, polished Plotly donut chart showing macronutrient calorie contribution.
    """
    # 4 kcal/g for protein and carbs, 9 kcal/g for fat
    protein_cal = protein_g * 4.0
    carbs_cal = carbs_g * 4.0
    fats_cal = fats_g * 9.0
    total_macro_cal = max(protein_cal + carbs_cal + fats_cal, 1.0)

    labels = ["Protein", "Carbohydrates", "Fats"]
    values = [protein_cal, carbs_cal, fats_cal]
    colors = ["#10B981", "#3B82F6", "#F59E0B"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.68,
                marker=dict(colors=colors, line=dict(color="#0B1120", width=3)),
                textinfo="percent+label",
                textfont=dict(size=12, color="#FFFFFF", family="Plus Jakarta Sans"),
                hoverinfo="label+value+percent",
                hovertemplate="<b>%{label}</b><br>Calories: %{value:.1f} kcal<br>Proportion: %{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color="#94A3B8", size=12)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=30, l=10, r=10),
        height=280,
        annotations=[
            dict(
                text=f"<b>{int(total_macro_cal)}</b><br><span style='font-size:11px;color:#94A3B8'>MACRO KCAL</span>",
                x=0.5,
                y=0.5,
                font=dict(size=16, color="#F8FAFC", family="Plus Jakarta Sans"),
                showarrow=False,
            )
        ],
    )
    return fig


def plot_micronutrient_bars(micros: dict):
    """
    Renders horizontal progress bars for micronutrient % RDA.
    micros format: {"Vitamin C": 45, "Iron": 20, "Calcium": 15, "Potassium": 30, ...}
    """
    if not micros:
        return None

    names = list(micros.keys())
    values = [min(float(v), 150) for v in micros.values()]
    colors = ["#34D399" if v >= 30 else "#FBBF24" if v >= 15 else "#94A3B8" for v in values]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=names,
            orientation="h",
            marker=dict(color=colors, cornerradius=6),
            text=[f"{v:.0f}% RDA" for v in values],
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=11, family="JetBrains Mono"),
        )
    )

    fig.update_layout(
        title=dict(
            text="Micronutrient Density (% Daily Recommended Value)",
            font=dict(size=13, color="#94A3B8", family="Plus Jakarta Sans"),
        ),
        xaxis=dict(
            range=[0, max(max(values) + 15, 100)],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="#64748B"),
        ),
        yaxis=dict(autorange="reversed", tickfont=dict(color="#E2E8F0")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=35, b=20, l=10, r=10),
        height=240,
    )
    return fig


def plot_hygiene_gauge(score: float):
    """
    Renders a gauge chart for Kitchen Hygiene Compliance Score (0-100%).
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Kitchen Hygiene Compliance", "font": {"size": 16, "color": "#E2E8F0"}},
            number={"suffix": "%", "font": {"size": 36, "color": "#F8FAFC"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748B"},
                "bar": {"color": "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 1,
                "bordercolor": "rgba(255,255,255,0.1)",
                "steps": [
                    {"range": [0, 60], "color": "rgba(239, 68, 68, 0.15)"},
                    {"range": [60, 80], "color": "rgba(245, 158, 11, 0.15)"},
                    {"range": [80, 100], "color": "rgba(16, 185, 129, 0.15)"},
                ],
                "threshold": {
                    "line": {"color": "#FFFFFF", "width": 3},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=20, l=20, r=20),
        height=240,
    )
    return fig


def plot_freshness_meter(freshness_score: float, stage: str):
    """
    Renders an indicator gauge meter for Food Freshness Index.
    """
    color = "#10B981" if stage.lower() == "fresh" else "#F59E0B" if "moderate" in stage.lower() else "#EF4444"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=freshness_score,
            title={"text": f"Freshness Index &bull; [{stage.upper()}]", "font": {"size": 15, "color": "#E2E8F0"}},
            number={"suffix": "/100", "font": {"size": 34, "color": color}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#64748B"},
                "bar": {"color": color},
                "bgcolor": "rgba(255,255,255,0.05)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(239, 68, 68, 0.2)"},
                    {"range": [40, 75], "color": "rgba(245, 158, 11, 0.2)"},
                    {"range": [75, 100], "color": "rgba(16, 185, 129, 0.2)"},
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=20, l=20, r=20),
        height=220,
    )
    return fig
