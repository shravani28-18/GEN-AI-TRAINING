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

    # Existing collection असेल तर तीच वापरायची.
    # Collection delete करायची नाही.
    try:
        collection = client.get_collection(name)
        print(f"Resuming existing collection: {name}")

    except ValueError:
        collection = client.create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Created new collection: {name}")

    # आधी index झालेले IDs शोधायचे.
    existing_ids = set(
        collection.get(include=[])["ids"]
    )

    print(f"Already indexed: {len(existing_ids)} chunks")

    batch_size = 25

    for start in range(0, len(chunks), batch_size):

        original_batch = chunks[start:start + batch_size]

        # आधीच index झालेले chunks skip करायचे.
        batch = [
            item for item in original_batch
            if item["id"] not in existing_ids
        ]

        if not batch:
            continue

        # फक्त नवीन chunks embed करायचे.
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

        # Newly added IDs update करायचे.
        existing_ids.update(
            item["id"] for item in embedded
        )

        print(
            f"Indexed: {len(existing_ids)}/{len(chunks)} chunks"
        )

    print(f"Collection completed: {collection.count()} chunks")

    return collection


def retrieve(collection, query_embedding, top_k):
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    return result["documents"][0]


def run():
    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    if len(questions) != 15:
        raise ValueError(
            f"Expected 15 evaluation questions, found {len(questions)}"
        )

    query_embeddings = embed_texts(
        [item["question"] for item in questions],
        task_type="RETRIEVAL_QUERY"
    )

    print("Question embeddings generated successfully!")

    client = chromadb.PersistentClient(path=str(DB_PATH))

    configurations = [
        {"name": "A", "chunk_size": 500, "top_k": 3},
        {"name": "B", "chunk_size": 1000, "top_k": 5}
    ]

    all_results = []

    for config in configurations:

        print(f"\nRunning Configuration {config['name']}")

        if config["name"] == "B":

            collection = client.get_collection(
                "pashuseva_documents"
            )

            print("Using existing pashuseva_documents collection")

        else:

            chunks = create_chunks(config["chunk_size"])

            print(f"Total chunks generated: {len(chunks)}")

            collection = build_collection(
                chunks,
                "day8_config_a"
            )

        correct = 0
        total = len(questions)

        for index, item in enumerate(questions):

            question = item["question"]
            expected = item["expected_answerable"]

            documents = retrieve(
                collection,
                query_embeddings[index],
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