from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.doc_parser import save_and_parse
from app.services.vector_store import build_vectorstore
from app.services.qa_engine import generate_summary

router = APIRouter()


@router.post("/")
async def upload_doc(file: UploadFile = File(...)):
    # 1️⃣ Parse document
    text, doc_id = await save_and_parse(file)

    if not text or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No extractable text found. Scanned PDFs are not supported."
        )

    # 2️⃣ Build vectorstore
    try:
        vectorstore = await build_vectorstore(doc_id, text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build vector store: {e}"
        )

    # 3️⃣ Generate summary
    try:
        summary = await generate_summary(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {e}"
        )

    return {
        "doc_id": doc_id,
        "summary": summary
    }
