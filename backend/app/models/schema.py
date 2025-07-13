from pydantic import BaseModel
from typing import List

class QARequest(BaseModel):
    question: str
    doc_id: str

class ChallengeAnswer(BaseModel):
    doc_id: str
    questions: List[str]
    answers: List[str]