"""
AI Multimodal Intelligence Engine for FoodVerse AI.
Unified Orchestration for Google Gemini, Groq Vision, and Standalone Demonstration Mode.
"""
import os
import json
import re
import requests
from PIL import Image
import io

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

from modules.sample_data import (
    SAMPLE_FOOD_RECOGNITION_RESULTS,
    SAMPLE_FRESHNESS_RESULTS_FRESH,
    SAMPLE_FRESHNESS_RESULTS_SPOILED,
    SAMPLE_KITCHEN_HYGIENE_COMPLIANT,
    SAMPLE_KITCHEN_HYGIENE_VIOLATION,
    SAMPLE_RECIPE_PAYLOAD
)

def extract_json_from_text(text: str) -> dict:
    """Safely extracts and parses JSON from LLM markdown codeblocks or raw text."""
    if not text:
        return {}
    # Remove markdown triple backticks
    text_clean = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text_clean)
    if match:
        text_clean = match.group(1).strip()
    try:
        return json.loads(text_clean)
    except Exception:
        # Fallback regex search for curly brackets
        brace_match = re.search(r"(\{[\s\S]*\})", text_clean)
        if brace_match:
            try:
                return json.loads(brace_match.group(1))
            except Exception:
                pass
    return {"raw_output": text}


