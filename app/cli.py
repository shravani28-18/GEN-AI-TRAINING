# ==================================================
#                   PASHUSEVA
#                  MAIN CLI APP
# ==================================================

from app.records import (
    load_records,
    search,
    count_by,
    get_by_id
)

# 1. DISPLAY ALL RECORDS

def show_all_records():

    all_records = load_records()

    print("\n========== ALL RECORDS ==========")

    for record in all_records:

        print("\nTopic:", record["topic"])
        print("Animal:", record["animal_type"])
        print("Recommendation:", record["recommendation"])
        print("Quantity/Schedule:", record["quantity_or_schedule"])
        print("Source:", record["source_doc"])
        print("URL:", record["source_url"])

        print("-" * 50)


# 2. SEARCH RECORDS

def search_menu():

    keyword = input("\nEnter keyword: ")

    results = search(keyword)

    print("\n========== SEARCH RESULTS ==========")

    if results:

        for record in results:

            print("\nTopic:", record["topic"])
            print("Animal:", record["animal_type"])
            print("Recommendation:", record["recommendation"])

    else:

        print("No records found.")


# 3. CATEGORY COUNT

def count_menu():

    counts = count_by()

    print("\n========== CATEGORY COUNT ==========")

    for category, total in counts.items():

        print(category, ":", total)


# 4. GET RECORD BY ID

def get_record_menu():

    try:

        record_id = int(input("\nEnter record ID: "))

        record = get_by_id(record_id)

        if record:

            print("\n========== RECORD DETAILS ==========")

            for key, value in record.items():

                print(key, ":", value)

        else:

            print("Record ID not found.")

    except ValueError:

        print("Please enter a valid numeric ID.")


# 5. MAIN MENU

def main():

    while True:

        print("\n========== PASHUSEVA CLI ==========")

        print("1. Display All Records")
        print("2. Search Records")
        print("3. Count By Category")
        print("4. Get Record By ID")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            show_all_records()

        elif choice == "2":

            search_menu()

        elif choice == "3":

            count_menu()

        elif choice == "4":

            get_record_menu()

        elif choice == "0":

            print("\nThank you for using PashuSeva!")

            break

        else:

            print("\nInvalid choice! Try again.")


if __name__ == "__main__":

    main()