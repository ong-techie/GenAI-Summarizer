import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

GEMINI_TEXT_MODEL = "gemini-2.5-flash-lite"
