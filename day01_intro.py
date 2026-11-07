# ==================================================
#                    PASHUSEVA
#          Smart Dairy Animal Care System
# ==================================================

print("\n" + "=" * 50)
print("              WELCOME TO PASHUSEVA")
print("       Dairy Animal Care Information System")
print("=" * 50)


# 1. FARMER DETAILS

print("\n----------- FARMER DETAILS -----------")

farmer_name = input("Enter your full name: ").strip().title()
village = input("Enter your village: ").strip().title()
taluka = input("Enter your taluka/tehsil: ").strip().title()
district = input("Enter your district: ").strip().title()
state = input("Enter your state: ").strip().title()
pincode = input("Enter your PIN code: ").strip()


# 2. ANIMAL DETAILS

print("\n----------- ANIMAL DETAILS -----------")

animal_type = input(
    "Enter animal type (Cow/Buffalo/Calf): "
).strip().title()

if animal_type not in ["Cow", "Buffalo", "Calf"]:
    print("\nInvalid animal type!")
    print("Please enter Cow, Buffalo or Calf.")

else:

    animal_name = input("Enter animal name: ").strip().title()

    animal_age = float(input("Enter animal age in years: "))

    print("\n----------- ANIMAL PROFILE -----------")

    print("Animal Type:", animal_type)
    print("Animal Name:", animal_name)
    print("Animal Age:", animal_age, "years")

    # 3. MILK PRODUCTION DETAILS

    if animal_type == "Cow" or animal_type == "Buffalo":

        milk_production = float(
            input("Enter daily milk production in litres: ")
        )

        print("Daily Milk Production:", milk_production, "litres")

    elif animal_type == "Calf":

        print("Milk production details are not required for a calf.")

    # 4. FARMER PROFILE SUMMARY

    print("\n----------- FARMER PROFILE -----------")

    print("Farmer Name:", farmer_name)
    print("Village:", village)
    print("Taluka:", taluka)
    print("District:", district)
    print("State:", state)
    print("PIN Code:", pincode)

    print("\n----------- REGISTRATION COMPLETE -----------")
    print("Thank you for using PashuSeva!")