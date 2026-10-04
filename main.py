from vehilces import EconomyCar, SUV, LuxuryCar
from customer import Customer
from rentals import Rental
from payment import CardPayment, CashPayment, MpesaPayment


# test 
car1= EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 3000)
car2 = SUV("KBG 222B", "Toyota", "Prado", 2022, 8000)
car3 = LuxuryCar("KGD 678C", "Mercedes", "E-Class", 2022, 15000)

car1.display_details()
# print()

# print(car1.calculate_rental_cost(3))
# print(car2.calculate_rental_cost(3))
# print(car3.calculate_rental_cost(3))

# print()

cust1 = Customer("C001", "Bob", "0712345678", 123456789, "DL1234")
cust3 = Customer("C003", "Newt", "0798456321", 36451278, "DL8795")

# cust1.display_details()

# testing empty driving licence number
# cust2 = Customer("C002", "Mob", "0712345678", 123456789, "")
# cust2.display_details()


# rental = Rental("R001", cust1, car1, rental_days=3)  
# rental.complete_rental(actual_days=5, damage_charge=30)
# rental.mark_as_paid()
# # rental.display_rental_details()

# print()
# rental = Rental("R002", cust3, car3, rental_days=3)  

# rental.complete_rental(actual_days=7)
# rental.display_rental_details()


# # payment = CashPayment(rental, amount_paid=70000)
# # if payment.process_payment():
# #     print("Rental paid:", rental.is_paid())

# payments = [
#     MpesaPayment(rental, "0712345678"),
#     CardPayment(rental, "4417"),
#     CashPayment(rental, 90000),
# ]
# for p in payments:
#     p.process_payment()  

# rental.mark_as_paid()


# # rental.complete_rental(actual_days=5, damage_charge=30)

