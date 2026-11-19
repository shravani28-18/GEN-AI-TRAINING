from app.smart_search import search_records


def test_search_records_returns_matching_result(monkeypatch):
    fake_records = [
        {
            "topic": "Feeding",
            "animal_type": "Cow",
            "recommendation": "Feed green fodder daily",
            "quantity_or_schedule": "15-20 kg per day",
        },
        {
            "topic": "Vaccination",
            "animal_type": "Buffalo",
            "recommendation": "Follow vaccination schedule",
            "quantity_or_schedule": "As advised by veterinarian",
        },
    ]

    monkeypatch.setattr(
        "app.smart_search.load_search_records",
        lambda: fake_records,
    )

    results = search_records("green fodder")

    assert len(results) > 0
    assert results[0]["topic"] == "Feeding"
    assert "score" in results[0]


def test_search_records_empty_query():
    results = search_records("   ")

    assert results == []


def test_search_records_no_matching_result(monkeypatch):
    monkeypatch.setattr(
        "app.smart_search.load_search_records",
        lambda: [
            {
                "topic": "Feeding",
                "animal_type": "Cow",
                "recommendation": "Give green fodder",
                "quantity_or_schedule": "Daily",
            }
        ],
    )

    results = search_records("airplane")

    assert results == []