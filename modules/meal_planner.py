"""
Tab 5: Personalized Meal Planner (Epic 5)
Metabolic BMR/TDEE Biometric Computation, Adaptive 7-Day Meal Schedule & Automated Categorized Grocery List
"""
import streamlit as st
import json
import pandas as pd

from modules.ui_components import render_metric_card

def calculate_metabolic_targets(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str, goal: str):
    """
    Computes Mifflin-St Jeor BMR and adjusted TDEE with macro distribution.
    """
    # Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + 5.0
    else:
        bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) - 161.0

    # Activity multiplier
    activity_multipliers = {
        "Sedentary (desk job, little/no exercise)": 1.2,
        "Lightly Active (exercise 1-3 days/week)": 1.375,
        "Moderately Active (exercise 3-5 days/week)": 1.55,
        "Very Active (hard exercise 6-7 days/week)": 1.725,
        "Extremely Active (physical job or 2x training)": 1.9,
    }
    mult = activity_multipliers.get(activity_level, 1.4)
    tdee_maintenance = bmr * mult

    # Goal adjustments
    goal_deltas = {
        "Aggressive Fat Loss (-500 kcal)": -500,
        "Moderate Fat Loss (-300 kcal)": -300,
        "Maintenance (Zero Deficit/Surplus)": 0,
        "Lean Muscle Gain (+250 kcal)": 250,
        "Athletic Bulking (+450 kcal)": 450,
    }
    target_cals = max(tdee_maintenance + goal_deltas.get(goal, 0), 1200)

    # Macronutrient assignment based on fitness goal
    # Protein: 2.0g per kg for muscle gain/fat loss preservation, min 1.6g/kg
    if "Muscle" in goal or "Bulking" in goal:
        protein_g = weight_kg * 2.2
    elif "Loss" in goal:
        protein_g = weight_kg * 2.0
    else:
        protein_g = weight_kg * 1.8

    protein_cals = protein_g * 4.0

    # Fats: 25% of total calories
    fats_cals = target_cals * 0.25
    fats_g = fats_cals / 9.0

    # Carbs: remainder
    carbs_cals = max(target_cals - (protein_cals + fats_cals), 200)
    carbs_g = carbs_cals / 4.0

    return {
        "bmr": round(bmr, 1),
        "maintenance_tdee": round(tdee_maintenance, 1),
        "target_calories": round(target_cals, 0),
        "protein_g": round(protein_g, 1),
        "carbs_g": round(carbs_g, 1),
        "fats_g": round(fats_g, 1)
    }


