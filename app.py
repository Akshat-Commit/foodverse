"""
FoodVerse AI – Multimodal Food Intelligence Agent
Platform ID: 6ac4ca021dcde6d7857c169a | Skill Wallet Capstone Project 3
Turnkey Master Implementation in Python & Streamlit
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load local environment if present
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FoodVerse AI – Multimodal Food Intelligence Agent",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import sub-modules
from modules.ui_components import inject_custom_css, render_hero_banner
from modules.ai_engine import FoodVerseAIEngine
from modules.food_recognition import render_food_recognition_tab
from modules.freshness_diagnostic import render_freshness_tab
from modules.kitchen_hygiene import render_kitchen_hygiene_tab
from modules.recipe_assistant import render_recipe_tab
from modules.meal_planner import render_meal_planner_tab

# Inject customized glassmorphism theme and CSS
inject_custom_css()

# =====================================================================
# SIDEBAR CONFIGURATION & MULTIMODAL PERSONA ENGINE
# =====================================================================
with st.sidebar:
    st.markdown("### 🥗 FoodVerse AI")
    st.caption("Multimodal Food Intelligence Ecosystem")
    st.markdown(
        "<span style='font-size:0.75rem; background:rgba(16,185,129,0.15); color:#34D399; padding:2px 8px; border-radius:10px; border:1px solid #10B98144; font-weight:700;'>"
        "CAPSTONE PROJECT 3 &bull; ID: 6ac4ca021dcde6d7857c169a"
        "</span>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown("#### ⚙️ Multimodal AI Engine")
    provider_choice = st.selectbox(
        "Inference Provider:",
        [
            "⚡ Standalone Demo Mode (Zero Key Needed)",
            "Google Gemini 1.5 / 2.0 (Multimodal Vision)",
            "Groq Cloud (LLaMA 3.2 Vision / LLaMA 3.3)"
        ],
        index=0,
        help="Standalone Demonstration Mode includes pre-calibrated food science payloads for instant evaluation."
    )

    gemini_key = ""
    groq_key = ""
    provider_key = "demo"

    if "Gemini" in provider_choice:
        provider_key = "gemini"
        env_gemini = os.getenv("GEMINI_API_KEY", "")
        gemini_key = st.text_input(
            "Gemini API Key:",
            value=env_gemini,
            type="password",
            placeholder="AIzaSy...",
            help="Get your key at aistudio.google.com"
        )
        if gemini_key:
            st.success("🟢 Gemini API Key Active")
        else:
            st.info("ℹ️ Enter key or fall back to Demo Mode.")

    elif "Groq" in provider_choice:
        provider_key = "groq"
        env_groq = os.getenv("GROQ_API_KEY", "")
        groq_key = st.text_input(
            "Groq API Key:",
            value=env_groq,
            type="password",
            placeholder="gsk_...",
            help="Get your key at console.groq.com"
        )
        if groq_key:
            st.success("🟢 Groq API Key Active")
        else:
            st.info("ℹ️ Enter key or fall back to Demo Mode.")
    else:
        provider_key = "demo"
        st.markdown(
            """
            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:10px; font-size:0.82rem; color:#A7F3D0;">
                <b>🚀 Plug & Play Ready:</b> Pre-loaded with high-fidelity culinary datasets and visual diagnostics. Zero external API keys needed!
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("#### 🧭 Core Intelligence Pillars")
    st.markdown(
        """
        - 🍱 **Epic 2:** Food Recognition & Nutrition Audit
        - 🔬 **Epic 3:** Spoilage & Freshness Diagnostic
        - 👨‍🍳 **Epic 4:** Kitchen Hygiene & Safety Compliance
        - 🍳 **Epic 4:** Smart Recipe Assistant
        - 🗓️ **Epic 5:** Biometric TDEE Meal Planner
        """
    )

    st.markdown("---")
    if st.button("🔄 Reset Diagnostic Cache", use_container_width=True):
        for k in ["food_audit_cache", "freshness_cache", "hygiene_cache", "recipe_cache", "meal_plan_cache"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown(
        """
        <div style="font-size:0.75rem; color:#64748B; text-align:center; margin-top:20px;">
            FoodVerse AI v1.0.0 &bull; Production Ready<br>
            Skill Wallet Capstone Platform 2026
        </div>
        """,
        unsafe_allow_html=True
    )

# Initialize AI Client
ai_engine = FoodVerseAIEngine(
    provider=provider_key,
    gemini_api_key=gemini_key,
    groq_api_key=groq_key
)

# =====================================================================
# MAIN CANVAS
# =====================================================================
render_hero_banner()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🍱 1. Dish & Nutrition Audit",
    "🔬 2. Freshness & Spoilage",
    "👨‍🍳 3. Kitchen Safety Compliance",
    "🍳 4. Smart Recipe Assistant",
    "🗓️ 5. Personalized Meal Planner"
])

with tab1:
    render_food_recognition_tab(ai_engine)

with tab2:
    render_freshness_tab(ai_engine)

with tab3:
    render_kitchen_hygiene_tab(ai_engine)

with tab4:
    render_recipe_tab(ai_engine)

with tab5:
    render_meal_planner_tab(ai_engine)

# =====================================================================
# FOOTER
# =====================================================================
st.markdown("---")
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; color:#64748B; font-size:0.85rem; padding:10px 0;">
        <div><b>FoodVerse AI Ecosystem</b> &bull; Capstone Project 3 (Platform ID: <code>6ac4ca021dcde6d7857c169a</code>)</div>
        <div>HACCP Compliant &bull; Mifflin-St Jeor Metabolic Engine &bull; Streamlit Community Ready</div>
    </div>
    """,
    unsafe_allow_html=True
)
