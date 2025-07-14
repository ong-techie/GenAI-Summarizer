# 📄 GenAI Summarizer

An AI-powered document assistant that lets you upload PDF/TXT files, generates summaries, answers custom questions contextually, and tests comprehension with auto-generated challenges using **Gemini Flash 2.5**, **FastAPI**, and **React**.

## 🌐 Live Deployment
[https://gen-ai-summarizer-one.vercel.app](https://gen-ai-summarizer-one.vercel.app)


## 🧠 Features
- 📤 Upload `.pdf` or `.txt` documents
- ✨ AI-generated summary on upload
- 💬 Ask Anything: contextual Q&A from the uploaded document
- 🧠 Challenge Me: AI-generated 3-question quiz with feedback
- 🌍 Fully responsive UI

## ⚙️ Tech Stack

| Layer      | Tech           |
|------------|----------------|
| Frontend   | React, Axios   |
| Backend    | FastAPI, Python |
| AI Model   | Gemini 2.5 Flash Preview |
| Vector DB  | FAISS + SentenceTransformers |
| File Parser| PyMuPDF for PDFs |
| Deployment | Render (backend), Vercel (frontend) |

## 🧱 Folder Structure
```
genai_summarizer/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       ├── ask.py              # Endpoint for Ask Anything
│   │   │       ├── challenge.py        # Endpoint for Challenge Me
│   │   │       └── upload.py           # Endpoint for document upload
│   │   ├── services/
│   │   │   ├── doc_parser.py           # Handles parsing of PDF/TXT
│   │   │   ├── qa_engine.py            # Handles summarization, QA, evaluation
│   │   │   └── vector_store.py         # Vector DB logic (FAISS)
│   │   ├── main.py                     # FastAPI app with routers
│   │   └── postman_collection.json     # (Optional) API test collection for Postman
│   ├── requirements.txt                # Backend Python dependencies
│   └── .env                            # Environment variables for backend (not committed)
│
├── frontend/
│   ├── public/
│   │   └── index.html                  # HTML entry point
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.js           # File upload UI
│   │   │   ├── AskAnything.js          # Ask Anything UI
│   │   │   └── ChallengeMe.js          # Challenge UI
│   │   ├── pages/
│   │   │   └── HomePage.js             # Main landing page
│   │   ├── shared/
│   │   │   └── DocContext.js           # Shared doc ID context
│   │   ├── App.js                      # Route configuration
│   │   ├── index.js                    # React DOM renderer
│   │   └── index.css                   # Global styles
│   ├── package.json                    # Frontend dependencies and scripts
│   └── .env                            # Vite/React environment (optional)
│
├── .gitignore                          # Exclude node_modules, venv, .env, etc.
└── README.md                           # Project overview and setup instructions


```

## 🧪 API Endpoints (Postman)
Replaced `localhost:8000` with 'https://genai-summarizer-1-bpn5.onrender.com' for testing.

| Endpoint                  | Method | Description                   |
|---------------------------|--------|-------------------------------|
| `/upload/`                | POST   | Upload PDF/TXT file           |
| `/ask/`                   | POST   | Ask question about doc        |
| `/challenge/{doc_id}`     | GET    | Get 3 AI-generated questions  |
| `/challenge/evaluate/`    | POST   | Submit answers for feedback   |

## 🔄 Example Workflow

1. **Upload** → Returns `doc_id` and a summary.
2. **Ask** → Send `question` and `doc_id` to get contextual answer.
3. **Challenge Me** → Get 3 questions → Submit answers → Receive feedback.

## 🧩 Requirements

### Backend (`requirements.txt`)
```bash
fastapi
uvicorn
python-dotenv
google-generativeai
sentence-transformers
faiss-cpu
PyMuPDF
python-multipart
```
> Also includes: uuid, shutil, os, pickle

### Frontend (React)
```bash
npm install react react-dom react-router-dom axios

```

## 🚀 Deployment Steps

### Backend on Render
1. Upload to GitHub (no `venv` or `/uploads`)
2. Create new **Web Service** on Render
3. Build command: `pip install -r backend/requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Python version: 3.10+

### Frontend on Vercel
1. Push frontend code to GitHub
2. Import on [vercel.com](https://vercel.com)
3. Set React root folder as `frontend/`

## 📬 Contact
Made by Piyush 🚀 | Powered by Gemini 2.5 Flash
