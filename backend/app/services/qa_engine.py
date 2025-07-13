import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from app.services.vector_store import retrieve_top_chunks

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


MODEL = genai.GenerativeModel("models/gemini-2.5-flash-lite-preview-06-17")

async def generate_summary(vectorstore, full_text):
    prompt = f"Summarize the following text in under 150 words:\n{full_text[:2000]}"
    response = MODEL.generate_content(prompt)
    return response.text


async def answer_question(vectorstore, question: str):
    chunks = await retrieve_top_chunks(vectorstore, question)
    context = "\n".join(chunks)

    prompt = f"""
You are a document question-answering assistant. Given the document below, answer the user's question in one or two sentences. Then, explain which part of the document justifies your answer in a separate line starting with "Justification:".

Document:
{context}

Question:
{question}

Answer:
"""
    response = MODEL.generate_content(prompt)
    return re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())


async def generate_challenge_questions(vectorstore):
    docs = await retrieve_top_chunks(vectorstore, "main points", top_k=6)
    context = "\n".join(docs)
    prompt = f"""
Based on the following document, generate only 3 logic-based questions.

Document:
{context}

Questions:
1.
"""
    response = MODEL.generate_content(prompt)
    return [line.strip() for line in response.text.strip().split("\n") if line.strip()]



async def evaluate_answers(vectorstore, questions, answers):
    feedbacks = []
    for question, answer in zip(questions, answers):
        if not question.strip():
            continue
        context_docs = await retrieve_top_chunks(vectorstore, question, top_k=4)
        context = "\n".join(context_docs)

        prompt = f"""
Given the document below, evaluate the answer to the question. Say if it's correct or not and explain briefly with "Justification" from the document.

Document:
{context}

Question:
{question}

Answer:
{answer}

Evaluation:
"""
        response = MODEL.generate_content(prompt)
        feedbacks.append(response.text.strip())

    return feedbacks
