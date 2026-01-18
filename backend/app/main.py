# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import upload, ask, challenge, root

app = FastAPI()

# CORS configuration - restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with specific origins in production (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(ask.router, prefix="/ask", tags=["AskAnything"])
app.include_router(challenge.router, prefix="/challenge", tags=["ChallengeMe"])
app.include_router(root.router)


import logging
logging.basicConfig(level=logging.DEBUG)
