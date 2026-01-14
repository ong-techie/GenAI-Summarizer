from fastapi import APIRouter, HTTPException
from app.models.schema import QARequest
from app.services.vector_store import load_vectorstore
from app.services.qa_engine import answer_question

router = APIRouter()


@router.post("/")
async def ask_anything(payload: QARequest):
    if not payload.question or not payload.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        vectorstore = await load_vectorstore(payload.doc_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Document not found or expired."
        )

    try:
        response = await answer_question(vectorstore, payload.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {e}"
        )

    return {"answer": response}
