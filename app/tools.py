
import json
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def load_vaccination_records():
    """Load vaccination schedules from records.json."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    vaccines = []

    for record in records:
        if record.get("topic", "").lower() in ["vaccination", "vaccinations"]:
            vaccines.append(record)

    return vaccines


def add_months(start_date, months):
    """Add months to a date without causing invalid dates."""

    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1

    # Handle dates such as 31st when the next month has fewer days
    import calendar

    day = min(start_date.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def cattle_vaccine_scheduler(
    birth_date,
    animal_type="Cow",
    vaccination_history=None,
    today=None,
    female=False,
    crossbred=False,
    endemic_area=False
):
    """
    Calculate vaccination due dates.

    birth_date: YYYY-MM-DD
    vaccination_history:
        {
            "FMD Vaccination": {
                "last_date": "YYYY-MM-DD",
                "dose_number": 1
            }
        }
    """

    if vaccination_history is None:
        vaccination_history = {}

    if today is None:
        today = date.today()

    birth_date = date.fromisoformat(birth_date)

    vaccines = load_vaccination_records()
    results = []

    for vaccine in vaccines:

        topic = vaccine["topic"]
        schedule = vaccine.get("schedule", {})
        animal_requirement = vaccine.get("animal_type", "")

                        # Eligibility checks
        if "Female Calf" in animal_requirement and not female:
            continue

        if "Crossbred/Exotic" in animal_requirement and not crossbred:
            continue

        if (
            "Cow/Buffalo" in animal_requirement
            and animal_type.lower() not in ["cow", "buffalo"]
        ):
            continue

        if schedule.get("endemic_area_only") and not endemic_area:
            continue

        # Calculate earliest eligible date
        min_months = schedule.get("first_dose_min_months")

        if min_months is None:
            min_months = schedule.get("first_dose_months")

        if min_months is not None:
            first_dose_date = add_months(birth_date, min_months)
        else:
            first_dose_date = birth_date

        # Brucellosis age window
        max_months = schedule.get("first_dose_max_months")

        if max_months is not None:
            last_eligible_date = add_months(birth_date, max_months)
        else:
            last_eligible_date = None

        history = vaccination_history.get(topic)

        if history is None:

            if today < first_dose_date:
                status = "Upcoming"
                due_date = first_dose_date

            elif last_eligible_date and today > last_eligible_date:
                status = "Eligibility window passed - consult veterinarian"
                due_date = None

            else:
                status = "First dose due"
                due_date = first_dose_date

        else:

            last_date = date.fromisoformat(history["last_date"])
            dose_number = history.get("dose_number", 1)

            if schedule.get("once_in_lifetime"):
                status = "Already vaccinated - no repeat schedule"
                due_date = None

            elif schedule.get("booster_months") and dose_number == 1:
                due_date = add_months(
                    last_date,
                    schedule["booster_months"]
                )
                status = "Booster due" if today >= due_date else "Booster upcoming"

            elif schedule.get("repeat_months"):
                due_date = add_months(
                    last_date,
                    schedule["repeat_months"]
                )
                status = "Vaccination due" if today >= due_date else "Upcoming"

            else:
                due_date = None
                status = "Schedule requires veterinarian confirmation"

        results.append({
            "vaccine": topic,
            "status": status,
            "due_date": due_date.isoformat() if due_date else None,
            "schedule": vaccine.get("quantity_or_schedule"),
            "source": vaccine.get("source_doc"),
            "source_url": vaccine.get("source_url")
        })

    return results
