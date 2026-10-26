
from .models import CarMake, CarModel


def initiate():
    car_data = [
        {
            "name": "Toyota",
            "description": "Japanese automobile manufacturer",
            "models": [
                ("Camry", "Sedan", 2022, 1),
                ("Corolla", "Sedan", 2021, 1),
                ("RAV4", "SUV", 2023, 1),
            ],
        },
        {
            "name": "Honda",
            "description": "Japanese automobile manufacturer",
            "models": [
                ("Civic", "Sedan", 2022, 2),
                ("Accord", "Sedan", 2021, 2),
                ("CR-V", "SUV", 2023, 2),
            ],
        },
        {
            "name": "Ford",
            "description": "American automobile manufacturer",
            "models": [
                ("Mustang", "Sedan", 2020, 3),
                ("Explorer", "SUV", 2022, 3),
                ("Focus", "Wagon", 2021, 3),
            ],
        },
        {
            "name": "BMW",
            "description": "German automobile manufacturer",
            "models": [
                ("3 Series", "Sedan", 2022, 4),
                ("X3", "SUV", 2023, 4),
                ("5 Series", "Sedan", 2021, 4),
            ],
        },
        {
            "name": "Audi",
            "description": "German automobile manufacturer",
            "models": [
                ("A4", "Sedan", 2022, 5),
                ("Q5", "SUV", 2023, 5),
                ("A6", "Sedan", 2021, 5),
            ],
        },
    ]

    for item in car_data:
        make, _ = CarMake.objects.get_or_create(
            name=item["name"],
            defaults={"description": item["description"]},
        )

        for model_name, car_type, year, dealer_id in item["models"]:
            CarModel.objects.get_or_create(
                car_make=make,
                name=model_name,
                defaults={
                    "type": car_type,
                    "year": year,
                    "dealer_id": dealer_id,
                },
            )

    print("Car makes and models populated successfully.")
