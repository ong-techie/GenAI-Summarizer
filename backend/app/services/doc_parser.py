import fitz  # PyMuPDF
import os
import uuid
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_and_parse(file):
    if not file.filename:
        raise ValueError("File must have a filename")
    
    if "." not in file.filename:
        raise ValueError("File must have an extension")
    
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "txt"]:
        raise ValueError(f"Unsupported file type: {ext}. Only PDF and TXT files are supported.")
    
    doc_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{doc_id}.{ext}")

    try:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        text = ""
        if ext == "pdf":
            doc = None
            try:
                doc = fitz.open(path)
                for page in doc:
                    text += page.get_text()
            finally:
                if doc:
                    doc.close()
        elif ext == "txt":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                # Try with different encoding if UTF-8 fails
                with open(path, "r", encoding="latin-1") as f:
                    text = f.read()

        return text, doc_id
    except Exception as e:
        # Clean up file if parsing fails
        if os.path.exists(path):
            os.remove(path)
        raise
