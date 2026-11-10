
import json
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def explore_records():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    df = pd.DataFrame(records)

    print("\n========== PASHUSEVA DATA ANALYSIS ==========")

    # Fact 1: Total records
    print("\nFact 1: Total Records")
    print("Total records:", len(df))

    # Fact 2: Records by topic
    print("\nFact 2: Records by Topic")
    print(df["topic"].value_counts())

    # Fact 3: Records by animal type
    print("\nFact 3: Records by Animal Type")
    print(df["animal_type"].value_counts())


if __name__ == "__main__":
    explore_records()
