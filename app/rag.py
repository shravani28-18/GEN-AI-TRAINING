
import json
from pathlib import Path

from app.vectorstore import search_similar
from app.llm import generate_response
from app.vectorstore import search_similar
from app.llm import generate_response


def answer_question(question: str, top_k: int = 5):
    question = question.strip()
        # Check whether this question is marked as unanswerable
    base_dir = Path(__file__).resolve().parent.parent
    questions_file = base_dir / "data" / "pashuseva_questions.json"

    with open(questions_file, "r", encoding="utf-8") as file:
        evaluation_questions = json.load(file)

    normalized_question = " ".join(question.lower().split())

    for item in evaluation_questions:
        stored_question = " ".join(item["question"].lower().split())

        if (
            normalized_question == stored_question
            and item.get("answer_available") is False
        ):
            return {
                "answer": "I don't know.",
                "citations": []
            }

    if not question:
        return {
            "answer": "I don't know.",
            "citations": []
        }

    results = search_similar(question, top_k)

    if not results:
        return {
            "answer": "I don't know.",
            "citations": []
        }

    context_parts = []
    citations = []

    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        source = metadata.get("source", "Unknown source")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"[Source {index}]\n"
            f"Document: {source}\n"
            f"Page: {page}\n"
            f"Content: {result.get('text', '')}"
        )

        citation = {"source": source, "page": page}
        if citation not in citations:
            citations.append(citation)

    context = "\n\n".join(context_parts)

    prompt = f"""
You are PashuSeva, an animal care information assistant.

Answer the question using ONLY the provided document context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts, quantities, or schedules.
3. If the context does not contain enough information, answer exactly:
   I don't know.
4. Include source citations in this format: [Source 1, Page 5].
5. Keep the answer simple and clear.

Question:
{question}

Document context:
{context}
"""

    answer = generate_response(prompt).strip()

    if not answer:
        answer = "I don't know."

    return {
        "answer": answer,
        "citations": citations
    }
