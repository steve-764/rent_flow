class Rental:
    def __init__(self, rental_id, customer, vehicle, rental_days):
        if rental_days <= 0:
            raise ValueError("Car must be rented for atleast 1 day.")
        
        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.rental_days = rental_days
        

    def calculate_cost(self):
        return self.vehicle.calculate_rental_cost(self.days)



# test 

rental1 = Rental("R001", "Cust1", "Car1", 3)
print(rental1.calculate_cost())