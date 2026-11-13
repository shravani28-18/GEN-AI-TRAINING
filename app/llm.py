import os

from dotenv import load_dotenv
from google import genai


# Load environment variables from .env
load_dotenv()


# Get Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# Generate response using Gemini
def generate_response(prompt: str) -> str:

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env file")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text or ""