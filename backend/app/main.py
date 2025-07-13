# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import upload, ask, challenge

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(ask.router, prefix="/ask", tags=["AskAnything"])
app.include_router(challenge.router, prefix="/challenge", tags=["ChallengeMe"])

import logging
logging.basicConfig(level=logging.DEBUG)
