"""
Tab 1: Food Recognition & Nutrition Audit (Epic 2)
Multimodal Vision Analysis for Dishes, Macronutrient Scoring, Micronutrient Radar & Allergen Detection
"""
import streamlit as st
import json
from PIL import Image
import io

from modules.sample_data import SAMPLE_DISH_IMAGE, SAMPLE_FOOD_RECOGNITION_RESULTS
from modules.ui_components import (
    plot_macro_donut,
    plot_micronutrient_bars,
    render_metric_card
)

def render_food_recognition_tab(ai_engine):
    st.markdown("### 🍱 Dish Recognition & Clinical Nutrition Audit")
    st.markdown(
        "Upload any meal photo or dish image. FoodVerse AI will identify the dish, cuisine, ingredients, "
        "portion size, allergens, and compute a comprehensive macronutrient & health score breakdown."
    )

    col_input, col_preset = st.columns([1.2, 0.8])

    with col_input:
        uploaded_file = st.file_uploader(
            "Upload Meal / Dish Photo",
            type=["jpg", "jpeg", "png", "webp"],
            key="dish_uploader",
            help="High-resolution top-down or angled food photo"
        )
        custom_notes = st.text_input(
            "Custom Notes / Dietary Context (Optional)",
            placeholder="e.g. Restaurant prepared, homemade low-sodium, dressing on side...",
            key="dish_notes"
        )

    with col_preset:
        st.markdown("**⚡ Or Test Instant Demo Presets:**")
        preset_choice = st.radio(
            "Select Pre-loaded Gourmet Dish:",
            ["None (Use Upload)", "Mediterranean Grilled Salmon & Quinoa Superfood Bowl"],
            index=1 if not uploaded_file else 0,
            key="dish_preset_radio"
        )

    # Determine image bytes to use
    image_bytes = None
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
    elif preset_choice != "None (Use Upload)":
        image_bytes = SAMPLE_DISH_IMAGE

    if image_bytes:
        st.image(image_bytes, caption="Active Meal Photo for Vision Intelligence", use_container_width=True)

        analyze_btn = st.button("🔍 Run Multimodal Nutrition Audit", key="btn_run_food_audit", use_container_width=True)

        if analyze_btn or "food_audit_cache" in st.session_state:
            if analyze_btn:
                with st.spinner("Analyzing culinary elements, estimating portion volume & calculating nutrient profile..."):
                    results = ai_engine.analyze_food_dish(image_bytes, custom_notes)
                    st.session_state["food_audit_cache"] = results
            else:
                results = st.session_state.get("food_audit_cache", SAMPLE_FOOD_RECOGNITION_RESULTS)

            st.markdown("---")
            render_audit_results(results)


