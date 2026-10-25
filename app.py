import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Recipe Idea Generator",
    page_icon="🍲",
    layout="wide",
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f4ffe9 0%, #fffdf5 55%, #fff7e8 100%);
        color: #1f2937;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp li, .stApp label, .stApp span {
        color: #1f2937;
    }
    .hero {
        text-align: center;
        padding: 1.1rem 0 1.4rem 0;
    }
    .hero h1 {
        color: #075c3b;
        font-size: clamp(2rem, 4vw, 3.2rem);
        margin-bottom: .35rem;
    }
    .hero p { color: #536579; font-size: 1.08rem; }
    .recipe-card {
        background: rgba(255,255,255,.92);
        border: 1px solid #e4eadf;
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        margin: .8rem 0;
        box-shadow: 0 8px 24px rgba(7, 92, 59, .08);
        color: #1f2937;
    }
    div.stButton > button, div.stButton > button * {
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"] {
        background: #087f50;
        border: 0;
        color: white;
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 650;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #0a9960;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🍲 AI Recipe Idea Generator</h1>
  <p>Tell us what ingredients you have, and Gemini AI will suggest something delicious.</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    left, right = st.columns([2, 1])
    with left:
        ingredients_text = st.text_area(
            "🥬 Available ingredients",
            placeholder="e.g. potato, tomato, onion, rice, cheese, milk",
            height=125,
            help="Enter ingredients separated by commas.",
        )
    with right:
        meal_type = st.selectbox(
            "🍽️ Meal type",
            ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
        )
        recipe_count = st.selectbox("✨ Number of recipe ideas", [1, 2, 3], index=0)
        dietary = st.selectbox(
            "🥗 Preference",
            ["No preference", "Vegetarian", "Vegan", "High-protein", "Gluten-free"],
        )
        cooking_level = st.selectbox(
            "👩‍🍳 Cooking level", ["Beginner", "Intermediate", "Experienced"]
        )

    generate = st.button("✨ Generate Recipe Ideas", type="primary", use_container_width=True)

if generate:
    ingredients = [item.strip() for item in ingredients_text.split(",") if item.strip()]

    if not ingredients:
        st.warning("Please enter at least one ingredient.")
        st.stop()

    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY to "
            "`.streamlit/secrets.toml` or your environment variables."
        )
        st.stop()

    prompt = f"""
You are a practical home-cooking assistant. Suggest {recipe_count} recipe idea(s)
using the ingredients the user already has.

Available ingredients: {", ".join(ingredients)}
Meal type: {meal_type}
Dietary preference: {dietary}
Cooking skill: {cooking_level}

Instructions:
- Prioritize the provided ingredients.
- Clearly separate ingredients the user already has from optional extras they may need.
- Do not pretend the user has ingredients they did not list.
- Give realistic quantities for 1-2 servings.
- Include recipe name, short description, preparation time, cooking time, servings,
  ingredients with quantities, numbered cooking steps, and one practical tip.
- Keep the instructions clear and beginner-friendly.
- If a dietary preference is selected, follow it.
- Mention common allergens when relevant.
- This is a recipe suggestion, not medical or nutritional advice.
- Format the response in clean Markdown with a heading for each recipe.
"""

    try:
        with st.spinner("Gemini is creating your recipe ideas..."):
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
            )
        if response.text:
            st.subheader("🍽️ Your recipe ideas")
            st.markdown(
                f'<div class="recipe-card">\n\n{response.text}\n\n</div>',
                unsafe_allow_html=True,
            )
            st.caption("AI-generated recipes can contain mistakes. Check ingredients and cooking temperatures before eating.")
        else:
            st.error("Gemini returned an empty response. Please try again.")
    except Exception as exc:
        st.error("Could not generate a recipe.")
        st.error(f"Actual error: {exc}")

st.divider()
st.caption("Built with Streamlit + Google Gemini API • Keep your API key private.")
