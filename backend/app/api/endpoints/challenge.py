from fastapi import APIRouter, HTTPException
from app.models.schema import ChallengeAnswer
from app.services.vector_store import load_vectorstore
from app.services.qa_engine import generate_challenge_questions, evaluate_answers

router = APIRouter()


@router.get("/{doc_id}")
async def challenge_me(doc_id: str):
    try:
        vectorstore = await load_vectorstore(doc_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Document not found or expired."
        )

    questions = await generate_challenge_questions(vectorstore, n=3)

    if not questions:
        raise HTTPException(
            status_code=400,
            detail="Unable to generate challenge questions for this document."
        )

    return {"questions": questions}


@router.post("/evaluate")
async def challenge_eval(payload: ChallengeAnswer):
    if len(payload.questions) != len(payload.answers):
        raise HTTPException(
            status_code=400,
            detail="Number of questions and answers must match."
        )

    try:
        vectorstore = await load_vectorstore(payload.doc_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Document not found or expired."
        )

    feedbacks = await evaluate_answers(
        vectorstore,
        payload.questions,
        payload.answers
    )

    return {"feedbacks": feedbacks}
