import random
import string
from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, rental):
        self.rental = rental
        self.amount = rental.calculate_total()

    @abstractmethod
    def process_payment(self):
        pass


    def _validate_rental(self):
        if self.status != "COMPLETED":
            print("Payment Failed. Rental not competed.")
            return False
        if self.rental.is_paid():
            print("Payment Failed: Rental is alreadt paid.")
            return False
        return True

    def _finalise(self):
        self.rental.mark_as_paid()
        return True


class MpesaPayment(Payment):
    def __init__(self, rental, phone_number):
        super().__init__(rental)
        self.phone_number = phone_number
        self.transaction_code = None

    def _generate_transaction_code(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def process_payment(self):
        if not self._validate_rental():
            return False

        print("Processing M-Pesa payment:")
        self.transaction_code = self._generate_transaction_code()
        print(f"Transaction : {self.transaction_code}")
        print(f"Payment of Ksh {self.amount} successful.")
        return self._finalise()

        

