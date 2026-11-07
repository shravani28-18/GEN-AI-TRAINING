# ==================================================
#                    PASHUSEVA
#                      MAIN MENU
# ==================================================

print("\n" + "=" * 45)
print("             WELCOME TO PASHUSEVA")
print("       Dairy Animal Care Information")
print("=" * 45)


while True:

    print("\n-------------- MAIN MENU --------------")

    print("1. About PashuSeva")
    print("2. Sample Questions")
    print("3. Animal Care Rule Check")
    print("0. Exit")

    print("---------------------------------------")

    choice = input("Enter your choice: ").strip()


    # OPTION 1: ABOUT PASHUSEVA

    if choice == "1":

        print("\n----------- ABOUT PASHUSEVA -----------")

        print("PashuSeva is a dairy animal care")
        print("information platform for small farmers.")

        print("\nIt provides information about:")

        print("- Animal Feeding")
        print("- Calf Rearing")
        print("- Fodder Conservation")
        print("- Vaccination Schedule")
        print("- Common Animal Diseases")

        print("\nSupported Animals:")
        print("- Cow")
        print("- Buffalo")
        print("- Calf")

        print("\nData Sources:")
        print("- NDDB Farmers' Corner")
        print("- Handbook of Good Dairy Husbandry Practices")


    # OPTION 2: SAMPLE QUESTIONS

    elif choice == "2":

        print("\n----------- SAMPLE QUESTIONS -----------")

        print("1. What should a newborn calf receive first?")
        print("2. When should colostrum be given to a newborn calf?")

        print("\nThese questions help farmers understand")
        print("basic dairy animal care practices.")


    # OPTION 3: ANIMAL CARE RULE CHECK

    elif choice == "3":

        print("\n----------- ANIMAL CARE RULE CHECK -----------")

        animal_type = input(
            "Enter animal type (Cow/Buffalo/Calf): "
        ).strip().title()

        if animal_type == "Cow":

            print("\nCow Care Information:")
            print("- Provide balanced nutrition.")
            print("- Ensure clean drinking water.")
            print("- Follow the recommended vaccination schedule.")

        elif animal_type == "Buffalo":

            print("\nBuffalo Care Information:")
            print("- Provide balanced nutrition.")
            print("- Ensure clean drinking water.")
            print("- Provide suitable cooling and bathing facilities.")

        elif animal_type == "Calf":

            print("\nCalf Care Information:")
            print("- Provide colostrum soon after birth.")
            print("- Maintain proper hygiene.")
            print("- Follow the recommended calf feeding schedule.")

        else:

            print("\nInvalid animal type!")
            print("Please enter Cow, Buffalo or Calf.")


    # OPTION 0: EXIT

    elif choice == "0":

        print("\nThank you for using PashuSeva!")
        print("Have a healthy and productive dairy farm!")
        break


    # INVALID MENU OPTION

    else:

        print("\nInvalid choice!")
        print("Please select 1, 2, 3 or 0.")