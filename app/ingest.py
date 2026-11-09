import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "feeding_records.json"
OUTPUT_FILE = BASE_DIR / "data" / "records.json"


def clean_record(raw):

    return {
        "topic": raw["topic"].strip(),
        "animal_type": raw["animal_type"].strip(),
        "recommendation": raw["recommendation"].strip(),
        "quantity_or_schedule": raw["quantity_or_schedule"].strip(),
        "source_doc": raw["source_doc"].strip(),
        "source_url": raw["source_url"].strip()
    }


def ingest_data():

    try:
        with open(RAW_FILE, "r", encoding="utf-8") as file:
            raw_records = json.load(file)

    except FileNotFoundError:
        print("Raw data file not found!")
        return

    except json.JSONDecodeError:
        print("Invalid JSON format!")
        return

    cleaned_records = []

    for index, raw in enumerate(raw_records, start=1):

        try:
            if not isinstance(raw, dict):
                raise ValueError("Record must be a dictionary")

            required_fields = [
                "topic",
                "animal_type",
                "recommendation",
                "quantity_or_schedule",
                "source_doc",
                "source_url"
            ]

            for field in required_fields:
                if field not in raw:
                    raise ValueError(f"Missing field: {field}")

            record = clean_record(raw)
            cleaned_records.append(record)

        except (ValueError, KeyError, AttributeError, TypeError) as error:
            print(f"Skipping bad row {index}: {error}")

    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(cleaned_records, file, indent=4, ensure_ascii=False)

        print(f"Successfully saved {len(cleaned_records)} records!")
        print(f"Output file: {OUTPUT_FILE}")

    except OSError as error:
        print(f"File saving error: {error}")


if __name__ == "__main__":
    ingest_data()