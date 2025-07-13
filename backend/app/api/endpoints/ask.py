from fastapi import APIRouter
from app.models.schema import QARequest
from app.services.vector_store import load_vectorstore
from app.services.qa_engine import answer_question

router = APIRouter()

@router.post("/")
async def ask_anything(payload: QARequest):
    vectorstore = await load_vectorstore(payload.doc_id)
    response = await answer_question(vectorstore, payload.question)
    return {"answer": response}
