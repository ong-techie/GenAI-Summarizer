import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.services.text_splitter import split_text

UPLOAD_DIR = "uploads"
VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)

# ✅ Load local embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_local_embeddings(texts: list[str]) -> np.ndarray:
    return embedding_model.encode(
        texts,
        show_progress_bar=False,
        convert_to_numpy=True
    )


async def build_vectorstore(doc_id: str, text: str):
    print(f"[DEBUG] Building vectorstore for doc_id: {doc_id}")

    chunks = split_text(text)
    print(f"[DEBUG] Split text into {len(chunks)} chunks")

    if not chunks:
        raise ValueError("No extractable text found in document")

    embeddings = get_local_embeddings(chunks)
    print(f"[DEBUG] Generated embeddings shape: {embeddings.shape}")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))

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

    if not os.path.exists(index_path):
        raise FileNotFoundError("Vector index not found")

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)

    return {"chunks": chunks, "index": index}


async def retrieve_top_chunks(vectorstore, query: str, top_k=4):
    chunks = vectorstore["chunks"]
    index = vectorstore["index"]

    query_embedding = get_local_embeddings([query])[0]
    query_vector = np.array([query_embedding]).astype("float32")

    _, indices = index.search(query_vector, top_k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]
