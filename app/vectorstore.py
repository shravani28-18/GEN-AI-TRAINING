
from pathlib import Path
import time
import chromadb

from app.chunking import load_pdf_chunks
from app.embed import embed_chunks, embed_texts


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "pashuseva_documents"

BATCH_SIZE = 25


def get_collection():
    """Create or connect to persistent ChromaDB collection."""

    client = chromadb.PersistentClient(path=str(DB_PATH))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def index_documents():
    """Index only chunks that are not already stored."""

    collection = get_collection()
    chunks = load_pdf_chunks()

    if not chunks:
        print("No document chunks found.")
        return

    print("Total chunks:", len(chunks))

    # Get IDs of already indexed chunks
    existing = collection.get(
        where={"document_type": "pashuseva"},
        include=["metadatas"]
    )

    existing_ids = set(existing["ids"])

    # Find chunks that are not indexed yet
    pending_chunks = [
        chunk for chunk in chunks
        if chunk["id"] not in existing_ids
    ]

    print("Already indexed:", len(existing_ids))
    print("Remaining chunks:", len(pending_chunks))

    if not pending_chunks:
        print("All chunks are already indexed!")
        return

    total_indexed = len(existing_ids)

    # Process only remaining chunks
    for start in range(0, len(pending_chunks), BATCH_SIZE):

        batch = pending_chunks[start:start + BATCH_SIZE]

        print(
            f"Embedding remaining batch: "
            f"{start + 1} to {start + len(batch)}"
        )

        for attempt in range(3):
            try:
                embedded_batch = embed_chunks(batch)
                break

            except Exception as error:

                message = str(error)

                if (
                    "429" not in message
                    and "RESOURCE_EXHAUSTED" not in message
                ):
                    raise

                if attempt == 2:
                    raise

                wait_time = 30 * (attempt + 1)

                print(
                    f"Rate limit reached. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

        time.sleep(5)

        # Save embeddings in ChromaDB
        collection.add(
            ids=[
                item["id"]
                for item in embedded_batch
            ],

            embeddings=[
                item["embedding"]
                for item in embedded_batch
            ],

            documents=[
                item["text"]
                for item in embedded_batch
            ],

            metadatas=[
                {
                    "title": item["title"],
                    "source": item["source"],
                    "page": item["page"],
                    "chunk_number": item["chunk_number"],
                    "document_type": "pashuseva"
                }
                for item in embedded_batch
            ]
        )

        total_indexed += len(batch)

        print("Indexed:", total_indexed)

    print("\nIndexing completed!")
    print("Total indexed chunks:", collection.count())
    print("Database location:", DB_PATH)


def search_similar(query, top_k=5):
    """Find document chunks relevant to a query."""

    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = embed_texts(
        [query],
        task_type="RETRIEVAL_QUERY"
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    hits = []

    for i in range(len(results["ids"][0])):

        hits.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return hits


if __name__ == "__main__":
    index_documents()
