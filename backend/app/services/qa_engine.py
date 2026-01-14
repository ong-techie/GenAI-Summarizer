import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from app.services.vector_store import retrieve_top_chunks

import google.generativeai as genai
from app.core.config import GOOGLE_API_KEY, GEMINI_TEXT_MODEL

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel(GEMINI_TEXT_MODEL)


async def generate_summary(vectorstore, full_text):
    prompt = f"Summarize the following text in under 150 words:\n{full_text[:2000]}"
    response = MODEL.generate_content(prompt)
    return response.text


async def answer_question(vectorstore, question: str):
    chunks = await retrieve_top_chunks(vectorstore, question)
    context = "\n".join(chunks)

    prompt = f"""
You are a document question-answering assistant. Given the document below, answer the user's question in one or two sentences. Then, explain which page, line and part of the document justifies your answer in next line starting with Justification:.

Document:
{context}

Question:
{question}

Answer:
"""
    response = MODEL.generate_content(prompt)
    return re.sub(r"\*\*(.*?)\*\*", r"\1", response.text.strip())

async def generate_challenge_questions(vectorstore, n=3):
    docs = await retrieve_top_chunks(vectorstore, "main points", top_k=6)
    context = "\n".join(docs)

    prompt = f"""
You are a highly skilled question generator.

Given the document below, generate exactly {n} logic-based comprehension questions. These should test understanding, reasoning, and interpretation — not surface-level recall.

Requirements:
- Format your response as a numbered list:
  1. First question
  2. Second question
  ...
  {n}. Final question
- Do NOT include answers, summaries, or explanations
- Each question must be relevant to the document

Document:
---
{context}
---

Now generate the {n} questions below:
Questions:
"""

    response = MODEL.generate_content(prompt)
    lines = response.text.strip().split("\n")

    # Extract and clean numbered questions like "1. ..."
    questions = [
        re.sub(r"^\d+\.\s*", "", line.strip())
        for line in lines
        if re.match(r"^\d+\.", line.strip())
    ]

    return questions[:n]



async def evaluate_answers(vectorstore, questions, answers):
    feedbacks = []
    for question, answer in zip(questions, answers):
        if not question.strip():
            continue
        context_docs = await retrieve_top_chunks(vectorstore, question, top_k=4)
        context = "\n".join(context_docs)

        prompt = f"""
Given the document below, evaluate the answer to the question. Say if it's correct or not and explain briefly with "Justification" about which page, line and part of the document explains the answer.

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
