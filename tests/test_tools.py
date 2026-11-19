from datetime import date

from app.tools import add_months, cattle_vaccine_scheduler


def test_add_months():
    result = add_months(date(2026, 1, 31), 1)

    assert result == date(2026, 2, 28)


def test_vaccination_scheduler(monkeypatch):
    fake_vaccines = [
        {
            "topic": "Vaccination",
            "animal_type": "Cow/Buffalo",
            "recommendation": "FMD vaccination",
            "quantity_or_schedule": "First dose at 3 months",
            "schedule": {
                "first_dose_months": 3,
            },
            "source_doc": "NDDB Handbook",
            "source_url": "https://example.com",
        }
    ]

    monkeypatch.setattr(
        "app.tools.load_vaccination_records",
        lambda: fake_vaccines,
    )

    results = cattle_vaccine_scheduler(
        birth_date="2026-01-15",
        animal_type="Cow",
        today=date(2026, 4, 15),
    )

    assert len(results) > 0
    assert results[0]["status"] == "First dose due"
    assert results[0]["due_date"] == "2026-04-15"