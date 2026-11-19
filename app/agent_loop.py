
from app.llm import generate_response
from app.rag import answer_question
from app.tools import cattle_vaccine_scheduler


def run_agent(question, animal_profile=None):
    """
    Handwritten agent:
    1. Decides which tool to use.
    2. Executes the selected tool.
    3. Returns the result.
    """

    question_lower = question.lower()

    vaccine_keywords = [
        "vaccine",
        "vaccination",
        "vaccinated",
        "vaccination schedule",
        "vaccine due",
        "booster",
        "fmd",
        "hs",
        "bq",
        "brucellosis",
        "theileriosis",
        "लसीकरण",
        "लस",
        "लसी",
        "लस कधी",
    ]

    # Tool 1: Vaccination scheduler
    if any(keyword in question_lower for keyword in vaccine_keywords):

        if not animal_profile or not animal_profile.get("birth_date"):
            return {
                "tool": "cattle_vaccine_scheduler",
                "message": (
                    "Please provide the animal's birth date "
                    "(YYYY-MM-DD) to calculate vaccination dates."
                )
            }

        results = cattle_vaccine_scheduler(
            birth_date=animal_profile["birth_date"],
            animal_type=animal_profile.get("animal_type", "Cow"),
            vaccination_history=animal_profile.get(
                "vaccination_history", {}
            ),
            today=animal_profile.get("today"),
            female=animal_profile.get("female", False),
            crossbred=animal_profile.get("crossbred", False),
            endemic_area=animal_profile.get("endemic_area", False)
        )

        tool_output = str(results)

        prompt = f"""
You are PashuSeva, an animal-care information assistant.

User question:
{question}

Vaccination scheduler results:
{tool_output}

Instructions:
- Explain the results in simple language.
- Use the dates returned by the scheduler.
- Do not invent vaccination dates or schedules.
- Mention the source when available.
- Recommend confirming vaccination with a veterinarian.
- If the results are empty, explain that no eligible vaccine
  schedule was found for the provided animal details.
"""

        response = generate_response(prompt)

        return {
            "tool": "cattle_vaccine_scheduler",
            "tool_result": results,
            "answer": response
        }

    # Tool 2: RAG search
    else:

        response = answer_question(question, top_k=5)

        return {
            "tool": "rag_search",
            "answer": response
        }