def render_audit_results(data: dict):
    dish_name = data.get("dish_name", "Identified Dish")
    cuisine = data.get("cuisine", "International")
    portion = data.get("portion_size", "1 serving")
    health_score = int(data.get("health_score", 85))
    dietary_tags = data.get("dietary_classification", ["Nutrient Dense"])

    # Score color class
    if health_score >= 80:
        score_class = "score-high"
        score_text = "Optimal Health Profile"
    elif health_score >= 60:
        score_class = "score-medium"
        score_text = "Moderate Health Profile"
    else:
        score_class = "score-low"
        score_text = "Indulgent / Calorie Dense"

    # Header Card
    tags_html = " ".join([f"<span class='fv-hero-badge' style='margin-right:6px;'>{tag}</span>" for tag in dietary_tags])
    header_html = f"""
    <div class="fv-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
            <div>
                <span style="font-size:0.85rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em;">{cuisine} CUISINE &bull; {portion}</span>
                <h2 style="color:#FFFFFF; margin:6px 0 10px 0; font-size:1.8rem; font-weight:700;">{dish_name}</h2>
                <div>{tags_html}</div>
            </div>
            <div class="health-score-pill {score_class}">
                <span style="font-size:1.5rem; font-weight:800;">{health_score}</span>
                <div>
                    <div style="font-size:0.68rem; text-transform:uppercase; opacity:0.8;">Health Score</div>
                    <div style="font-size:0.8rem;">{score_text}</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # Macronutrient Quick Grid
    macros = data.get("macronutrients", {})
    calories = macros.get("calories", 0)
    protein = macros.get("protein_g", 0.0)
    carbs = macros.get("carbohydrates_g", 0.0)
    fats = macros.get("fats_g", 0.0)
    fiber = macros.get("fiber_g", 0.0)

    st.markdown("#### 📊 Macronutrient & Energy Breakdown")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_metric_card("Energy", f"{calories} kcal", "Total Calories", "#F8FAFC")
    with col2:
        render_metric_card("Protein", f"{protein}g", "Muscle & Satiety", "#10B981")
    with col3:
        render_metric_card("Carbs", f"{carbs}g", "Glycogen Fuel", "#3B82F6")
    with col4:
        render_metric_card("Healthy Fats", f"{fats}g", "Hormonal Balance", "#F59E0B")
    with col5:
        render_metric_card("Dietary Fiber", f"{fiber}g", "Gut Microbiome", "#A855F7")

    # Visualizations Row: Donut Chart & Micronutrients
    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        st.markdown("**Caloric Distribution (% of Total Energy)**")
        fig_donut = plot_macro_donut(protein, carbs, fats, fiber)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_chart2:
        micros = data.get("micronutrients", {})
        if micros:
            fig_micros = plot_micronutrient_bars(micros)
            if fig_micros:
                st.plotly_chart(fig_micros, use_container_width=True)
        else:
            st.info("Micronutrient detail not available for this custom image.")

    # Ingredients & Allergens in 2 columns
    col_ingr, col_safety = st.columns([1.1, 0.9])

    with col_ingr:
        st.markdown("#### 🥗 Recognized Ingredients")
        ingredients = data.get("ingredients", [])
        if ingredients:
            for item in ingredients:
                name = item.get("name", "Ingredient")
                qty = item.get("estimated_qty", "Portion")
                st.markdown(f"- **{name}** &mdash; *{qty}*")
        else:
            st.write("Itemized ingredients could not be isolated.")

    with col_safety:
        st.markdown("#### ⚠️ Allergen & Glycemic Profile")
        allergens = data.get("allergen_alerts", [])
        if allergens:
            for al in allergens:
                al_name = al.get("allergen", "Allergen")
                al_sev = al.get("severity", "Low")
                al_note = al.get("note", "")
                sev_color = "#EF4444" if al_sev == "High" else "#F59E0B" if al_sev == "Medium" else "#3B82F6"
                st.markdown(
                    f"<div style='border-left: 3px solid {sev_color}; padding:6px 12px; margin-bottom:8px; background:rgba(255,255,255,0.03); border-radius:4px;'>"
                    f"<b style='color:{sev_color};'>{al_name}</b> ({al_sev} Risk): <span style='color:#CBD5E1; font-size:0.9rem;'>{al_note}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.success("No common priority allergens flagged.")

        glycemic = data.get("glycemic_impact", "Low")
        st.markdown(f"**Glycemic Response:** `{glycemic}`")

    # Clinical Dietitian Nutritional Verdict
    verdict = data.get("nutritional_verdict", "")
    if verdict:
        st.markdown("---")
        st.markdown(
            f"""
            <div class="fv-card" style="border-left: 4px solid #10B981;">
                <h4 style="color:#34D399; margin-top:0;">🩺 Clinical Dietitian Assessment</h4>
                <p style="color:#E2E8F0; line-height:1.6; margin-bottom:0;">{verdict}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Downloadable Nutrition Report
    report_json = json.dumps(data, indent=2)
    st.download_button(
        label="📥 Download Food Intelligence JSON Report",
        data=report_json,
        file_name=f"foodverse_{dish_name.lower().replace(' ', '_')}_audit.json",
        mime="application/json"
    )
