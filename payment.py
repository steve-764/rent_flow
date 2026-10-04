from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, rental):
        self.rental = rental
        self.amount = rental.calculate_total()

    @abstractmethod
    def process_payment(self):
        pass


    def validate_rental(self):
        if self.status != "COMPLETED":
            print("Payment Failed. Rental not competed.")
            return False
        if self.rental.is_paid():
            print("Payment Failed: Rental is alreadt paid.")
            return False
        return True

    def finalise(self):
        self.rental.mark_as_paid()
        return True

    