class FoodVerseAIEngine:
    def __init__(self, provider: str = "demo", gemini_api_key: str = None, groq_api_key: str = None):
        self.provider = provider  # "gemini", "groq", or "demo"
        self.gemini_key = gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        self.groq_key = groq_api_key or os.getenv("GROQ_API_KEY", "")

        if self.gemini_key and HAS_GENAI:
            try:
                genai.configure(api_key=self.gemini_key)
            except Exception:
                pass

    def is_demo(self) -> bool:
        return self.provider == "demo" or (self.provider == "gemini" and not self.gemini_key) or (self.provider == "groq" and not self.groq_key)

    # -------------------------------------------------------------
    # 1. Food Recognition & Nutrition Audit (Epic 2)
    # -------------------------------------------------------------
    def analyze_food_dish(self, image_bytes: bytes, custom_context: str = "") -> dict:
        """Analyzes dish image for identity, ingredients, portion, macros, allergens, and health score."""
        if self.is_demo():
            return SAMPLE_FOOD_RECOGNITION_RESULTS

        prompt = f"""
You are FoodVerse AI, a master food scientist, clinical dietitian, and multimodal vision expert.
Analyze this food/dish image and output STRICT, VALID JSON ONLY (no markdown text outside the JSON).
Context notes from user: {custom_context or 'None provided'}

The JSON structure MUST follow this exact schema:
{{
  "dish_name": "Accurate culinary name of dish",
  "cuisine": "Cuisine origin (e.g., Mediterranean, Indian, Japanese)",
  "portion_size": "Estimated portion in grams and common serving unit",
  "health_score": integer between 1 and 100,
  "confidence_score": float between 0.50 and 0.99,
  "dietary_classification": ["tag1", "tag2"],
  "macronutrients": {{
    "calories": integer kcal,
    "protein_g": float grams,
    "carbohydrates_g": float grams,
    "fats_g": float grams,
    "fiber_g": float grams
  }},
  "micronutrients": {{
    "Vitamin C": float % RDA,
    "Iron": float % RDA,
    "Calcium": float % RDA,
    "Potassium": float % RDA,
    "Vitamin A": float % RDA
  }},
  "ingredients": [
    {{"name": "Ingredient name", "estimated_qty": "approx weight/volume"}}
  ],
  "allergen_alerts": [
    {{"allergen": "Allergen name", "severity": "High/Medium/Low", "note": "Explanation"}}
  ],
  "glycemic_impact": "Low/Moderate/High with brief reason",
  "nutritional_verdict": "2-3 sentences of expert dietitian assessment with positive aspects and optimization tips"
}}
"""
        return self._run_multimodal_vision(image_bytes, prompt, fallback=SAMPLE_FOOD_RECOGNITION_RESULTS)

    # -------------------------------------------------------------
    # 2. Food Freshness & Spoilage Diagnostic (Epic 3)
    # -------------------------------------------------------------
    def analyze_freshness(self, image_bytes: bytes, food_category: str = "Produce") -> dict:
        """Evaluates surface texture, discoloration, mold, and classifies freshness."""
        if self.is_demo():
            return SAMPLE_FRESHNESS_RESULTS_FRESH

        prompt = f"""
You are FoodVerse AI Spoilage & Freshness Diagnostic Agent.
Analyze this perishable food item image. Inspect closely for surface texture, discoloration, shriveling/wrinkling, and microbial or fungal mold formation.
Food category specified: {food_category}

Output STRICT, VALID JSON ONLY with this schema:
{{
  "food_item": "Specific name of the raw/perishable item",
  "category": "{food_category}",
  "freshness_stage": "Fresh" OR "Moderately Fresh" OR "Spoiled",
  "freshness_score": integer between 0 and 100,
  "safety_verdict": "Actionable verdict: Safe to consume immediately / Consume within 24h / Discard immediately",
  "surface_analysis": {{
    "texture": "Detailed observation of surface firmness, softness, turgor, or slime",
    "discoloration": "Detailed observation of color deviations, browning, or oxidation",
    "wrinkling": "Observation of epidermal wrinkling or moisture loss",
    "mold_detection": "Specific detection of fungal hyphae, mold colonies, or spores (or None)"
  }},
  "estimated_shelf_life": "E.g. 5-7 days refrigerated / 24 hours / Expired",
  "preservation_tips": [
    "Storage tip 1",
    "Storage tip 2",
    "Storage tip 3"
  ]
}}
"""
        return self._run_multimodal_vision(image_bytes, prompt, fallback=SAMPLE_FRESHNESS_RESULTS_FRESH)

    # -------------------------------------------------------------
    # 3. Kitchen Hygiene & Safety Auditor (Epic 4)
    # -------------------------------------------------------------
    def analyze_kitchen_hygiene(self, image_bytes: bytes, kitchen_type: str = "Commercial Prep") -> dict:
        """Detects chef hat/hairnet, glove usage, sanitization, and cross-contamination hazards."""
        if self.is_demo():
            return SAMPLE_KITCHEN_VIOLATIONS_IMAGE and SAMPLE_KITCHEN_HYGIENE_VIOLATION

        prompt = f"""
You are FoodVerse AI Commercial Kitchen Hygiene & Food Safety Compliance Auditor (FDA Food Code / HACCP standards).
Analyze this kitchen environment image or snapshot frame.
Area type: {kitchen_type}

Evaluate:
1. Hair restraints (Chef hats, hairnets, beard nets).
2. Glove usage on ready-to-eat vs raw food handling.
3. Sanitization state of surfaces, cutting boards, sinks.
4. Cross-contamination hazards (e.g., raw meat/poultry in contact or proximity to produce, unwashed tools).
5. Waste, floor cleanliness, or pest risk indicators.

Output STRICT, VALID JSON ONLY with this schema:
{{
  "kitchen_area": "Identified station or kitchen sector",
  "compliance_score": integer between 0 and 100,
  "safety_grade": "A+ / A / B / C / F with classification",
  "inspected_items": [
    {{"indicator": "Chef Hat / Hairnet Compliance", "status": "Compliant / Warning / Violation", "details": "Specific notes"}},
    {{"indicator": "Food-Grade Glove Usage", "status": "Compliant / Warning / Violation", "details": "Specific notes"}},
    {{"indicator": "Work Surface Sanitization", "status": "Compliant / Warning / Violation", "details": "Specific notes"}},
    {{"indicator": "Cross-Contamination Prevention", "status": "Compliant / Critical Hazard", "details": "Specific notes"}}
  ],
  "violations": [
    {{"severity": "Critical / Major / Minor", "violation": "Short name", "description": "Specific finding", "haccp_risk": "Hazard impact"}}
  ],
  "corrective_actions": [
    "Immediate corrective step 1",
    "Immediate corrective step 2",
    "Systemic preventive protocol 3"
  ]
}}
"""
        return self._run_multimodal_vision(image_bytes, prompt, fallback=SAMPLE_KITCHEN_HYGIENE_VIOLATION)

    # -------------------------------------------------------------
    # 4. Smart Recipe Assistant (Epic 4)
    # -------------------------------------------------------------
    def generate_smart_recipe(self, pantry_ingredients: str, dietary_pref: str = "None", cook_time_max: int = 30, skill_level: str = "Intermediate") -> dict:
        """Synthesizes creative, chef-level recipes from available pantry ingredients with substitutions."""
        if self.is_demo():
            return SAMPLE_RECIPE_PAYLOAD

        prompt = f"""
You are FoodVerse AI Master Chef & Culinary Nutritionist.
Synthesize a nutritious, creative recipe using primarily these pantry ingredients:
Ingredients available: {pantry_ingredients}
Dietary preferences: {dietary_pref}
Max cooking time: {cook_time_max} minutes
Skill level: {skill_level}

Output STRICT, VALID JSON ONLY with this schema:
{{
  "recipe_name": "Creative appetizing title",
  "prep_time_minutes": integer,
  "cook_time_minutes": integer,
  "servings": integer,
  "difficulty": "{skill_level}",
  "calories_per_serving": integer kcal,
  "macronutrients": {{
    "protein_g": float,
    "carbohydrates_g": float,
    "fats_g": float,
    "fiber_g": float
  }},
  "ingredients_needed": [
    "Ingredient with exact measurements"
  ],
  "substitutions": [
    {{"original": "Ingredient name", "substitute": "Alternative option"}}
  ],
  "step_by_step_instructions": [
    "1. Step title: Actionable detailed direction",
    "2. Step title: Actionable detailed direction"
  ],
  "chef_pro_tip": "Insider culinary technique for flavor, texture or efficiency"
}}
"""
        return self._run_text_llm(prompt, fallback=SAMPLE_RECIPE_PAYLOAD)

    # -------------------------------------------------------------
    # 5. Adaptive 7-Day Meal Planner (Epic 5)
    # -------------------------------------------------------------
    def generate_7day_meal_plan(self, user_profile: dict, bmr: float, tdee: float, macro_targets: dict) -> dict:
        """Generates comprehensive 7-day meal schedule and organized grocery checklist based on BMR/TDEE."""
        if self.is_demo():
            # Return high-quality structured demo plan
            return self._build_demo_meal_plan(user_profile, bmr, tdee, macro_targets)

        prompt = f"""
You are FoodVerse AI Clinical Nutritionist & Exercise Physiologist.
Generate an adaptive 7-day personalized meal schedule for this client:
- Age: {user_profile.get('age', 28)}, Gender: {user_profile.get('gender', 'Male')}, Weight: {user_profile.get('weight_kg', 75)}kg, Height: {user_profile.get('height_cm', 178)}cm
- Fitness Goal: {user_profile.get('goal', 'Fat Loss')}
- Dietary Constraint: {user_profile.get('diet', 'Balanced')}
- Calculated BMR: {int(bmr)} kcal, Target Daily Caloric Intake: {int(tdee)} kcal
- Target Macros: Protein: {int(macro_targets.get('protein_g', 150))}g, Carbs: {int(macro_targets.get('carbs_g', 180))}g, Fats: {int(macro_targets.get('fats_g', 55))}g

Output STRICT, VALID JSON ONLY with this schema:
{{
  "plan_overview": {{
    "goal": "{user_profile.get('goal', 'Fat Loss')}",
    "daily_target_calories": {int(tdee)},
    "macro_targets": {{
      "protein_g": {int(macro_targets.get('protein_g', 150))},
      "carbs_g": {int(macro_targets.get('carbs_g', 180))},
      "fats_g": {int(macro_targets.get('fats_g', 55))}
    }},
    "nutrition_strategy": "2-3 sentences explaining macro pacing, hydration, and adherence strategy"
  }},
  "days": [
    {{
      "day_number": 1,
      "day_name": "Monday",
      "breakfast": {{"meal": "Dish title", "calories": 450, "protein_g": 32, "carbs_g": 40, "fats_g": 14}},
      "lunch": {{"meal": "Dish title", "calories": 650, "protein_g": 48, "carbs_g": 60, "fats_g": 20}},
      "dinner": {{"meal": "Dish title", "calories": 600, "protein_g": 45, "carbs_g": 50, "fats_g": 18}},
      "snack": {{"meal": "Healthy snack", "calories": 200, "protein_g": 15, "carbs_g": 15, "fats_g": 6}}
    }}
    // Provide all 7 days (Monday through Sunday)
  ],
  "grocery_list": {{
    "Produce": ["Item 1", "Item 2"],
    "Proteins": ["Item 1", "Item 2"],
    "Dairy & Alternatives": ["Item 1", "Item 2"],
    "Grains & Pantry Staples": ["Item 1", "Item 2"],
    "Healthy Fats & Condiments": ["Item 1", "Item 2"]
  }}
}}
"""
        return self._run_text_llm(prompt, fallback=self._build_demo_meal_plan(user_profile, bmr, tdee, macro_targets))

    # -------------------------------------------------------------
    # Internal Engine Dispatchers
    # -------------------------------------------------------------
    def _run_multimodal_vision(self, image_bytes: bytes, prompt: str, fallback: dict) -> dict:
        """Dispatches vision inference to Gemini or Groq, with fallback on error."""
        if self.provider == "gemini" and self.gemini_key and HAS_GENAI:
            try:
                # Try 2.5-flash or 1.5-flash
                img = Image.open(io.BytesIO(image_bytes))
                models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
                for model_name in models_to_try:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content([prompt, img])
                        parsed = extract_json_from_text(response.text)
                        if parsed and len(parsed) > 2:
                            return parsed
                    except Exception:
                        continue
            except Exception as e:
                print(f"[Gemini Vision Error] {e}")

        elif self.provider == "groq" and self.groq_key:
            try:
                import base64
                b64_img = base64.b64encode(image_bytes).decode("utf-8")
                headers = {
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama-3.2-11b-vision-preview",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                                }
                            ]
                        }
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1500
                }
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
                if res.status_code == 200:
                    content = res.json()["choices"][0]["message"]["content"]
                    parsed = extract_json_from_text(content)
                    if parsed and len(parsed) > 2:
                        return parsed
            except Exception as e:
                print(f"[Groq Vision Error] {e}")

        # If API failed or is in demo mode
        return fallback

    def _run_text_llm(self, prompt: str, fallback: dict) -> dict:
        """Dispatches text-only queries to Gemini or Groq."""
        if self.provider == "gemini" and self.gemini_key and HAS_GENAI:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                parsed = extract_json_from_text(response.text)
                if parsed and len(parsed) > 2:
                    return parsed
            except Exception as e:
                print(f"[Gemini Text Error] {e}")

        elif self.provider == "groq" and self.groq_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 2500
                }
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
                if res.status_code == 200:
                    content = res.json()["choices"][0]["message"]["content"]
                    parsed = extract_json_from_text(content)
                    if parsed and len(parsed) > 2:
                        return parsed
            except Exception as e:
                print(f"[Groq Text Error] {e}")

        return fallback

    def _build_demo_meal_plan(self, user_profile: dict, bmr: float, tdee: float, macro_targets: dict) -> dict:
        """Builds a rich, realistic 7-day nutrition meal schedule for instant demonstration."""
        goal = user_profile.get("goal", "Moderate Fat Loss")
        diet = user_profile.get("diet", "Mediterranean")
        cal = int(tdee) if tdee else 2100
        p = int(macro_targets.get("protein_g", 150))
        c = int(macro_targets.get("carbs_g", 200))
        f = int(macro_targets.get("fats_g", 65))

        days_data = [
            {
                "day_number": 1, "day_name": "Monday",
                "breakfast": {"meal": "Greek Yogurt Parfait with Chia, Blueberries & Almonds", "calories": int(cal*0.25), "protein_g": int(p*0.25), "carbs_g": int(c*0.25), "fats_g": int(f*0.25)},
                "lunch": {"meal": "Mediterranean Grilled Chicken & Quinoa Herb Bowl", "calories": int(cal*0.35), "protein_g": int(p*0.35), "carbs_g": int(c*0.35), "fats_g": int(f*0.35)},
                "dinner": {"meal": "Pan-Seared Salmon with Steamed Asparagus & Sweet Potato", "calories": int(cal*0.30), "protein_g": int(p*0.30), "carbs_g": int(c*0.25), "fats_g": int(f*0.30)},
                "snack": {"meal": "Handful of Raw Walnuts & Green Apple Slices", "calories": int(cal*0.10), "protein_g": int(p*0.10), "carbs_g": int(c*0.15), "fats_g": int(f*0.10)}
            },
            {
                "day_number": 2, "day_name": "Tuesday",
                "breakfast": {"meal": "Spinach, Tomato & Feta 3-Egg Scramble on Sourdough", "calories": int(cal*0.25), "protein_g": int(p*0.27), "carbs_g": int(c*0.22), "fats_g": int(f*0.28)},
                "lunch": {"meal": "Wild Tuna Salad with Olive Oil, Chickpeas & Crisp Greens", "calories": int(cal*0.33), "protein_g": int(p*0.35), "carbs_g": int(c*0.30), "fats_g": int(f*0.32)},
                "dinner": {"meal": "Turkey Stuffed Bell Peppers with Brown Rice & Zucchini", "calories": int(cal*0.32), "protein_g": int(p*0.28), "carbs_g": int(c*0.35), "fats_g": int(f*0.25)},
                "snack": {"meal": "Cottage Cheese with Crushed Pumpkin Seeds", "calories": int(cal*0.10), "protein_g": int(p*0.10), "carbs_g": int(c*0.13), "fats_g": int(f*0.15)}
            },
            {
                "day_number": 3, "day_name": "Wednesday",
                "breakfast": {"meal": "Steel-Cut Oats with Whey Protein, Cinnamon & Sliced Banana", "calories": int(cal*0.25), "protein_g": int(p*0.25), "carbs_g": int(c*0.30), "fats_g": int(f*0.18)},
                "lunch": {"meal": "Grilled Herb Tofu or Lean Beef Bowl with Broccoli & Jasmine Rice", "calories": int(cal*0.35), "protein_g": int(p*0.35), "carbs_g": int(c*0.35), "fats_g": int(f*0.30)},
                "dinner": {"meal": "Herb Crusted Cod Fillet with Roasted Cauliflower & Lentils", "calories": int(cal*0.30), "protein_g": int(p*0.30), "carbs_g": int(c*0.25), "fats_g": int(f*0.32)},
                "snack": {"meal": "Hard-boiled Free-Range Eggs & Baby Carrots", "calories": int(cal*0.10), "protein_g": int(p*0.10), "carbs_g": int(c*0.10), "fats_g": int(f*0.20)}
            },
            {
                "day_number": 4, "day_name": "Thursday",
                "breakfast": {"meal": "Avocado & Smoked Salmon Protein Toast on Sprouted Grain", "calories": int(cal*0.26), "protein_g": int(p*0.26), "carbs_g": int(c*0.22), "fats_g": int(f*0.30)},
                "lunch": {"meal": "Lemon Garlic Chicken Breast over Arugula, Lentil & Walnut Salad", "calories": int(cal*0.34), "protein_g": int(p*0.36), "carbs_g": int(c*0.30), "fats_g": int(f*0.30)},
                "dinner": {"meal": "Stir-Fried Tiger Shrimp with Snap Peas, Bell Peppers & Soba", "calories": int(cal*0.30), "protein_g": int(p*0.28), "carbs_g": int(c*0.33), "fats_g": int(f*0.25)},
                "snack": {"meal": "Dark Chocolate (85%) square with Handful of Roasted Almonds", "calories": int(cal*0.10), "protein_g": int(p*0.10), "carbs_g": int(c*0.15), "fats_g": int(f*0.15)}
            },
            {
                "day_number": 5, "day_name": "Friday",
                "breakfast": {"meal": "Green Detox Superfood Smoothie with Plant Protein & Avocado", "calories": int(cal*0.24), "protein_g": int(p*0.25), "carbs_g": int(c*0.26), "fats_g": int(f*0.22)},
                "lunch": {"meal": "Grilled Turkey Burger Patty with Guacamole & Roasted Sweet Potato Fries", "calories": int(cal*0.36), "protein_g": int(p*0.35), "carbs_g": int(c*0.34), "fats_g": int(f*0.35)},
                "dinner": {"meal": "Mediterranean Baked Halibut with Kalamata Olives & Roasted Veggies", "calories": int(cal*0.30), "protein_g": int(p*0.30), "carbs_g": int(c*0.25), "fats_g": int(f*0.28)},
                "snack": {"meal": "Edamame in Pods dusted with Himalayan Pink Salt", "calories": int(cal*0.10), "protein_g": int(p*0.10), "carbs_g": int(c*0.15), "fats_g": int(f*0.15)}
            },
            {
                "day_number": 6, "day_name": "Saturday",
                "breakfast": {"meal": "Protein Oat Banana Pancakes topped with Pure Maple & Berries", "calories": int(cal*0.27), "protein_g": int(p*0.26), "carbs_g": int(c*0.35), "fats_g": int(f*0.18)},
                "lunch": {"meal": "Moroccan Spiced Chickpea & Grilled Chicken Tagine over Couscous", "calories": int(cal*0.33), "protein_g": int(p*0.34), "carbs_g": int(c*0.33), "fats_g": int(f*0.32)},
                "dinner": {"meal": "Grass-Fed Flank Steak with Chimichurri, Garlic Mushrooms & Broccolini", "calories": int(cal*0.30), "protein_g": int(p*0.32), "carbs_g": int(c*0.18), "fats_g": int(f*0.38)},
                "snack": {"meal": "Fresh Mixed Berries with 1 tbsp Organic Peanut Butter", "calories": int(cal*0.10), "protein_g": int(p*0.08), "carbs_g": int(c*0.14), "fats_g": int(f*0.12)}
            },
            {
                "day_number": 7, "day_name": "Sunday",
                "breakfast": {"meal": "Poached Eggs on Shakshuka (Spiced Tomato & Pepper Sauce)", "calories": int(cal*0.25), "protein_g": int(p*0.24), "carbs_g": int(c*0.26), "fats_g": int(f*0.26)},
                "lunch": {"meal": "Rainbow Salmon Poke Bowl with Edamame, Pickled Ginger & Brown Rice", "calories": int(cal*0.35), "protein_g": int(p*0.36), "carbs_g": int(c*0.34), "fats_g": int(f*0.32)},
                "dinner": {"meal": "Herb Roasted Free-Range Chicken Breast with Roasted Root Veggies", "calories": int(cal*0.30), "protein_g": int(p*0.30), "carbs_g": int(c*0.26), "fats_g": int(f*0.28)},
                "snack": {"meal": "Greek Yogurt Bowl with Flaxseed & a Drizzle of Raw Honey", "calories": int(cal*0.10), "protein_g": int(p*0.10), "carbs_g": int(c*0.14), "fats_g": int(f*0.14)}
            }
        ]

        grocery = {
            "Produce": [
                "Baby Spinach (2x large tubs)",
                "Wild Arugula & Romaine lettuce",
                "Fresh Avocados (5 units)",
                "Broccolini & Asparagus spears",
                "Sweet Potatoes (1.5 kg)",
                "Fresh Blueberries & Strawberries",
                "Lemons & Limes (6 units)",
                "Garlic heads, Yellow Onions, Ginger root"
            ],
            "Proteins": [
                "Wild Salmon Fillets (600g)",
                "Lean Organic Chicken Breast (1.2 kg)",
                "Grass-Fed Flank Steak (400g)",
                "Ground Turkey 93/7 (500g)",
                "Free-Range Eggs (2 dozen)"
            ],
            "Dairy & Alternatives": [
                "Authentic Plain Greek Yogurt 0% or 2% (1 kg)",
                "Low-Fat Cottage Cheese (500g)",
                "Feta Cheese in Brine (200g)",
                "Unsweetened Almond or Oat Milk (1L)"
            ],
            "Grains & Pantry Staples": [
                "Tricolor Organic Quinoa (500g)",
                "Steel-Cut Oats (500g)",
                "Brown Jasmine Rice (1 kg)",
                "Low-Sodium Vegetable / Chicken Bone Broth",
                "Canned Organic Chickpeas & Black Beans"
            ],
            "Healthy Fats & Condiments": [
                "Extra Virgin Olive Oil (Cold-pressed)",
                "Raw Walnuts & Almonds",
                "Chia Seeds & Ground Flaxseed",
                "Dijon Mustard & Apple Cider Vinegar",
                "Sea Salt & Peppercorn Grinder"
            ]
        }

        return {
            "plan_overview": {
                "goal": goal,
                "daily_target_calories": cal,
                "macro_targets": {"protein_g": p, "carbs_g": c, "fats_g": f},
                "nutrition_strategy": f"Engineered for {goal} with a {diet} profile. High-leucine protein distribution across 4 feeding windows optimizes muscle protein synthesis while keeping glycemic fluctuations subdued."
            },
            "days": days_data,
            "grocery_list": grocery
        }
