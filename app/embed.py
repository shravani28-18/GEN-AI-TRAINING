
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.chunking import load_pdf_chunks


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768


def get_client():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env file")

    return genai.Client(api_key=GEMINI_API_KEY)


def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT"):
    """Generate embeddings for a list of texts."""

    if not texts:
        return []

    client = get_client()

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return [item.values for item in response.embeddings]


def embed_chunks(chunks):
    """Generate embeddings and attach them to document chunks."""

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts, task_type="RETRIEVAL_DOCUMENT")

    if len(embeddings) != len(chunks):
        raise ValueError("Number of embeddings does not match number of chunks")

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks


if __name__ == "__main__":
    print("Loading PashuSeva document chunks...")

    chunks = load_pdf_chunks()

    if not chunks:
        print("No document chunks found.")
    else:
        # Test only 3 chunks first to avoid unnecessary API usage.
        sample_chunks = chunks[:3]

        print("Generating embeddings for 3 sample chunks...")

        embedded_chunks = embed_chunks(sample_chunks)

        print("\nEmbedding test successful!")
        print("Tested chunks:", len(embedded_chunks))
        print("Embedding dimensions:", len(embedded_chunks[0]["embedding"]))
        print("First chunk title:", embedded_chunks[0]["title"])
        print("First chunk page:", embedded_chunks[0]["page"])
