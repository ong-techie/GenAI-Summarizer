import os
import pickle
import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.text_splitter import split_text

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

UPLOAD_DIR = "uploads"
VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)


async def get_gemini_embeddings(texts: list[str]) -> list[list[float]]:
    model = "models/embedding-001"
    results = []
    for t in texts:
        try:
            result = genai.embed_content(
                model=model,
                content=t,
                task_type="retrieval_document"
            )
            results.append(result["embedding"])
        except Exception as e:
            print(f"Embedding error on chunk: {e}")
            results.append([0.0] * 768)  # fallback vector
    return results



async def build_vectorstore(doc_id: str, text: str):
    print(f"[DEBUG] Starting build_vectorstore for doc_id: {doc_id}")

    chunks = split_text(text)
    print(f"[DEBUG] Split text into {len(chunks)} chunks")

    if not chunks:
        print("[ERROR] No chunks generated — check split_text() or empty document.")
        return

    embeddings = await get_gemini_embeddings(chunks)
    print(f"[DEBUG] Retrieved {len(embeddings)} embeddings")

    if not embeddings or len(embeddings[0]) == 0:
        print("[ERROR] Embedding generation failed or returned empty vectors")
        return

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    # Write FAISS index
    index_path = os.path.join(VECTOR_DIR, f"{doc_id}.index")
    meta_path = os.path.join(VECTOR_DIR, f"{doc_id}_meta.pkl")

    print(f"[DEBUG] Writing FAISS index to {index_path}")
    faiss.write_index(index, index_path)

    print(f"[DEBUG] Writing metadata to {meta_path}")
    with open(meta_path, "wb") as f:
        pickle.dump(chunks, f)

    print(f"[SUCCESS] Vectorstore created for doc_id: {doc_id}")
    return { "chunks": chunks, "index": index }



async def load_vectorstore(doc_id: str):
    index = faiss.read_index(os.path.join(VECTOR_DIR, f"{doc_id}.index"))
    with open(os.path.join(VECTOR_DIR, f"{doc_id}_meta.pkl"), "rb") as f:
        chunks = pickle.load(f)
    return { "chunks": chunks, "index": index }


async def retrieve_top_chunks(vectorstore, query: str, top_k=4):
    chunks = vectorstore["chunks"]
    index = vectorstore["index"]

    query_embedding = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query"
    )["embedding"]

    query_vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_vector, top_k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]
