import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is not set. "
        "Add it in Render Environment Variables."
    )

# ✅ Use ONLY supported models here
GEMINI_TEXT_MODEL = "models/gemini-1.5-flash"
GEMINI_EMBED_MODEL = "models/embedding-001"
