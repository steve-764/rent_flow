from vehilces import Vehicle, EconomyCar, SUV, LuxuryCar
from customer import Customer


class Rental:
    def __init__(self, rental_id, customer, registration_number, rental_days):
        if rental_days <= 0:
            raise ValueError("Car must be rented for atleast 1 day.")
        
        self.rental_id = rental_id
        self.customer = customer
        self.registration_number = registration_number
        self.rental_days = rental_days
        

    # def calculate_cost(self):
    #     return self.vehicle.calculate_rental_cost(self.rental_days)

