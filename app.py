import streamlit as st
import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Gemini Vision Color Palette",
    layout="centered"
)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-2.5-flash"

# ---------------- HELPERS ----------------
def extract_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*", "", text)
        text = re.sub(r"```$", "", text).strip()

    return json.loads(text)

# ---------------- UI ----------------
st.title("Gemini Vision Color Palette Generator")
st.write(
    "Uses Gemini 2.5 Vision to extract the top 5 dominant colors "
    "with human-friendly names and HEX codes."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        width="stretch"
    )

    if st.button("Generate Palette"):
        with st.spinner("Gemini is analyzing the image..."):
            model = genai.GenerativeModel(MODEL_NAME)

            prompt = (
                "You are a professional color analyst.\n\n"
                "From the given image:\n"
                "- Identify the TOP 5 visually dominant colors\n"
                "- Assign each color a short, human-friendly name\n"
                "- Provide accurate HEX color codes\n\n"
                "Return ONLY valid JSON in this format:\n\n"
                "[\n"
                "  {\"name\": \"Color Name\", \"hex\": \"#RRGGBB\"},\n"
                "  {\"name\": \"Color Name\", \"hex\": \"#RRGGBB\"},\n"
                "  {\"name\": \"Color Name\", \"hex\": \"#RRGGBB\"},\n"
                "  {\"name\": \"Color Name\", \"hex\": \"#RRGGBB\"},\n"
                "  {\"name\": \"Color Name\", \"hex\": \"#RRGGBB\"}\n"
                "]\n\n"
                "No markdown. No explanations. JSON only."
            )

            response = model.generate_content(
                [prompt, image],
                generation_config={"temperature": 0}
            )

            try:
                palette = extract_json(response.text)
            except Exception as e:
                st.error("Failed to parse Gemini response")
                st.code(response.text)
                st.exception(e)
                st.stop()

        st.success("Palette generated successfully")

        cols = st.columns(5)
        for i, color in enumerate(palette):
            with cols[i]:
                st.color_picker(
                    label=f"{color['name']}\n{color['hex']}",
                    value=color["hex"],
                    disabled=True
                )