def render_meal_planner_tab(ai_engine):
    st.markdown("### 🗓️ Personalized Biometric Meal Planner (BMR / TDEE Engine)")
    st.markdown(
        "Scientific metabolic calculation based on the validated **Mifflin-St Jeor formula**. "
        "Generates a complete adaptive **7-Day Meal Schedule** with automated **Categorized Grocery Shopping List**."
    )

    with st.form("biometric_profile_form"):
        st.markdown("#### 1. Biometric & Physiological Profile")
        col_bio1, col_bio2, col_bio3, col_bio4 = st.columns(4)
        with col_bio1:
            age = st.number_input("Age (Years):", min_value=15, max_value=100, value=28, step=1)
        with col_bio2:
            gender = st.selectbox("Biological Sex:", ["Male", "Female"])
        with col_bio3:
            weight = st.number_input("Weight (kg):", min_value=35.0, max_value=250.0, value=74.0, step=0.5)
        with col_bio4:
            height = st.number_input("Height (cm):", min_value=120.0, max_value=230.0, value=178.0, step=1.0)

        col_pref1, col_pref2, col_pref3 = st.columns(3)
        with col_pref1:
            activity = st.selectbox(
                "Daily Activity Multiplier:",
                [
                    "Sedentary (desk job, little/no exercise)",
                    "Lightly Active (exercise 1-3 days/week)",
                    "Moderately Active (exercise 3-5 days/week)",
                    "Very Active (hard exercise 6-7 days/week)",
                    "Extremely Active (physical job or 2x training)"
                ],
                index=2
            )
        with col_pref2:
            fitness_goal = st.selectbox(
                "Fitness / Body Composition Goal:",
                [
                    "Moderate Fat Loss (-300 kcal)",
                    "Aggressive Fat Loss (-500 kcal)",
                    "Maintenance (Zero Deficit/Surplus)",
                    "Lean Muscle Gain (+250 kcal)",
                    "Athletic Bulking (+450 kcal)"
                ],
                index=0
            )
        with col_pref3:
            diet_type = st.selectbox(
                "Dietary Framework:",
                [
                    "Mediterranean (Heart Healthy)",
                    "High-Protein Balanced",
                    "Vegan / 100% Plant-Based",
                    "Keto / Low-Carb High-Fat",
                    "Diabetic-Friendly (Low GI)",
                    "Gluten-Free Celiac Safe",
                    "Halal Certified"
                ],
                index=0
            )

        submit_plan = st.form_submit_button("⚡ Compute Metabolic Targets & Generate 7-Day Schedule", use_container_width=True)

    # Calculate metrics
    calc = calculate_metabolic_targets(weight, height, age, gender, activity, fitness_goal)

    # Render Metabolic Summary Cards
    st.markdown("#### ⚡ Computed Metabolic & Daily Energy Targets")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        render_metric_card("BMR", f"{int(calc['bmr'])}", "Basal Metabolic Rate", "#94A3B8")
    with m2:
        render_metric_card("TDEE", f"{int(calc['maintenance_tdee'])}", "Maintenance kcal", "#38BDF8")
    with m3:
        render_metric_card("Target Cal", f"{int(calc['target_calories'])}", "Prescribed Intake", "#10B981")
    with m4:
        render_metric_card("Protein", f"{int(calc['protein_g'])}g", "4 kcal/g", "#34D399")
    with m5:
        render_metric_card("Carbs", f"{int(calc['carbs_g'])}g", "4 kcal/g", "#60A5FA")
    with m6:
        render_metric_card("Fats", f"{int(calc['fats_g'])}g", "9 kcal/g", "#FBBF24")

    # If submitted or cache present
    if submit_plan or "meal_plan_cache" in st.session_state:
        user_profile = {
            "age": age,
            "gender": gender,
            "weight_kg": weight,
            "height_cm": height,
            "activity": activity,
            "goal": fitness_goal,
            "diet": diet_type
        }

        if submit_plan:
            with st.spinner("Synthesizing 7-day adaptive nutrition protocol and consolidating grocery supply chain..."):
                plan_data = ai_engine.generate_meal_plan(
                    user_profile,
                    calc["bmr"],
                    calc["target_calories"],
                    {"protein_g": calc["protein_g"], "carbs_g": calc["carbs_g"], "fats_g": calc["fats_g"]}
                )
                st.session_state["meal_plan_cache"] = plan_data
        else:
            plan_data = st.session_state.get("meal_plan_cache")

        st.markdown("---")
        render_meal_plan_view(plan_data)


