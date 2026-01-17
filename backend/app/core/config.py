import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

# Gemini (text only)
GEMINI_TEXT_MODEL = "models/gemini-1.5-flash"

# OpenAI (embeddings)
OPENAI_EMBED_MODEL = "text-embedding-3-small"
