
import json
import time
from pathlib import Path

from app.smart_search import search_records
from app.llm import generate_response


# Project folder path
BASE_DIR = Path(__file__).resolve().parent.parent

# Input questions file
QUESTIONS_FILE = BASE_DIR / "data" / "pashuseva_questions.json"

# Prompt files
PROMPT_A_FILE = BASE_DIR / "prompts" / "task1_v1.txt"
PROMPT_B_FILE = BASE_DIR / "prompts" / "task1_v2.txt"
SYSTEM_PROMPT_FILE = BASE_DIR / "prompts" / "system.txt"

# Output file
OUTPUT_FILE = BASE_DIR / "eval" / "results.json"


# Load questions
def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Load prompt
def load_prompt(prompt_file):
    return prompt_file.read_text(encoding="utf-8")


# Get relevant records
def get_context(question):
    records = search_records(question)

    if not records:
        return "No relevant PashuSeva records available."

    context = "\n\n".join([
        f"Topic: {record['topic']}\n"
        f"Animal: {record['animal_type']}\n"
        f"Recommendation: {record['recommendation']}\n"
        f"Quantity or Schedule: {record['quantity_or_schedule']}\n"
        f"Source: {record['source_doc']}"
        for record in records
    ])

    return context


# Build complete prompt
def build_prompt(template, question, context, system_prompt):
    task_prompt = template.format(
        question=question,
        context=context
    )

    return system_prompt + "\n\n" + task_prompt


# Call Gemini with retry for rate limits
def safe_generate_response(prompt):
    for attempt in range(3):
        try:
            response = generate_response(prompt)

            # Keep requests below the free-tier per-minute limit
            time.sleep(5)

            return response

        except Exception as error:
            error_message = str(error)

            if "429" not in error_message and "RESOURCE_EXHAUSTED" not in error_message:
                raise

            if attempt == 2:
                raise

            print("Gemini rate limit reached. Waiting 20 seconds...")
            time.sleep(20)


# Generate answer
def run_prompt(prompt_file, question, context, system_prompt):
    template = load_prompt(prompt_file)

    prompt = build_prompt(
        template,
        question,
        context,
        system_prompt
    )

    return safe_generate_response(prompt)


# Save results after every answer
def save_results(results):
    ordered_results = sorted(
        results.values(),
        key=lambda item: item["id"]
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            ordered_results,
            file,
            indent=4,
            ensure_ascii=False
        )


# Run evaluation
def run_evaluation():
    questions = load_questions()
    system_prompt = load_prompt(SYSTEM_PROMPT_FILE)

    results = {}

    # Load previous results if available
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            old_results = json.load(file)

        for item in old_results:
            results[str(item["id"])] = item

        print("Previous results loaded.")

    for item in questions:
        question_id = str(item["id"])
        question = item["question"]

        if question_id not in results:
            results[question_id] = {
                "id": item["id"],
                "question": question,
                "related_topic": item["related_topic"],
                "answer_available": item["answer_available"],
                "prompt_a_answer": "",
                "prompt_b_answer": ""
            }

        result = results[question_id]

        context = get_context(question)

        print(f"\nTesting Question {item['id']}: {question}")

        # Prompt A
        if not result["prompt_a_answer"]:
            print("Generating Prompt A answer...")

            result["prompt_a_answer"] = run_prompt(
                PROMPT_A_FILE,
                question,
                context,
                system_prompt
            )

            save_results(results)
            print("Prompt A saved.")

        else:
            print("Prompt A already completed. Skipping.")

        # Prompt B
        if not result["prompt_b_answer"]:
            print("Generating Prompt B answer...")

            result["prompt_b_answer"] = run_prompt(
                PROMPT_B_FILE,
                question,
                context,
                system_prompt
            )

            save_results(results)
            print("Prompt B saved.")

        else:
            print("Prompt B already completed. Skipping.")

    print("\nEvaluation completed!")
    print("Total questions:", len(questions))
    print("Results saved to:", OUTPUT_FILE)


# Main execution
if __name__ == "__main__":
    run_evaluation()
