"""
Sample Datasets and Curated Multimodal Demonstrations for FoodVerse AI.
Provides instant 1-click test scenarios across all 5 epics with realistic food science data.
"""
import io
from PIL import Image, ImageDraw, ImageFont

def create_stylized_sample_image(title: str, subtitle: str, bg_color: tuple, accent_color: tuple, icon_emoji: str) -> bytes:
    """Generates an attractive visual placeholder image with food iconography."""
    img = Image.new("RGB", (700, 480), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw gradient-like borders and visual accents
    draw.rectangle([15, 15, 685, 465], outline=accent_color, width=3)
    draw.rectangle([30, 30, 670, 450], outline=(bg_color[0]+20, bg_color[1]+20, bg_color[2]+20), width=1)

    # Draw circular backdrop for emoji/icon
    draw.ellipse([270, 70, 430, 230], fill=accent_color)
    draw.ellipse([285, 85, 415, 215], fill=bg_color)

    # Note: Default font is used for portability
    # Draw simple badge pill
    draw.rectangle([230, 255, 470, 290], fill=accent_color)

    # In PIL default font, write text
    draw.text((250, 265), "FOODVERSE AI SAMPLE", fill=(255, 255, 255))
    draw.text((160, 320), title, fill=(255, 255, 255))
    draw.text((140, 360), subtitle, fill=(180, 200, 220))
    draw.text((190, 410), "[ Click 'Run Food Intelligence Audit' to analyze ]", fill=accent_color)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


# Generate sample image bytes
SAMPLE_DISH_IMAGE = create_stylized_sample_image(
    "Mediterranean Grilled Salmon Quinoa Bowl",
    "Wild salmon fillet, tricolor quinoa, avocado, baby spinach & lemon",
    (24, 38, 56), (16, 185, 129), "🥗"
)

SAMPLE_FRESH_BERRIES_IMAGE = create_stylized_sample_image(
    "Fresh Farm-Picked Organic Strawberries",
    "Bright crimson red, firm calyx, taut surface, no fungal mycelium",
    (48, 20, 28), (239, 68, 68), "🍓"
)

SAMPLE_SPOILED_BERRIES_IMAGE = create_stylized_sample_image(
    "Spoiled Strawberries with Botrytis Mold",
    "White fuzzy mycelium growth, surface softening, dark grey lesions",
    (40, 35, 30), (245, 158, 11), "⚠️"
)

SAMPLE_KITCHEN_COMPLIANT_IMAGE = create_stylized_sample_image(
    "HACCP Certified Prep Kitchen - Station A",
    "Head chef in hairnet & beard net, nitrile gloves, sanitized stainless steel",
    (18, 38, 42), (16, 185, 129), "👨‍🍳"
)

SAMPLE_KITCHEN_VIOLATIONS_IMAGE = create_stylized_sample_image(
    "Commercial Prep Line - Hygiene Audit Alert",
    "Uncovered hair, raw poultry next to fresh salad, cross-contamination risk",
    (52, 28, 20), (239, 68, 68), "🚨"
)


# Standalone Demonstration Data Payloads (Epic 2: Food Recognition & Nutrition)
SAMPLE_FOOD_RECOGNITION_RESULTS = {
    "dish_name": "Mediterranean Grilled Salmon & Quinoa Superfood Bowl",
    "cuisine": "Mediterranean / Coastal California",
    "portion_size": "1 large serving (approx. 420g)",
    "health_score": 92,
    "confidence_score": 0.96,
    "dietary_classification": ["High Protein", "Heart Healthy", "Gluten-Free", "Rich in Omega-3"],
    "macronutrients": {
        "calories": 540,
        "protein_g": 38.5,
        "carbohydrates_g": 44.0,
        "fats_g": 22.0,
        "fiber_g": 9.5
    },
    "micronutrients": {
        "Vitamin D": 85,
        "Vitamin B12": 110,
        "Omega-3 Fatty Acids": 140,
        "Iron": 24,
        "Potassium": 28,
        "Magnesium": 35
    },
    "ingredients": [
        {"name": "Wild Atlantic Salmon (Grilled)", "estimated_qty": "150g"},
        {"name": "Steamed Tricolor Quinoa", "estimated_qty": "120g"},
        {"name": "Fresh Hass Avocado slices", "estimated_qty": "60g"},
        {"name": "Baby Spinach & Arugula", "estimated_qty": "40g"},
        {"name": "Cherry Tomatoes & Cucumber", "estimated_qty": "50g"},
        {"name": "Extra Virgin Olive Oil & Lemon Vinaigrette", "estimated_qty": "15ml"}
    ],
    "allergen_alerts": [
        {"allergen": "Fish (Salmon)", "severity": "High", "note": "Primary protein base"},
        {"allergen": "Sesame / Seeds", "severity": "Low", "note": "Garnish sesame seeds detected"}
    ],
    "glycemic_impact": "Low to Moderate (sustained slow energy release)",
    "nutritional_verdict": "Outstanding micronutrient-dense meal with optimal 1:1 protein to carb ratio, exceptionally high in anti-inflammatory EPA/DHA Omega-3s, heart-healthy monounsaturated fats, and prebiotic fiber."
}


# Standalone Demonstration Data Payloads (Epic 3: Freshness & Spoilage)
SAMPLE_FRESHNESS_RESULTS_FRESH = {
    "food_item": "Organic Fresh Strawberries (Fragaria × ananassa)",
    "category": "Berries / Perishable Produce",
    "freshness_stage": "Fresh",
    "freshness_score": 94,
    "safety_verdict": "Safe to consume immediately or store for optimal shelf life",
    "surface_analysis": {
        "texture": "Firm, taut drupelets with intact cell turgidity",
        "discoloration": "None. Uniform vibrant crimson pigmentation",
        "wrinkling": "Negligible (<2% epidermal shrinkage)",
        "mold_detection": "0% fungal spores or Botrytis cinerea mycelium"
    },
    "estimated_shelf_life": "4 to 6 days under refrigeration (34°F - 38°F / 1°C - 3°C)",
    "preservation_tips": [
        "Do NOT wash before storing; surface moisture accelerates Botrytis mold proliferation.",
        "Store in a breathable paper-towel lined container in the refrigerator crisper drawer.",
        "Maintain relative humidity around 90-95% without direct condensation.",
        "Inspect daily and isolate any bruised berry immediately to prevent ethylene contamination."
    ]
}

SAMPLE_FRESHNESS_RESULTS_SPOILED = {
    "food_item": "Decomposed Strawberries with Fungal Infiltration",
    "category": "Berries / Perishable Produce",
    "freshness_stage": "Spoiled",
    "freshness_score": 18,
    "safety_verdict": "Discard immediately. Do NOT consume.",
    "surface_analysis": {
        "texture": "Extensive cellular breakdown, soft water-soaked liquefaction",
        "discoloration": "Greyish-brown necrotic patches across 40% of surface",
        "wrinkling": "Severe epidermal collapse and shriveling",
        "mold_detection": "Active Botrytis cinerea (Grey Mold) mycelial growth with sporulation"
    },
    "estimated_shelf_life": "Expired (0 days). Unsafe for consumption.",
    "preservation_tips": [
        "Discard entire cluster to avoid airborne spore contamination to neighboring produce.",
        "Sterilize the storage container with warm soapy water and white vinegar or food-safe sanitizer.",
        "Check adjacent fruits immediately for incipient microscopic mycelium."
    ]
}


# Standalone Demonstration Data Payloads (Epic 4: Kitchen Hygiene & Safety)
SAMPLE_KITCHEN_HYGIENE_COMPLIANT = {
    "kitchen_area": "Cold Prep & Garde Manger Station",
    "compliance_score": 96,
    "safety_grade": "A+ (Exemplary HACCP Compliance)",
    "inspected_items": [
        {"indicator": "Chef Hat / Hairnet Compliance", "status": "Compliant", "details": "All active personnel wearing approved clean hair restraints."},
        {"indicator": "Food-Grade Glove Usage", "status": "Compliant", "details": "Nitrile gloves worn during ready-to-eat salad and cold plating assembly."},
        {"indicator": "Work Surface Sanitization", "status": "Compliant", "details": "Stainless steel counters sanitized with zero debris or standing grease."},
        {"indicator": "Cross-Contamination Prevention", "status": "Compliant", "details": "Color-coded cutting boards in use; raw meat isolated from fresh greens."},
        {"indicator": "Storage & Labeling", "status": "Compliant", "details": "Tightly sealed containers with FIFO date stickers visible."}
    ],
    "violations": [],
    "corrective_actions": [
        "Maintain current 2-hour glove change interval protocol.",
        "Schedule standard mid-shift Quaternary Ammonium sanitizer chemical strip test."
    ]
}

SAMPLE_KITCHEN_HYGIENE_VIOLATION = {
    "kitchen_area": "Hot Line & Butchery Prep Station",
    "compliance_score": 48,
    "safety_grade": "F (Critical Safety Intervention Required)",
    "inspected_items": [
        {"indicator": "Chef Hat / Hairnet Compliance", "status": "Violation", "details": "2 prep cooks operating without hairnets or beard coverings."},
        {"indicator": "Food-Grade Glove Usage", "status": "Violation", "details": "Bare hand contact observed handling ready-to-serve garnishes."},
        {"indicator": "Work Surface Sanitization", "status": "Warning", "details": "Liquid runoff pooling on stainless steel work table near slicing station."},
        {"indicator": "Cross-Contamination Prevention", "status": "Critical Hazard", "details": "Raw unbreaded poultry dripping adjacent to sliced raw bell peppers."},
        {"indicator": "Waste & Rubbish Management", "status": "Warning", "details": "Overfilled garbage receptacle located under prep counter."}
    ],
    "violations": [
        {"severity": "Critical", "violation": "Cross-Contamination Hazard", "description": "Raw chicken tray placed within 10cm of ready-to-eat salad prep without physical divider.", "haccp_risk": "High risk of Salmonella enterica and Campylobacter jejuni transfer."},
        {"severity": "Major", "violation": "Personal Hygiene Non-Compliance", "description": "Unrestrained hair and bare hand food contact on active service line.", "haccp_risk": "Physical and Staphylococcal bacterial contamination hazard."},
        {"severity": "Minor", "violation": "Sanitation Protocol Failure", "description": "Standing pooling fluid on prep surface.", "haccp_risk": "Bacterial harbor point."}
    ],
    "corrective_actions": [
        "IMMEDIATELY halt prep on Station 3. Condemn and discard the contaminated bell peppers.",
        "Sanitize counter with chlorine solution (100-200 ppm) or approved quat sanitizer.",
        "Enforce mandatory hairnet and fresh glove donning before kitchen re-entry.",
        "Re-brief kitchen staff on FDA Food Code Section 3-301.11 regarding bare hand contact."
    ]
}


# Standalone Demonstration Data Payloads (Epic 4: Recipe Assistant)
SAMPLE_RECIPE_PAYLOAD = {
    "recipe_name": "Pan-Seared Citrus Herb Salmon with Warm Quinoa Pilaf",
    "prep_time_minutes": 15,
    "cook_time_minutes": 18,
    "servings": 2,
    "difficulty": "Intermediate",
    "calories_per_serving": 490,
    "macronutrients": {
        "protein_g": 36,
        "carbohydrates_g": 38,
        "fats_g": 19,
        "fiber_g": 7
    },
    "ingredients_needed": [
        "2 Wild salmon fillets (approx. 150g each)",
        "3/4 cup tricolor quinoa (rinsed)",
        "1.5 cups vegetable or chicken low-sodium broth",
        "1 ripe avocado, diced",
        "2 cloves garlic, minced",
        "1 lemon (zested and juiced)",
        "2 tbsp extra virgin olive oil",
        "Fresh dill and cracked black pepper to taste"
    ],
    "substitutions": [
        {"original": "Salmon Fillet", "substitute": "Firm Tofu, Steelhead Trout, or Chicken Breast"},
        {"original": "Quinoa", "substitute": "Brown Rice, Farro, or Riced Cauliflower (for Keto)"},
        {"original": "Avocado", "substitute": "Toasted walnuts or sliced green olives"}
    ],
    "step_by_step_instructions": [
        "1. Simmer Quinoa: In a small saucepan, combine quinoa with broth and pinch of salt. Bring to boil, cover, reduce heat to low for 15 minutes until fluffy.",
        "2. Prep Salmon: Pat salmon fillets thoroughly dry with paper towel. Season both sides with lemon zest, garlic, sea salt, and freshly cracked black pepper.",
        "3. Sear to Perfection: Heat 1 tbsp olive oil in a stainless steel or cast iron skillet over medium-high until shimmering. Place salmon skin-side down for 4-5 minutes until crispy. Flip and cook 3 minutes more until medium-rare.",
        "4. Assemble & Finish: Fold diced avocado, lemon juice, and fresh dill into the warm quinoa. Top with seared salmon and a drizzle of pan juices."
    ],
    "chef_pro_tip": "Patting the salmon skin bone-dry before it touches the hot oil ensures an ultra-crisp restaurant-grade skin without sticking or tearing."
}
