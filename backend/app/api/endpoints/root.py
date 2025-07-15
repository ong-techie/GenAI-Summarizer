from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "GenAI Summarizer is live"}

@router.get("/ping")
async def ping():
    return {"message": "pong"}
