
# ==================================================
#                  PASHUSEVA
#                   MAIN MENU
# ==================================================

print("\n" + "=" * 45)
print("             WELCOME TO PASHUSEVA")
print("=" * 45)


while True:

    print("\n-------------- MAIN MENU --------------")
    print("1. About PashuSeva")
    print("2. Sample Questions")
    print("3. Animal Care Rule Check")
    print("0. Exit")
    print("---------------------------------------")

    choice = input("Enter your choice: ").strip()


    # Option 1: About PashuSeva

    if choice == "1":

        print("\n----------- ABOUT PASHUSEVA -----------")

        print("PashuSeva is a dairy animal care")
        print("information platform for small farmers.")

        print("\nIt provides information about:")
        print("- Animal Feeding")
        print("- Calf Rearing")
        print("- Vaccination")
        print("- Common Animal Diseases")

        print("---------------------------------------")


    # Option 2: Sample Questions

    elif choice == "2":

        print("\n----------- SAMPLE QUESTIONS -----------")

        print("1. How can I reduce cattle feeding costs?")
        print("2. How can I prevent repeated mastitis?")

        print("----------------------------------------")


    # Option 3: Animal Care Rule Check

    elif choice == "3":

        status = input(
            "\nIs your dairy animal vaccinated? (Yes/No/Unknown): "
        ).strip().lower()

        if status == "yes":

            print("\nVaccination status: Yes")
            print("Keep the vaccination record updated.")

        elif status == "no":

            print("\nVaccination status: No")
            print("Contact a veterinarian for the appropriate")
            print("vaccination schedule for your animal.")

        elif status == "unknown":

            print("\nVaccination status is unknown.")
            print("Check the animal's vaccination record")
            print("or contact a veterinarian.")

        else:

            print("\nInvalid input!")
            print("Please enter Yes, No or Unknown.")

        print("----------------------------------------")


    # Option 0: Exit

    elif choice == "0":

        print("\nThank you for using PashuSeva!")
        print("Goodbye!")
        print("----------------------------------------")

        break


    # Invalid Menu Choice

    else:

        print("\nInvalid choice!")
        print("Please select 0, 1, 2 or 3.")



