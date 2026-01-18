import os
import pickle
import faiss
import numpy as np
from openai import OpenAI

from app.services.text_splitter import split_text
from app.core.config import OPENAI_API_KEY, OPENAI_EMBED_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)


async def get_openai_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        raise ValueError("Texts list cannot be empty")
    
    response = client.embeddings.create(
        model=OPENAI_EMBED_MODEL,
        input=texts
    )
    
    if not response.data or len(response.data) == 0:
        raise ValueError("No embeddings returned from OpenAI API")
    
    return [item.embedding for item in response.data]


async def build_vectorstore(doc_id: str, text: str):
    chunks = split_text(text)

    if not chunks:
        raise ValueError(
            "No extractable text found. "
            "Scanned PDFs or empty documents are not supported."
        )

    embeddings = await get_openai_embeddings(chunks)
    
    if not embeddings or len(embeddings) == 0:
        raise ValueError("Failed to generate embeddings for document chunks")
    
    if len(embeddings[0]) == 0:
        raise ValueError("Embedding dimension is zero - invalid embeddings")

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, f"{VECTOR_DIR}/{doc_id}.index")
    with open(f"{VECTOR_DIR}/{doc_id}_meta.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return {"chunks": chunks, "index": index}


async def load_vectorstore(doc_id: str):
    index_path = f"{VECTOR_DIR}/{doc_id}.index"
    meta_path = f"{VECTOR_DIR}/{doc_id}_meta.pkl"

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError(f"Vectorstore not found for doc_id: {doc_id}")

    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        chunks = pickle.load(f)

    return {"chunks": chunks, "index": index}


async def retrieve_top_chunks(vectorstore, query: str, top_k=4):
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if not vectorstore or "index" not in vectorstore or "chunks" not in vectorstore:
        raise ValueError("Invalid vectorstore provided")
    
    response = client.embeddings.create(
        model=OPENAI_EMBED_MODEL,
        input=query
    )

    if not response.data or len(response.data) == 0:
        raise ValueError("No embedding returned for query")
    
    query_vector = np.array(
        [response.data[0].embedding]
    ).astype("float32")

    if vectorstore["index"].ntotal == 0:
        return []

    _, indices = vectorstore["index"].search(query_vector, top_k)
    # Handle case where search returns fewer results than requested
    valid_indices = [i for i in indices[0] if i < len(vectorstore["chunks"])]
    return [vectorstore["chunks"][i] for i in valid_indices]
