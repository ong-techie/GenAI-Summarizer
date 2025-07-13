from fastapi import APIRouter, UploadFile, File
from app.services.doc_parser import save_and_parse
from app.services.vector_store import build_vectorstore
from app.services.qa_engine import generate_summary

router = APIRouter()

@router.post("/")
async def upload_doc(file: UploadFile = File(...)):
    text, doc_id = await save_and_parse(file)
    vectorstore = await build_vectorstore(doc_id, text)
    summary = await generate_summary(vectorstore, text)
    return {"doc_id": doc_id, "summary": summary}
