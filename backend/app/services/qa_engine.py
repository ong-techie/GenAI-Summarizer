import re
import google.generativeai as genai

from app.services.vector_store import retrieve_top_chunks
from app.core.config import GEMINI_API_KEY, GEMINI_TEXT_MODEL

# Configure Gemini once
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel(GEMINI_TEXT_MODEL)


async def generate_summary(vectorstore, full_text: str):
    if not full_text or not full_text.strip():
        return "No extractable text found in the document."

    prompt = (
        "Summarize the following text in under 150 words:\n\n"
        f"{full_text[:2000]}"
    )

    try:
        response = MODEL.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Summary generation failed: {e}"


async def answer_question(vectorstore, question: str):
    chunks = await retrieve_top_chunks(vectorstore, question)

    if not chunks:
        return (
            "Answer: Unable to find relevant information.\n"
            "Justification: The document does not contain relevant context."
        )

    context = "\n".join(chunks)

    prompt = f"""
You are a document question-answering assistant.

Answer the question in one or two sentences.
Then add a second line starting with "Justification:" explaining
which part of the document supports the answer.

Document:
{context}

Question:
{question}

Answer:
"""

    try:
        response = MODEL.generate_content(prompt)
        return re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())
    except Exception as e:
        return f"Answer generation failed: {e}"


async def generate_challenge_questions(vectorstore, n: int = 3):
    docs = await retrieve_top_chunks(vectorstore, "main points", top_k=6)

    if not docs:
        return []

    context = "\n".join(docs)

    prompt = f"""
You are a highly skilled question generator.

Generate exactly {n} logic-based comprehension questions
that test reasoning and understanding.

Rules:
- Numbered list only
- No answers or explanations

Document:
---
{context}
---

Questions:
"""

    try:
        response = MODEL.generate_content(prompt)
        lines = response.text.strip().split("\n")

        questions = [
            re.sub(r"^\d+\.\s*", "", line.strip())
            for line in lines
            if re.match(r"^\d+\.", line.strip())
        ]

        return questions[:n]

    except Exception as e:
        print(f"[QUESTION GEN ERROR] {e}")
        return []


async def evaluate_answers(vectorstore, questions, answers):
    feedbacks = []

    for question, answer in zip(questions, answers):
        if not question.strip():
            continue

        context_docs = await retrieve_top_chunks(vectorstore, question, top_k=4)
        if not context_docs:
            feedbacks.append("Unable to evaluate: no relevant context found.")
            continue

        context = "\n".join(context_docs)

        prompt = f"""
Evaluate the answer to the question using the document.

State whether it is correct or incorrect and explain briefly.
Include a line starting with "Justification:".

Document:
{context}

Question:
{question}

Answer:
{answer}

Evaluation:
"""

        try:
            response = MODEL.generate_content(prompt)
            feedbacks.append(response.text.strip())
        except Exception as e:
            feedbacks.append(f"Evaluation failed: {e}")

    return feedbacks
