import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.smart_search import search_records
from app.llm import generate_response

# Project folder path
BASE_DIR = Path(__file__).resolve().parent.parent

# PashuSeva records file
DATA_FILE = BASE_DIR / "data" / "records.json"


# Create FastAPI application
app = FastAPI(
    title="PashuSeva API",
    description="Smart Animal Care Information API",
    version="1.0.0"
)


# Load records from JSON
def load_data():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Health Check API
@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "message": "PashuSeva API is running"
    }

# Get all records with limit
@app.get("/records")
def get_all_records(limit: int = 10):

    records = load_data()

    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be at least 1"
        )

    return records[:limit]


# Get one record by ID
@app.get("/records/{record_id}")
def get_record(record_id: int):

    records = load_data()

    if record_id < 1 or record_id > len(records):
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return records[record_id - 1]


# Smart Search API
@app.get("/search")
def search_api(q: str):

    results = search_records(q)

    return {
        "query": q,
        "total_results": len(results),
        "results": results
    }


# Question Request Model
class QuestionRequest(BaseModel):
    question: str


# Chat Request Model
class ChatRequest(BaseModel):
    question: str


# Chat Response Model
class ChatResponse(BaseModel):
    answer: str
    confidence: str
    follow_up: str | None = None
# Ask a Question API
@app.post("/questions")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    results = search_records(question)

    if not results:
        return {
            "question": question,
            "answer": "No matching information found.",
            "results": []
        }

    return {
        "question": question,
        "answer": results[0]["recommendation"],
        "quantity_or_schedule": results[0]["quantity_or_schedule"],
        "source": results[0]["source_doc"],
        "results": results
    }


# Chat API
@app.post("/chat", response_model=ChatResponse)
def chat_api(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Search relevant PashuSeva records
    results = search_records(question)

    # If no relevant records are found
    if not results:
        return ChatResponse(
            answer="Sorry, this information is currently not available in PashuSeva records. Please consult a qualified veterinarian for animal health concerns.",
            confidence="low",
            follow_up="Would you like to ask about animal feeding?"
        )

    # Prepare context from search results
    context = "\n\n".join([
        f"Topic: {record['topic']}\n"
        f"Animal: {record['animal_type']}\n"
        f"Recommendation: {record['recommendation']}\n"
        f"Quantity or Schedule: {record['quantity_or_schedule']}\n"
        f"Source: {record['source_doc']}"
        for record in results
    ])

    # Load system prompt
    system_prompt = (BASE_DIR / "prompts" / "system.txt").read_text(
        encoding="utf-8"
    )

    # Load task prompt
    task_prompt = (BASE_DIR / "prompts" / "task1.txt").read_text(
        encoding="utf-8"
    )

    # Prepare final prompt
    prompt = (
        system_prompt
        + "\n\n"
        + task_prompt.format(
            question=question,
            context=context
        )
    )

    # Generate answer using Gemini
    response = generate_response(prompt)

    # Parse Gemini JSON response
    try:
        data = json.loads(response)

        return ChatResponse(
            answer=data["answer"],
            confidence=data["confidence"],
            follow_up=data.get("follow_up")
        )

    except (json.JSONDecodeError, KeyError, TypeError):
        return ChatResponse(
            answer=response,
            confidence="low",
            follow_up="Would you like to ask another animal care question?"
        )
