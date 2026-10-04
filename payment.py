import random
import string
from abc import ABC, abstractmethod
from rentals import RentalStatus

class Payment(ABC):
    def __init__(self, rental):
        self.rental = rental
        self.amount = rental.calculate_total()

    @abstractmethod
    def process_payment(self):
        pass


    def _validate_rental(self):
        if self.rental.status != RentalStatus.COMPLETED:
            print("Payment Failed. Rental not competed.")
            return False
        if self.rental.is_paid():
            print("Payment Failed: Rental is already paid.")
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


class CardPayment(Payment):
    def __init__(self, rental, last_digits):
        super().__init__(rental)
        last_digits = str(last_digits)
        if len(last_digits) != 4 or not last_digits.isdigit():
            raise ValueError("Provide 4 digits of the card!")
        self.last_digits = last_digits

    def process_payment(self):
        if not self._validate_rental():
            return False

        print(f"Card ending {self.last_digits} charged Ksh {self.amount}")
        return self._finalise()


class CashPayment(Payment):
    def __init__(self, rental, amount_paid):
        super().__init__(rental)
        self.amount_paid = amount_paid

    def process_payment(self):
        if not self._validate_rental():
            return False

        if self.amount_paid < self.amount:
            deficit = self.amount - self.amount_paid
            print(f"Payment Failed: Cash deficit of Ksh {deficit}.")
            return False

        change = self.amount_paid - self.amount
        print(f"Cash received : Ksh {self.amount_paid}")
        print(f"Change due: Ksh {change}")
        print(f"Cash payment of Ksh {self.amount} received.")
        return self._finalise()

