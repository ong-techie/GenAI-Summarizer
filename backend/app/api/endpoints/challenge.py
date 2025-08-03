from fastapi import APIRouter
from fastapi import Query
from app.models.schema import ChallengeAnswer
from app.services.vector_store import load_vectorstore
from app.services.qa_engine import generate_challenge_questions, evaluate_answers

router = APIRouter()

@router.get("/{doc_id}")
async def challenge_me(doc_id: str):
    vectorstore = await load_vectorstore(doc_id)
    questions = await generate_challenge_questions(vectorstore,n=3)
    print(f"Generated {len(questions)} questions.")
    return {"questions": questions}



@router.post("/evaluate")
async def challenge_eval(payload: ChallengeAnswer):
    vectorstore = await load_vectorstore(payload.doc_id)
    feedbacks = await evaluate_answers(vectorstore, payload.questions, payload.answers)
    return {"feedbacks": feedbacks}
