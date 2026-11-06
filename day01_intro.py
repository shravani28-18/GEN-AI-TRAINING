
# ==================================================
#                  PASHUSEVA
#       Smart Dairy Animal Care Information
# ==================================================

print("\n" + "=" * 50)
print("               WELCOME TO PASHUSEVA")
print("       Dairy Animal Care Information System")
print("=" * 50)


# 1. Farmer Details

print("\n----------- FARMER DETAILS -----------")

farmer_name = input("Enter your full name: ").strip().title()
village = input("Enter your village: ").strip().title()
taluka = input("Enter your taluka/tehsil: ").strip().title()
district = input("Enter your district: ").strip().title()
state = input("Enter your state: ").strip().title()
pincode = input("Enter your PIN code: ").strip()


# 2. Animal Details

print("\n----------- ANIMAL DETAILS -----------")

animal_type = input(
    "Enter animal type (Cow/Buffalo/Calf): "
).strip().title()

animal_name = input("Enter animal name: ").strip().title()

animal_age = int(input("Enter animal age in years: "))


# 3. Animal-Specific Information

milk_production = None
animal_weight = None

if animal_type in ["Cow", "Buffalo"]:

    milk_production = float(
        input("Enter daily milk production in litres: ")
    )

elif animal_type == "Calf":

    animal_weight = float(
        input("Enter calf weight in kg: ")
    )

else:

    print("This animal type is not currently supported.")
    

# 4. Vaccination Details

vaccination_status = input(
    "Is your animal vaccinated? (Yes/No/Unknown): "
).strip().lower()


# 5. Farmer Question

print("\n----------- FARMER QUESTION -----------")

question = input(
    "What is your animal care question? "
).strip()


# 6. Display Farmer and Animal Profile

print("\n" + "=" * 50)
print("              PASHUSEVA PROFILE")
print("=" * 50)

print(f"Farmer Name       : {farmer_name}")
print(f"Village           : {village}")
print(f"Taluka/Tehsil     : {taluka}")

print("-" * 50)

print(f"Animal Type       : {animal_type}")
print(f"Animal Name       : {animal_name}")
print(f"Animal Age        : {animal_age} years")

if milk_production is not None:
    print(f"Daily Milk        : {milk_production} litres")

if animal_weight is not None:
    print(f"Animal Weight     : {animal_weight} kg")

print(f"Vaccination Status: {vaccination_status}")

print("-" * 50)

print(f"Farmer Question   : {question}")

print("=" * 50)
print(f"Thank you, {farmer_name}!")
print("Welcome to PashuSeva.")
print("=" * 50)
