from app.records import (
    count_by,
    get_by_id,
    load_records,
    search,
)


def test_load_records_returns_list():
    data = load_records()

    assert isinstance(data, list)
    assert len(data) > 0


def test_search_returns_matching_records():
    first_record = load_records()[0]
    keyword = str(next(iter(first_record.values())))

    results = search(keyword)

    assert len(results) > 0


def test_count_by_topic():
    counts = count_by()

    assert isinstance(counts, dict)
    assert sum(counts.values()) == len(load_records())


def test_get_by_id_first_record():
    assert get_by_id(1) == load_records()[0]


def test_get_by_id_invalid_returns_none():
    assert get_by_id(0) is None
    assert get_by_id(len(load_records()) + 1) is None