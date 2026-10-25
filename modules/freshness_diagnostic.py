"""
Tab 2: Food Freshness & Spoilage Diagnostic (Epic 3)
Computer Vision Surface Analysis, Spoilage Stage Classification & Preservation Advisory
"""
import streamlit as st
import json
from PIL import Image

from modules.sample_data import (
    SAMPLE_FRESH_BERRIES_IMAGE,
    SAMPLE_SPOILED_BERRIES_IMAGE,
    SAMPLE_FRESHNESS_RESULTS_FRESH,
    SAMPLE_FRESHNESS_RESULTS_SPOILED
)
from modules.ui_components import plot_freshness_meter, render_metric_card

def render_freshness_tab(ai_engine):
    st.markdown("### 🔬 Perishable Food Freshness & Spoilage Diagnostic")
    st.markdown(
        "Upload photos of raw or perishable food items (produce, meat, poultry, dairy). "
        "FoodVerse AI performs microscopic vision surface diagnostic to evaluate cellular turgidity, "
        "discoloration, wrinkling, mold formation, and classifies safety status."
    )

    col_upload, col_presets = st.columns([1.2, 0.8])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Raw / Perishable Food Photo",
            type=["jpg", "jpeg", "png", "webp"],
            key="freshness_uploader",
            help="Close-up macro or clear photo of the food surface"
        )
        food_cat = st.selectbox(
            "Food Classification Category:",
            ["Produce / Berries / Fruits", "Vegetables & Leafy Greens", "Raw Meat & Poultry", "Seafood & Fish", "Dairy & Cheese"],
            key="freshness_category_sel"
        )

    with col_presets:
        st.markdown("**⚡ Instant Demonstration Presets:**")
        preset_choice = st.radio(
            "Select Diagnostic Scenario:",
            [
                "None (Use Upload)",
                "Fresh Organic Strawberries (Taut, Intact Calyx)",
                "Spoiled Strawberries (Botrytis Mold & Liquefaction)"
            ],
            index=1 if not uploaded_file else 0,
            key="freshness_preset_radio"
        )

    image_bytes = None
    active_sample_data = None

    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
    elif "Fresh Organic" in preset_choice:
        image_bytes = SAMPLE_FRESH_BERRIES_IMAGE
        active_sample_data = SAMPLE_FRESHNESS_RESULTS_FRESH
    elif "Spoiled" in preset_choice:
        image_bytes = SAMPLE_SPOILED_BERRIES_IMAGE
        active_sample_data = SAMPLE_FRESHNESS_RESULTS_SPOILED

    if image_bytes:
        st.image(image_bytes, caption="Active Perishable Item for Spoilage Diagnostics", use_container_width=True)

        diagnose_btn = st.button("🧪 Run Spoilage & Freshness Diagnostic", key="btn_run_freshness", use_container_width=True)

        if diagnose_btn or "freshness_cache" in st.session_state:
            if diagnose_btn:
                with st.spinner("Analyzing surface morphology, microbial discoloration & epidermal integrity..."):
                    if ai_engine.is_demo() and active_sample_data:
                        results = active_sample_data
                    else:
                        results = ai_engine.analyze_freshness(image_bytes, food_cat)
                    st.session_state["freshness_cache"] = results
            else:
                results = st.session_state.get("freshness_cache", active_sample_data or SAMPLE_FRESHNESS_RESULTS_FRESH)

            st.markdown("---")
            render_freshness_results(results)


def render_freshness_results(data: dict):
    item_name = data.get("food_item", "Examined Specimen")
    stage = data.get("freshness_stage", "Fresh")
    score = int(data.get("freshness_score", 90))
    verdict = data.get("safety_verdict", "Safe to consume")
    shelf_life = data.get("estimated_shelf_life", "3-5 days")
    surface = data.get("surface_analysis", {})
    tips = data.get("preservation_tips", [])

    # Badge formatting
    if stage.lower() == "fresh":
        badge_html = "<span class='badge-fresh'>🟢 FRESH & OPTIMAL</span>"
        verdict_color = "#34D399"
        verdict_icon = "✅"
    elif "moderate" in stage.lower():
        badge_html = "<span class='badge-moderate'>🟡 MODERATELY FRESH (RAPID USE)</span>"
        verdict_color = "#FBBF24"
        verdict_icon = "⚠️"
    else:
        badge_html = "<span class='badge-spoiled'>🔴 SPOILED / CONTAMINATED</span>"
        verdict_color = "#F87171"
        verdict_icon = "🚨"

    # Header Card
    st.markdown(
        f"""
        <div class="fv-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <span style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase;">BIOLOGICAL ASSESSMENT SPECIMEN</span>
                    <h2 style="color:#FFFFFF; margin:4px 0 8px 0; font-size:1.8rem;">{item_name}</h2>
                    <div>{badge_html}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.8rem; color:#94A3B8;">ESTIMATED REMAINING SHELF LIFE</div>
                    <div style="font-size:1.2rem; font-weight:700; color:#38BDF8;">{shelf_life}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Meter & Verdict Row
    col_meter, col_action = st.columns([1, 1.2])

    with col_meter:
        fig_meter = plot_freshness_meter(score, stage)
        st.plotly_chart(fig_meter, use_container_width=True)

    with col_action:
        st.markdown(
            f"""
            <div class="fv-card" style="border-left: 5px solid {verdict_color}; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; font-weight:600;">Actionable Food Safety Directive</div>
                <h3 style="color: {verdict_color}; margin: 8px 0 12px 0; font-size: 1.4rem;">{verdict_icon} {verdict}</h3>
                <p style="color: #CBD5E1; font-size: 0.92rem; line-height: 1.5; margin:0;">
                    Automated HACCP biosecurity protocol triggered. Review surface diagnostic criteria below prior to culinary preparation.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Surface Analysis Grid
    st.markdown("#### 🔬 Detailed Surface Morphology Inspection")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Surface Texture", surface.get("texture", "Intact")[:22], surface.get("texture", ""), "#38BDF8")
    with c2:
        render_metric_card("Discoloration", surface.get("discoloration", "None")[:22], surface.get("discoloration", ""), "#F59E0B")
    with c3:
        render_metric_card("Epidermal Shrinkage", surface.get("wrinkling", "None")[:22], surface.get("wrinkling", ""), "#A855F7")
    with c4:
        render_metric_card("Fungal/Mold", surface.get("mold_detection", "None")[:22], surface.get("mold_detection", ""), "#EF4444" if "Botrytis" in surface.get("mold_detection","") or "mold" in surface.get("mold_detection","").lower() else "#10B981")

    # Preservation and Storage Advice
    st.markdown("#### 🛡️ Preservation & Food Waste Prevention Guidelines")
    if tips:
        for i, tip in enumerate(tips, 1):
            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.5); border-left: 3px solid #38BDF8; padding: 10px 16px; border-radius: 8px; margin-bottom: 8px;">
                    <span style="color:#38BDF8; font-weight:700; margin-right:8px;">Protocol #{i}:</span>
                    <span style="color:#E2E8F0; font-size:0.95rem;">{tip}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Download Diagnostic
    st.download_button(
        label="📥 Export Freshness & Safety Diagnostic Log",
        data=json.dumps(data, indent=2),
        file_name=f"foodverse_freshness_{item_name.lower().replace(' ', '_')}.json",
        mime="application/json"
    )
