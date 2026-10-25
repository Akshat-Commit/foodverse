# 🥗 FoodVerse AI – Multimodal Food Intelligence Agent

**Category:** Generative AI | Nutrition, Freshness & Kitchen Safety  
**Platform ID:** `6ac4ca021dcde6d7857c169a`  
**Skill Wallet Capstone Project 3**

---

## 🌟 Executive Overview & Scope
**FoodVerse AI** is a production-ready multimodal food intelligence ecosystem analyzing dish photography, perishable food surfaces, commercial kitchen environments, and biometric dietary profiles. It seamlessly integrates computer vision, multimodal reasoning, and physiological nutrition science into an ultra-modern Streamlit web application.

---

## 📌 Epics & Core Modules Coverage

| Module / Epic | Intelligence Scope & Features |
| :--- | :--- |
| **Configuration & Persona** | Secure API key input (Google Gemini 1.5/2.0 or Groq Cloud) + **Standalone Demonstration Fallback Mode** (zero-friction 1-click evaluation without API keys). |
| **Tab 1: Food Recognition & Nutrition Audit** *(Epic 2)* | Multimodal vision prompt identifying dish name, cuisine, ingredients, and portion volume. Calculates Calories, Protein, Carbs, Fats, Fiber, Allergen alerts, Glycemic impact, and a composite **Health Score (1-100)** with interactive Plotly macro donut charts and micronutrient density bars. |
| **Tab 2: Freshness & Spoilage Diagnostic** *(Epic 3)* | Vision diagnostic evaluating surface texture, discoloration, epidermal wrinkling, and fungal mold formation. Classifies items into `[Fresh | Moderately Fresh | Spoiled]` with actionable safety directives (*Safe to consume*, *Consume within 24h*, *Discard immediately*) and preservation guidelines. |
| **Tab 3: Kitchen Hygiene & Safety Compliance** *(Epic 4)* | Computer vision auditor for commercial kitchen prep lines (image/video clip support). Scans for chef hat/hairnet compliance, glove usage, sanitization state, and cross-contamination hazards (e.g. raw poultry near fresh vegetables). Computes **HACCP Compliance Score (%)** with an itemized violation log and corrective action checklist. |
| **Tab 4: Smart Kitchen Recipe Assistant** *(Epic 4)* | Dynamic pantry inventory input. Synthesizes chef-grade nutritious recipes with prep & cook times, difficulty levels, step-by-step instructions, and intelligent ingredient substitutions. |
| **Tab 5: Personalized Biometric Meal Planner** *(Epic 5)* | Mifflin-St Jeor metabolic engine computing BMR and TDEE calorie targets based on age, gender, weight, height, activity level, and fitness goals (Fat Loss, Muscle Gain). Generates an adaptive **7-Day Meal Schedule** (Breakfast, Lunch, Dinner, Snack) with an automated categorized grocery shopping list. |

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.9+
- pip

### 1. Clone & Setup Virtual Environment
```bash
cd FoodVerse
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 API Configuration (Optional)
The application is pre-calibrated with an **Offline Standalone Demo Mode** allowing reviewers and users to test all 5 tabs immediately with 1-click sample presets.

To connect live generative vision models, you can enter your keys in the sidebar or create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## ☁️ 1-Click Deployment to Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Select your repository, set branch `main`, and main file path `app.py`.
4. (Optional) Under **Advanced settings**, set `GEMINI_API_KEY` or `GROQ_API_KEY` in Secrets.
5. Click **Deploy!** Zero external database dependencies required.

---

## 📁 Project Architecture
```
FoodVerse/
├── .streamlit/
│   └── config.toml           # Sleek dark theme & server configurations
├── modules/
│   ├── __init__.py
│   ├── ai_engine.py          # Unified Gemini, Groq & Offline Demo inference engine
│   ├── food_recognition.py   # Tab 1: Vision Dish & Nutrition Breakdown (Epic 2)
│   ├── freshness_diagnostic.py # Tab 2: Spoilage & Freshness Diagnostics (Epic 3)
│   ├── kitchen_hygiene.py    # Tab 3: Commercial Kitchen HACCP Compliance (Epic 4)
│   ├── recipe_assistant.py   # Tab 4: Smart Pantry Recipe Synthesis (Epic 4)
│   ├── meal_planner.py       # Tab 5: Mifflin-St Jeor BMR/TDEE & 7-Day Plan (Epic 5)
│   ├── sample_data.py        # Curated visual presets & demo datasets
│   └── ui_components.py      # Glassmorphism CSS, Plotly charts & badges
├── app.py                    # Main Streamlit application entrypoint
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

---
*Developed for Skill Wallet Capstone Project 3 &bull; Platform ID: 6ac4ca021dcde6d7857c169a*
