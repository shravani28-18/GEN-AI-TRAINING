# ==================================================
#                  PASHUSEVA
#               RECORD FUNCTIONS
# ==================================================

from data.sample_records import records


# 1. LOAD ALL RECORDS

def load_records():

    return records


# 2. SEARCH RECORDS

def search(keyword):

    keyword = keyword.lower()

    results = []

    for record in records:

        searchable_text = " ".join(
            str(value) for value in record.values()
        ).lower()

        if keyword in searchable_text:

            results.append(record)

    return results


# 3. COUNT BY CATEGORY

def count_by(category_field="topic"):

    category_count = {}

    for record in records:

        category = record[category_field]

        if category in category_count:

            category_count[category] += 1

        else:

            category_count[category] = 1

    return category_count


# 4. GET RECORD BY ID

def get_by_id(record_id):

    if record_id < 1 or record_id > len(records):

        return None

    return records[record_id - 1]