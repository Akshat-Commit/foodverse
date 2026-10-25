"""
Tab 4: Smart Kitchen Recipe Assistant (Epic 4)
Dynamic Culinary Recipe Synthesis from Pantry Ingredients with Intelligent Substitutions
"""
import streamlit as st
import json

from modules.sample_data import SAMPLE_RECIPE_PAYLOAD
from modules.ui_components import render_metric_card

def render_recipe_tab(ai_engine):
    st.markdown("### 🍳 Smart Kitchen Recipe Assistant & Pantry AI")
    st.markdown(
        "Transform whatever ingredients you have in your fridge or pantry into a gourmet, nutritious meal. "
        "FoodVerse AI crafts tailored culinary recipes with exact cooking steps, macro counts, and smart ingredient substitutions."
    )

    col_inputs, col_pantry = st.columns([1.1, 0.9])

    with col_inputs:
        pantry_text = st.text_area(
            "Enter Available Pantry / Fridge Ingredients:",
            value="Wild salmon fillets, tricolor quinoa, ripe avocado, fresh garlic, lemon, extra virgin olive oil, baby spinach",
            height=90,
            help="Comma-separated or listed ingredients you have on hand",
            key="pantry_input_text"
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            diet_pref = st.selectbox(
                "Dietary Constraint:",
                ["None / Balanced", "High Protein", "Keto / Low-Carb", "Vegan / Plant-Based", "Gluten-Free", "Diabetic-Friendly", "Mediterranean"],
                key="recipe_diet_sel"
            )
        with c2:
            cook_time = st.slider("Max Cook Time (min):", min_value=15, max_value=90, value=30, step=5, key="recipe_time_slider")
        with c3:
            skill = st.selectbox("Culinary Skill:", ["Beginner Friendly", "Intermediate", "Executive Chef"], index=1, key="recipe_skill_sel")

    with col_pantry:
        st.markdown("**💡 Quick Pantry Inspiration Presets:**")
        preset_pantry = st.radio(
            "Select Pantry Basket Preset:",
            [
                "Custom / Current Input",
                "Salmon, Quinoa, Avocado, Garlic & Lemon (Mediterranean Power)",
                "Chicken Breast, Broccoli, Garlic, Brown Rice & Soy Sauce (Lean Prep)",
                "Black Beans, Sweet Potato, Bell Peppers, Cumin & Lime (Vegan Fiesta)",
                "Eggs, Sourdough, Cherry Tomatoes, Feta Cheese & Olive Oil (Artisan Brunch)"
            ],
            key="pantry_preset_radio"
        )

        if "Salmon, Quinoa" in preset_pantry and pantry_text != "Wild salmon fillets, tricolor quinoa, ripe avocado, fresh garlic, lemon, extra virgin olive oil, baby spinach":
            pantry_text = "Wild salmon fillets, tricolor quinoa, ripe avocado, fresh garlic, lemon, extra virgin olive oil, baby spinach"
        elif "Chicken Breast" in preset_pantry:
            pantry_text = "Boneless chicken breast, fresh broccoli florets, garlic cloves, brown jasmine rice, low sodium soy sauce, ginger"
        elif "Black Beans" in preset_pantry:
            pantry_text = "Canned black beans, roasted sweet potatoes, red bell peppers, ground cumin, fresh lime, cilantro, olive oil"
        elif "Eggs, Sourdough" in preset_pantry:
            pantry_text = "Pasture-raised eggs, artisan sourdough bread, cherry tomatoes, sheep feta cheese, cold-pressed olive oil, fresh oregano"

    generate_btn = st.button("✨ Synthesize Nutritious Chef Recipe", key="btn_run_recipe", use_container_width=True)

    if generate_btn or "recipe_cache" in st.session_state:
        if generate_btn:
            with st.spinner("Analyzing flavor synergy, texture balance, cooking kinetics & nutrient ratios..."):
                results = ai_engine.generate_smart_recipe(pantry_text, diet_pref, cook_time, skill)
                st.session_state["recipe_cache"] = results
        else:
            results = st.session_state.get("recipe_cache", SAMPLE_RECIPE_PAYLOAD)

        st.markdown("---")
        render_recipe_card(results)


def render_recipe_card(data: dict):
    title = data.get("recipe_name", "Gourmet Healthy Recipe")
    prep_m = data.get("prep_time_minutes", 15)
    cook_m = data.get("cook_time_minutes", 20)
    servings = data.get("servings", 2)
    difficulty = data.get("difficulty", "Intermediate")
    cals = data.get("calories_per_serving", 480)
    macros = data.get("macronutrients", {})
    ingredients = data.get("ingredients_needed", [])
    substitutions = data.get("substitutions", [])
    steps = data.get("step_by_step_instructions", [])
    tip = data.get("chef_pro_tip", "")

    # Header Card
    st.markdown(
        f"""
        <div class="fv-card" style="border-top: 4px solid #10B981;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <span style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase;">CHEF-DESIGNED NUTRITION RECIPE &bull; {difficulty.upper()}</span>
                    <h2 style="color:#FFFFFF; margin:6px 0 10px 0; font-size:1.8rem; font-weight:700;">{title}</h2>
                    <div style="display:flex; gap:16px; color:#94A3B8; font-size:0.9rem;">
                        <span>⏱️ <b>Prep:</b> {prep_m} mins</span>
                        <span>🔥 <b>Cook:</b> {cook_m} mins</span>
                        <span>👥 <b>Servings:</b> {servings}</span>
                        <span>🎯 <b>Energy:</b> {cals} kcal/serving</span>
                    </div>
                </div>
                <div class="fv-metric-box" style="padding:10px 20px;">
                    <div style="font-size:0.75rem; color:#94A3B8;">CALORIES</div>
                    <div style="font-size:1.5rem; font-weight:800; color:#34D399;">{cals}</div>
                    <div style="font-size:0.7rem; color:#64748B;">kcal/serving</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Macros row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Protein", f"{macros.get('protein_g', 35)}g", "Per Serving", "#10B981")
    with col2:
        render_metric_card("Carbs", f"{macros.get('carbohydrates_g', 40)}g", "Per Serving", "#3B82F6")
    with col3:
        render_metric_card("Fats", f"{macros.get('fats_g', 18)}g", "Per Serving", "#F59E0B")
    with col4:
        render_metric_card("Fiber", f"{macros.get('fiber_g', 8)}g", "Per Serving", "#A855F7")

    # Ingredients & Substitutions Columns
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.markdown("#### 🛒 Ingredients Needed")
        for ing in ingredients:
            st.markdown(f"- {ing}")

        if substitutions:
            st.markdown("#### 🔄 Smart Culinary Substitutions")
            for sub in substitutions:
                orig = sub.get("original", "")
                alt = sub.get("substitute", "")
                st.markdown(
                    f"""
                    <div style="background: rgba(30, 41, 59, 0.5); border-left: 3px solid #F59E0B; padding: 6px 12px; border-radius: 6px; margin-bottom: 6px; font-size:0.88rem;">
                        <span style="color:#F59E0B; font-weight:700;">If missing {orig}:</span> <span style="color:#E2E8F0;">Use {alt}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with col_right:
        st.markdown("#### 👨‍🍳 Step-by-Step Instructions")
        for step in steps:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); padding: 12px 16px; border-radius: 10px; margin-bottom: 10px;">
                    <div style="color: #F8FAFC; font-size: 0.95rem; line-height: 1.5;">{step}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if tip:
            st.markdown(
                f"""
                <div class="fv-card" style="border-left: 4px solid #A855F7; background: rgba(168, 85, 247, 0.08); padding: 16px;">
                    <div style="color: #C084FC; font-weight: 700; font-size: 0.9rem; text-transform: uppercase;">✨ Executive Chef Secret</div>
                    <div style="color: #F1F5F9; font-size: 0.92rem; margin-top: 4px;">{tip}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Download recipe
    st.download_button(
        label="📥 Download Recipe & Nutrition Card",
        data=json.dumps(data, indent=2),
        file_name=f"foodverse_recipe_{title.lower().replace(' ', '_')}.json",
        mime="application/json"
    )
