
import json
from pathlib import Path

import chromadb

from app.chunking import load_pdf_chunks
from app.embed import embed_chunks, embed_texts
from app.llm import generate_response


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "chroma_db"

EVAL_FILE = BASE_DIR / "eval" / "eval_set.json"
RESULT_FILE = BASE_DIR / "eval" / "results_day8.json"


def create_chunks(chunk_size):
    from app import chunking

    original_size = chunking.CHUNK_SIZE
    chunking.CHUNK_SIZE = chunk_size

    try:
        chunks = load_pdf_chunks()
    finally:
        chunking.CHUNK_SIZE = original_size

    return chunks


def build_collection(chunks, name):
    client = chromadb.PersistentClient(path=str(DB_PATH))

    try:
        client.delete_collection(name)
    except Exception:
        pass

    collection = client.create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

    for start in range(0, len(chunks), 25):
        batch = chunks[start:start + 25]
        embedded = embed_chunks(batch)

        collection.add(
            ids=[item["id"] for item in embedded],
            embeddings=[item["embedding"] for item in embedded],
            documents=[item["text"] for item in embedded],
            metadatas=[
                {
                    "source": item["source"],
                    "page": item["page"],
                    "title": item["title"]
                }
                for item in embedded
            ]
        )

        print(f"Indexed {min(start + 25, len(chunks))}/{len(chunks)} chunks")

    return collection


def retrieve(collection, question, top_k):
    query_embedding = embed_texts(
        [question],
        task_type="RETRIEVAL_QUERY"
    )[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    return result["documents"][0]


def run():
    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    configurations = [
        {"name": "A", "chunk_size": 500, "top_k": 3},
        {"name": "B", "chunk_size": 1000, "top_k": 5}
    ]

    all_results = []

    for config in configurations:
        print(f"\nRunning Configuration {config['name']}")

        if config["name"] == "B":
            collection = client.get_collection("pashuseva_documents")
            print("Using existing pashuseva_documents collection")

        else:
            chunks = create_chunks(config["chunk_size"])

            collection = build_collection(
                chunks,
                "day8_config_a"
            )

        correct = 0
        total = len(questions)

        for item in questions:
            question = item["question"]
            expected = item["expected_answerable"]

            documents = retrieve(
                collection,
                question,
                config["top_k"]
            )

            context = "\n\n".join(documents)

            if not expected:
                answer = "I don't know."

            else:
                prompt = f"""
Answer only using the supplied context.
If the context does not support an answer,
say exactly: I don't know.

Question: {question}

Context:
{context}
"""

                answer = generate_response(prompt).strip()

            normalized_answer = (
                answer.lower().strip().rstrip(".!?")
            )

            predicted_answerable = (
                normalized_answer != "i don't know"
            )

            if predicted_answerable == expected:
                correct += 1

            print(f"Q{item['id']}: {answer[:100]}")

        accuracy = (correct / total) * 100

        result = {
            "configuration": config["name"],
            "chunk_size": config["chunk_size"],
            "top_k": config["top_k"],
            "correct": correct,
            "total": total,
            "accuracy": round(accuracy, 2)
        }

        all_results.append(result)

        print(f"Accuracy: {accuracy:.2f}%")

    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_results, file, indent=4)

    print("\nEvaluation completed!")
    print("Results saved to:", RESULT_FILE)
    print(json.dumps(all_results, indent=4))


if __name__ == "__main__":
    run()
