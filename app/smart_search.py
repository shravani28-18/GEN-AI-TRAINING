import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def load_search_records():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_records(query, limit=5):

    query = query.strip()

    if not query:
        return []

    records = load_search_records()

    if not records:
        return []

    documents = []

    for record in records:
        text = " ".join([
            record["topic"],
            record["animal_type"],
            record["recommendation"],
            record["quantity_or_schedule"]
        ])
        documents.append(text)

    vectorizer = TfidfVectorizer()

    record_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(
        query_vector,
        record_vectors
    ).flatten()

    ranked_indices = similarity_scores.argsort()[::-1]

    results = []

    for index in ranked_indices:

        score = float(similarity_scores[index])

        if score <= 0:
            continue

        result = records[index].copy()
        result["score"] = round(score, 4)

        results.append(result)

        if len(results) >= limit:
            break

    return results