def render_meal_plan_view(data: dict):
    overview = data.get("plan_overview", {})
    days = data.get("days", [])
    grocery = data.get("grocery_list", {})

    strategy = overview.get("nutrition_strategy", "")
    if strategy:
        st.markdown(
            f"""
            <div class="fv-card" style="border-left: 4px solid #38BDF8;">
                <h4 style="color:#38BDF8; margin-top:0;">📋 Adaptive Strategic Nutrition Protocol</h4>
                <p style="color:#E2E8F0; font-size:0.95rem; line-height:1.6; margin-bottom:0;">{strategy}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("#### 📅 7-Day Precision Meal Schedule")

    day_tabs = st.tabs([f"Day {d.get('day_number', i+1)}: {d.get('day_name', 'Day')}" for i, d in enumerate(days)])

    for i, tab in enumerate(day_tabs):
        with tab:
            if i < len(days):
                day = days[i]
                d_c1, d_c2, d_c3, d_c4 = st.columns(4)

                b = day.get("breakfast", {})
                l = day.get("lunch", {})
                d = day.get("dinner", {})
                s = day.get("snack", {})

                with d_c1:
                    st.markdown(
                        f"""
                        <div class="fv-card" style="height:100%; border-top: 3px solid #10B981;">
                            <div style="font-size:0.75rem; color:#10B981; font-weight:700;">🌅 BREAKFAST</div>
                            <div style="color:#FFFFFF; font-weight:700; margin:6px 0; font-size:1.05rem;">{b.get('meal', 'Oatmeal & Berries')}</div>
                            <div style="color:#94A3B8; font-size:0.85rem;">🔥 <b>{b.get('calories', 400)} kcal</b></div>
                            <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">P: {b.get('protein_g', 30)}g &bull; C: {b.get('carbs_g', 40)}g &bull; F: {b.get('fats_g', 12)}g</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with d_c2:
                    st.markdown(
                        f"""
                        <div class="fv-card" style="height:100%; border-top: 3px solid #3B82F6;">
                            <div style="font-size:0.75rem; color:#3B82F6; font-weight:700;">☀️ LUNCH</div>
                            <div style="color:#FFFFFF; font-weight:700; margin:6px 0; font-size:1.05rem;">{l.get('meal', 'Chicken Salad')}</div>
                            <div style="color:#94A3B8; font-size:0.85rem;">🔥 <b>{l.get('calories', 600)} kcal</b></div>
                            <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">P: {l.get('protein_g', 45)}g &bull; C: {l.get('carbs_g', 55)}g &bull; F: {l.get('fats_g', 18)}g</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with d_c3:
                    st.markdown(
                        f"""
                        <div class="fv-card" style="height:100%; border-top: 3px solid #F59E0B;">
                            <div style="font-size:0.75rem; color:#F59E0B; font-weight:700;">🌙 DINNER</div>
                            <div style="color:#FFFFFF; font-weight:700; margin:6px 0; font-size:1.05rem;">{d.get('meal', 'Salmon & Veggies')}</div>
                            <div style="color:#94A3B8; font-size:0.85rem;">🔥 <b>{d.get('calories', 550)} kcal</b></div>
                            <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">P: {d.get('protein_g', 40)}g &bull; C: {d.get('carbs_g', 45)}g &bull; F: {d.get('fats_g', 16)}g</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with d_c4:
                    st.markdown(
                        f"""
                        <div class="fv-card" style="height:100%; border-top: 3px solid #A855F7;">
                            <div style="font-size:0.75rem; color:#A855F7; font-weight:700;">🍎 SNACK / POST-WORKOUT</div>
                            <div style="color:#FFFFFF; font-weight:700; margin:6px 0; font-size:1.05rem;">{s.get('meal', 'Greek Yogurt & Nuts')}</div>
                            <div style="color:#94A3B8; font-size:0.85rem;">🔥 <b>{s.get('calories', 200)} kcal</b></div>
                            <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">P: {s.get('protein_g', 15)}g &bull; C: {s.get('carbs_g', 15)}g &bull; F: {s.get('fats_g', 6)}g</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # Automated Grocery Shopping List
    st.markdown("---")
    st.markdown("#### 🛒 Automated Categorized Grocery Supply List")
    st.markdown("Consolidated pantry & produce checklist for all 7 days of culinary execution:")

    col_g1, col_g2, col_g3 = st.columns(3)

    produce = grocery.get("Produce", [])
    proteins = grocery.get("Proteins", [])
    dairy = grocery.get("Dairy & Alternatives", [])
    grains = grocery.get("Grains & Pantry Staples", [])
    fats = grocery.get("Healthy Fats & Condiments", [])

    with col_g1:
        st.markdown("**🥦 Fresh Produce**")
        for item in produce:
            st.checkbox(item, key=f"g_prod_{item}")

    with col_g2:
        st.markdown("**🥩 Proteins & Fish**")
        for item in proteins:
            st.checkbox(item, key=f"g_prot_{item}")

        st.markdown("**🥛 Dairy & Alternatives**")
        for item in dairy:
            st.checkbox(item, key=f"g_dairy_{item}")

    with col_g3:
        st.markdown("**🌾 Grains & Pantry Staples**")
        for item in grains:
            st.checkbox(item, key=f"g_grain_{item}")

        st.markdown("**🫒 Healthy Fats & Spices**")
        for item in fats:
            st.checkbox(item, key=f"g_fats_{item}")

    # Generate Markdown export of plan + grocery list
    md_content = f"# FoodVerse AI 7-Day Meal Plan\n\n"
    md_content += f"**Goal:** {overview.get('goal')} | **Daily Calories:** {overview.get('daily_target_calories')} kcal\n\n"
    md_content += f"## 7-Day Schedule\n"
    for day in days:
        md_content += f"### {day.get('day_name')}\n"
        md_content += f"- **Breakfast:** {day.get('breakfast',{}).get('meal')} ({day.get('breakfast',{}).get('calories')} kcal)\n"
        md_content += f"- **Lunch:** {day.get('lunch',{}).get('meal')} ({day.get('lunch',{}).get('calories')} kcal)\n"
        md_content += f"- **Dinner:** {day.get('dinner',{}).get('meal')} ({day.get('dinner',{}).get('calories')} kcal)\n"
        md_content += f"- **Snack:** {day.get('snack',{}).get('meal')} ({day.get('snack',{}).get('calories')} kcal)\n\n"

    md_content += f"## Grocery Checklist\n"
    for cat, items in grocery.items():
        md_content += f"### {cat}\n"
        for it in items:
            md_content += f"- [ ] {it}\n"

    st.download_button(
        label="📥 Download 7-Day Meal Schedule & Grocery Checklist (.md)",
        data=md_content,
        file_name="foodverse_7day_meal_plan.md",
        mime="text/markdown"
    )
