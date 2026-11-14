import json
from pathlib import Path

from app.vectorstore import search_similar


# Project folder path
BASE_DIR = Path(__file__).resolve().parent.parent

# Questions file
QUESTIONS_FILE = BASE_DIR / "data" / "pashuseva_questions.json"

# Evaluation output file
OUTPUT_FILE = BASE_DIR / "eval" / "search_results.md"


def evaluate_search():

    # Load farmer questions
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    report = []

    report.append("# PashuSeva Semantic Search Evaluation\n")
    report.append("## Evaluation Results\n")
    report.append("- Embedding Model: gemini-embedding-001")
    report.append("- Vector Database: ChromaDB")
    report.append("- Total Questions: 10")
    report.append("- Top Results: 5\n")

    # Search each question
    for item in questions:

        question = item["question"]

        print(f"Evaluating Question {item['id']}...")

        results = search_similar(question, top_k=5)

        report.append(f"## Question {item['id']}")
        report.append(f"**Question:** {question}")
        report.append(f"**Related Topic:** {item['related_topic']}")
        report.append(
            f"**Answer Available:** {item['answer_available']}\n"
        )

        if not results:
            report.append("No matching results found.\n")
            continue

        for rank, result in enumerate(results, start=1):

            metadata = result["metadata"]

            report.append(f"### Result {rank}")
            report.append(f"- Source: {metadata.get('source', 'Unknown')}")
            report.append(f"- Page: {metadata.get('page', 'Unknown')}")
            report.append(f"- Distance: {result['distance']:.4f}")
            report.append(f"- Text: {result['text'][:500]}\n")

    # Save evaluation report
    OUTPUT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nEvaluation completed!")
    print("Report saved at:", OUTPUT_FILE)


if __name__ == "__main__":
    evaluate_search()