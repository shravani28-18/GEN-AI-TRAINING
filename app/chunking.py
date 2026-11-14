
from pathlib import Path
from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS = [
    BASE_DIR / "data" / "downloads" / "pashuseva" / "animal_nutrition_booklet.pdf",
    BASE_DIR / "data" / "downloads" / "pashuseva" / "nddb_handbook.pdf",
    BASE_DIR / "data" / "downloads" / "pashuseva" / "quality_control_manual.pdf",
]

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_text(text):
    """Split text into smaller chunks with overlap."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def load_pdf_chunks():
    """Extract PDF text and preserve document metadata."""
    all_chunks = []

    for pdf_path in DOCUMENTS:
        if not pdf_path.exists():
            print(f"File not found: {pdf_path.name}")
            continue

        print(f"Reading: {pdf_path.name}")

        reader = PdfReader(str(pdf_path))

        title = reader.metadata.title if reader.metadata and reader.metadata.title else pdf_path.stem

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            if not page_text.strip():
                continue

            page_chunks = split_text(page_text)

            for chunk_number, chunk_text in enumerate(page_chunks, start=1):
                all_chunks.append({
                    "id": f"{pdf_path.stem}_page{page_number}_chunk{chunk_number}",
                    "title": title,
                    "source": str(pdf_path.relative_to(BASE_DIR)),
                    "page": page_number,
                    "chunk_number": chunk_number,
                    "text": chunk_text
                })

    return all_chunks


if __name__ == "__main__":
    chunks = load_pdf_chunks()

    print("\nChunking completed!")
    print("Total chunks:", len(chunks))

    if chunks:
        print("\nFirst chunk details:")
        print("Title:", chunks[0]["title"])
        print("Source:", chunks[0]["source"])
        print("Page:", chunks[0]["page"])
        print("Text preview:", chunks[0]["text"][:300])
