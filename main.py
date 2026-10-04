from vehilces import EconomyCar, SUV, LuxuryCar
from customer import Customer
from payment import MpesaPayment
from car_rental import CarRentalSysytem

# system = CarRentalSysytem("SafariDrive Rentals")
system = CarRentalSysytem()

# Add vehicles
car1 = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
car2 = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
car3 = SUV("KDJ 672B", "Nissan", "X-Trail", 2021, 6500)
car4 = LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000)

for car in [car1, car2, car3, car4]:
    system.add_vehicle(car)

# Register a customer
customer1 = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
system.register_customer(customer1)

# Rent the Prado for 4 days
system.show_available_vehicles()
rental1 = system.rent_vehicle(customer1, car2, 4)
rental1.display_rental_details()

# Try to rent it again (should fail)
try:
    system.rent_vehicle(customer1, car2, 2)
except ValueError as error:
    print(f"Error: {error}")

# Return it 2 days late, then pay
system.return_vehicle(rental1, actual_days=6)
payment1 = MpesaPayment(rental1, "0712345678")
system.process_payment(payment1)

system.generate_report()