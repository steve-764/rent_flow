from enum import Enum
from vehilces import Vehicle
from customer import Customer


class RentalStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Rental:
    def __init__(self, rental_id, customer, vehicle, rental_days):
        if rental_days < 1:
            raise ValueError("Car must be rented for atleast 1 day.")
        if not vehicle.is_available():
            raise ValueError("Vehicle not available for rent.")
        
        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.rental_days = rental_days
        self.actual_days = None
        self.status = RentalStatus.ACTIVE
        self.base_cost = vehicle.calculate_rental_cost(rental_days)
        self.late_fee = 0
        self.damage_fee = 0
        self.__paid = False

        self.vehicle.mark_as_rented()


    penalty_rate = 0.2

    def calculate_late_fee(self):
        if self.actual_days is None:
            return 0
        late_days = max(0, self.actual_days - self.rental_days)
        daily_penalty = self.penalty_rate * self.vehicle.daily_rate
        self.late_fee = late_days * daily_penalty
        return self.late_fee

    def calculate_total(self):
        return self.base_cost + self.late_fee + self.damage_fee

    def complete_rental(self, actual_days, damage_charge = 0):
        if self.status != RentalStatus.ACTIVE:
            raise ValueError("Only currently rented vehicles can be returned.")
        if actual_days < 1:
            raise ValueError("Vehicle must be rented for atleast 1 day")
        if damage_charge < 0:
            raise ValueError("Damage charge cannot be negative")

        
        self.actual_days = actual_days
        self.damage_fee = damage_charge
        self.calculate_late_fee()
        self.status = RentalStatus.COMPLETED
        self.vehicle.mark_as_available()

    def cancel_rental(self):
        if self.status != RentalStatus.ACTIVE:
            raise ValueError("Only actively rented vehicles can be cancellled.")
        self.status = RentalStatus.CANCELLED
        self.vehicle.mark_as_available()


    def mark_as_paid(self):
        self.__paid = True

    def is_paid(self):
        return self.__paid


    def display_rental_details(self):
        print(f"--- Rental {self.rental_id} ---")
        print(f"Customer : {self.customer.name}")    
        print(f"Vehicle  : {self.vehicle.make} {self.vehicle.model} ({self.vehicle.registration_number})")
        print(f"Status   : {self.status}")
        print(f"Days     : {self.rental_days} agreed, {self.actual_days if self.actual_days is not None else '-'} actual")
        print(f"Base cost: {self.base_cost:.2f}")
        print(f"Late fee : {self.late_fee:.2f}")
        print(f"Damage   : {self.damage_fee:.2f}")
        print(f"TOTAL    : {self.calculate_total():.2f}")
        print(f"Paid     : {'Yes' if self.is_paid() else 'No'}")


    def __str__(self):
        return (f"{self.rental_id} | {self.vehicle.make} {self.vehicle.model} "
                f"({self.vehicle.registration_number}) | {self.rental_days} days | "
                f"{self.status.value} | KSh {self.calculate_total():,.0f}")


