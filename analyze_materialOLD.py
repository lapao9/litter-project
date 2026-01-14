#analyze_materialOLD.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_material(image_path):
    if API_KEY is None:
        return "api_key_error"

    try:
        # Abrir imagem como bytes
        with open(image_path, "rb") as img:
            image_bytes = img.read()

        # Usa o novo modelo Gemini 2.5
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = """
        You are a waste classification assistant.
        Look at the image and answer ONLY with one word:
        plastic, metal, paper, glass, organic, or other.
        """

        # Novo formato correto para imagem
        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": "image/jpeg",
                    "data": image_bytes
                }
            ]
        )

        material = response.text.strip().lower()

        allowed = ["plastic", "metal", "paper", "glass", "organic"]
        if material not in allowed:
            return "other"

        return material

    except Exception as e:
        print("Error in Gemini:", e)
        return "error"
