import fitz  # PyMuPDF
import os
import uuid
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_and_parse(file):
    ext = file.filename.split(".")[-1]
    doc_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{doc_id}.{ext}")

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = ""
    if ext == "pdf":
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
    elif ext == "txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    return text, doc_id
