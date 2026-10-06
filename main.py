from vehilces import EconomyCar, SUV, LuxuryCar
from customer import Customer
from payment import MpesaPayment, CardPayment, CashPayment
from car_rental import CarRentalSysytem

system = CarRentalSysytem()

# Add vehicles
car1 = EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 4000)
car2 = SUV("KDJ 456B", "Toyota", "Prado", 2023, 8000)
car3 = SUV("KDJ 672B", "Nissan", "X-Trail", 2021, 6500)
car4 = LuxuryCar("KDL 789C", "Mercedes-Benz", "E-Class", 2024, 15000)
car5 = EconomyCar("KBD 556P", "Mazda", "Demio", 2021, 2500)
car6 = LuxuryCar("KDE 001A", "Nissan", "ALtima", 2024, 10900)

for car in [car1, car2, car3, car4, car5, car6]:
    system.add_vehicle(car)

#======================================
# Register customers

customer1 = Customer("C001", "John Kamau", "0712345678", "12345678", "DL45821")
customer2 = Customer("C002", "Mark Levin", "0797456321", "20121457", "DL98485")
customer3 = Customer("C003", "Anna Beth", "0754789632", "30745289", "DL84571")

system.register_customer(customer1)
system.register_customer(customer2)
system.register_customer(customer3)

#============================================

# system.show_available_vehicles()
# Rent the Prado for 4 days
# system.show_available_vehicles()
rental1 = system.rent_vehicle(customer1, car2, 4)


# # Try to rent it again (should fail)
# try:
#     system.rent_vehicle(customer1, car2, 2)
# except ValueError as error:
#     print(f"Error: {error}")


# Return it 2 days late, then pay
system.return_vehicle(rental1, actual_days=6)
payment1 = CardPayment(rental1, 5678)
system.process_payment(payment1)
# rental1.display_rental_details()

# # ===================================
rental2 = system.rent_vehicle(customer2, car1, 9)

# system.return_vehicle(rental2, actual_days=9)
# payment2 = CashPayment(rental2, 64788)
# system.process_payment(payment2)
# rental2.display_rental_details()

# # ===================================
rental3 = system.rent_vehicle(customer2, car6, 14)

system.return_vehicle(rental3, actual_days=15)
payment3 = CashPayment(rental3, 50000)
system.process_payment(payment3)
# rental3.display_rental_details()



# # ===================================
rental4 = system.rent_vehicle(customer3, car5, 8)

system.return_vehicle(rental4, actual_days=8)
payment4 = MpesaPayment(rental4, "0797456321")
system.process_payment(payment4)
# rental4.display_rental_details()


# # ===================================
# testing cancelled rental
# system.show_available_vehicles()
rental5 = system.rent_vehicle(customer1, car6, 14)
rental5.cancel_rental()
# rental5.display_rental_details()


# # ===============================

# # viewing customer rental history
# print()
# customer1.view_rental_history()
# print()
# customer2.view_rental_history()
# print()
# customer3.view_rental_history()

# # ===============================
system.generate_report()