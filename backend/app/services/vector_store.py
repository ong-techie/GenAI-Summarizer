import os
import pickle
import faiss
import numpy as np
import google.generativeai as genai

from app.services.text_splitter import split_text
from app.core.config import GOOGLE_API_KEY, GEMINI_EMBED_MODEL

# Configure Gemini once
genai.configure(api_key=GOOGLE_API_KEY)

UPLOAD_DIR = "uploads"
VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)


async def get_gemini_embeddings(texts: list[str]) -> list[list[float]]:
    results = []

    for t in texts:
        try:
            result = genai.embed_content(
                model=GEMINI_EMBED_MODEL,
                content=t,
                task_type="retrieval_document"
            )
            results.append(result["embedding"])
        except Exception as e:
            print(f"[EMBEDDING ERROR] {e}")
            results.append([0.0] * 768)  # fallback

    return results


async def build_vectorstore(doc_id: str, text: str):
    print(f"[DEBUG] Starting build_vectorstore for doc_id: {doc_id}")

    chunks = split_text(text)
    print(f"[DEBUG] Split text into {len(chunks)} chunks")

    if not chunks:
        raise ValueError(
            "No extractable text found. "
            "Scanned PDFs or empty documents are not supported."
        )

    embeddings = await get_gemini_embeddings(chunks)
    print(f"[DEBUG] Retrieved {len(embeddings)} embeddings")

    if not embeddings or not embeddings[0]:
        raise RuntimeError("Embedding generation failed")

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    index_path = os.path.join(VECTOR_DIR, f"{doc_id}.index")
    meta_path = os.path.join(VECTOR_DIR, f"{doc_id}_meta.pkl")

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(chunks, f)

    print(f"[SUCCESS] Vectorstore created for doc_id: {doc_id}")

    return {"chunks": chunks, "index": index}


async def load_vectorstore(doc_id: str):
    index_path = os.path.join(VECTOR_DIR, f"{doc_id}.index")
    meta_path = os.path.join(VECTOR_DIR, f"{doc_id}_meta.pkl")

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError(f"Vectorstore not found for doc_id: {doc_id}")

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)

    return {"chunks": chunks, "index": index}


async def retrieve_top_chunks(vectorstore, query: str, top_k=4):
    chunks = vectorstore["chunks"]
    index = vectorstore["index"]

    query_embedding = genai.embed_content(
        model=GEMINI_EMBED_MODEL,
        content=query,
        task_type="retrieval_query"
    )["embedding"]

    query_vector = np.array([query_embedding]).astype("float32")
    _, indices = index.search(query_vector, top_k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]
