from vehilces import Vehicle, EconomyCar, SUV, LuxuryCar
from customer import Customer


class Rental:
    def __init__(self, rental_id, customer, vehicle, rental_days):
        if rental_days < 1:
            raise ValueError("Car must be rented for atleast 1 day.")
        if not Vehicle.is_available():
            raise ValueError("Vehicle not available for rent.")
        
        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.rental_days = rental_days
        self.actual_days = None
        self.status = None
        self.base_cost = Vehicle.calculate_rental_cost(rental_days)
        self.late_fee = 0
        self.damage_fee = 0
        self.__paid = False

        self.vehicle.mark_as_rented()

    penalty_rate = 0.2
    def calculate_late_fee(self):
        if self.actual_days is None:
            return 0
        late_days = self.actual_days - self.rental_days
        daily_penalty = self.penalty_rate * self.vehicle.daily_rate
        self.late_fee = late_days * daily_penalty
        return self.late_fee

    def calculate_total(self):
        return self.base_cost + self.late_fee + self.damage_fee

    def complete_rental(self, actual_days, damage_charge = 0):
        self.actual_days = actual_days
        self.damage_fee = damage_charge
        self.calculate_late_fee()
        self.status = "COMPLETED"
        self.vehicle.mark_as_available()



