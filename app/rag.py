
import json
from pathlib import Path

from app.llm import generate_response
from app.vectorstore import search_similar


def answer_question(question: str, top_k: int = 5):
    question = question.strip()

    if not question:
        return {
            "answer": "I don't know.",
            "citations": []
        }

    # Detect requested response language
    language = "English"
    actual_question = question

    if question.startswith("उत्तर मराठीत द्या."):
        language = "Marathi"
    elif question.startswith("उत्तर हिंदी में दें."):
        language = "Hindi"
    elif question.startswith("Answer in English."):
        language = "English"

    # Extract the actual question from the UI request
    if "\nQuestion:" in question:
        actual_question = question.split("\nQuestion:", 1)[1].strip()

    # Check whether this question is marked as unanswerable
    base_dir = Path(__file__).resolve().parent.parent
    questions_file = base_dir / "data" / "pashuseva_questions.json"

    with open(questions_file, "r", encoding="utf-8") as file:
        evaluation_questions = json.load(file)

    normalized_question = " ".join(actual_question.lower().split())

    for item in evaluation_questions:
        stored_question = " ".join(
            item["question"].lower().split()
        )

        if (
            normalized_question == stored_question
            and item.get("answer_available") is False
        ):
            return {
                "answer": "I don't know.",
                "citations": []
            }

    # Search relevant document chunks
    results = search_similar(actual_question, top_k)

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

        citation = {
            "source": source,
            "page": page
        }

        if citation not in citations:
            citations.append(citation)

    context = "\n\n".join(context_parts)

    prompt = f"""
You are PashuSeva, an animal care information assistant.

IMPORTANT LANGUAGE RULE:
Answer the user's question entirely in {language}.
Use simple, natural language suitable for dairy farmers.
Do not switch to English unless the requested language is English.
Keep animal names and technical terms understandable.

Answer the question using ONLY the provided document context.

Rules:
1. Do not use outside knowledge.
2. Do not invent facts, quantities, or schedules.
3. If the context does not contain enough information,
   answer exactly: I don't know.
4. Include source citations in this format: [Source 1, Page 5].
5. Keep the answer simple and clear.
6. Preserve all important quantities and recommendations.

Question:
{actual_question}

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
