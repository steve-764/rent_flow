from vehilces import EconomyCar, SUV, LuxuryCar
from customer import Customer
from payment import MpesaPayment, CardPayment, CashPayment
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

customer2 = Customer("C002", "Mark Levin", "0797456321", "20121457", "DL98485")
system.register_customer(customer2)

customer3 = Customer("C003", "Anna Beth", "0754789632", "30745289", "DL84571")
system.register_customer(customer3)

# Rent the Prado for 4 days
system.show_available_vehicles()
rental1 = system.rent_vehicle(customer1, car2, 4)

# # Try to rent it again (should fail)
# try:
#     system.rent_vehicle(customer1, car2, 2)
# except ValueError as error:
#     print(f"Error: {error}")

# Return it 2 days late, then pay
system.return_vehicle(rental1, actual_days=6)
rental1.display_rental_details()
payment1 = CardPayment(rental1, 5678)
system.process_payment(payment1)

# ===================================
rental2 = system.rent_vehicle(customer2, car1, 9)

system.return_vehicle(rental2, actual_days=9)
rental1.display_rental_details()
payment2 = CashPayment(rental2, 64788)
system.process_payment(payment2)


# ===================================
rental3 = system.rent_vehicle(customer2, car4, 1)

system.return_vehicle(rental3, actual_days=2)
rental1.display_rental_details()
payment2 = MpesaPayment(rental3, "0797456321")
system.process_payment(payment2)

system.generate_report()