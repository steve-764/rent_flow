from rentals import Rental, RentalStatus


class CarRentalSysytem():
    def __init__(self):
        self.name = "SafariDrive Rentals"
        self.vehicles = []
        self.customers = []
        self.rentals = []
        self.payments = []
        self.__revenue = 0


def add_vehicle(self, vehicle):
    if self.find_vehicle(vehicle.registration_number):
        raise ValueError(f"Vehicle {vehicle.registration_number} already in the sysytem.")
    self.vehicles.append(vehicle)

def find_vehicle(self, registration_number):
    for vehicle in self.vehicles:
        if vehicle.registration_number == registration_number:
            return vehicle
        return None


def register_customer(self, customer):
    if self.find_customer(customer.customer_id):
        raise ValueError(f"Customer {customer.customer_id} already in the system.")
    self.customers.append(customer)

def find_customer(self, customer_id):
    for customer in self.customers:
        if customer.customer_id == customer_id:
            return customer
        return None


def search_vehicles(self, vehicle_type = None, max_daily_rate = None):
    results = []
    for v in self.vehicles:
        if not v.is_available():
            continue
        if vehicle_type is not None:
            if isinstance(vehicle_type, str):
                if type(v).__name__.lower() != vehicle_type.lower():
                    continue
            elif not isinstance(v, vehicle_type):
                continue
        if max_daily_rate is not None and v.daily_rate > max_daily_rate:
            continue
        results.append(v)
    return results



def rent_vehicle(self, customer, vehicle, days):
    if customer not in self.customers:
        raise ValueError("Customer is not registered.")
    if vehicle not in self.vehicles:
        raise ValueError("Vehicle not in fleet")
    if not vehicle.is_available():
        raise ValueError(f"Vehicle {vehicle.registration_number} is not available.")
    if days < 1:
        raise ValueError("Vehicle must be rented for atleast 1 day.")


    rental_id = f"R{len(self.rentals) + 1}"
    rental = Rental(rental_id, customer, vehicle, days)
    self.rentals.append(rental)
    customer.add_rental(rental)
    return rental



def return_vehicle(self, rental, actual_days, damage_charge = 0):
    if rental not in self.rentals:
        raise ValueError("Rental not in the system")
    rental.complete_rental(actual_days, damage_charge)
    return rental



def process_payment(self, payment):
    if payment.rental not in self.rentals:
        raise ValueError("Payment cannot be made for a vehicle that is not rented.")

    if payment.process_payment():
        self.payment.append(payment)
        self.__revenue += payment.amount
        return True
    return False


@property
def revenue(self):
    return self.__revenue


def _show_rentals(self, status, title):
    matching = [r for r in self.rentals if r.status == status]
    print(f"--- {title} ({len(matching)}) ---")
    if not matching:
        print("None.")
    for r in matching:
        print(f"{r.rental_id}   |   {r.customer_name} "
              f"{r.vehicle.registration_number}   |    {r.rental_days} days")
    return matching


def show_active_rentals(self):
    return self._show_rentals(RentalStatus.ACTIVE, "Active rentals")


def show_completed_rentals(self):
    return self._show_rentals(RentalStatus.COMPLETED, "Completed rentals")



def generate_report(self):
        active = [r for r in self.rentals if r.status == RentalStatus.ACTIVE]
        completed = [r for r in self.rentals if r.status == RentalStatus.COMPLETED]
        cancelled = [r for r in self.rentals if r.status == RentalStatus.CANCELLED]
        unpaid = [r for r in completed if not r.is_paid()]
        outstanding = sum(r.calculate_total() for r in unpaid)
        available = sum(1 for v in self.vehicles if v.is_available())

        print("=" * 40)
        print(f"{self.name.upper()} - MANAGEMENT REPORT")
        print("=" * 40)
        print(f"Vehicles in fleet : {len(self.vehicles)} ({available} available)")
        print(f"Customers         : {len(self.customers)}")
        print(f"Rentals           : {len(self.rentals)} total")
        print(f"  Active          : {len(active)}")
        print(f"  Completed       : {len(completed)}")
        print(f"  Cancelled       : {len(cancelled)}")
        print(f"Payments received : {len(self.payments)}")
        print(f"Total revenue     : KSh {self.revenue:,.0f}")
        print(f"Unpaid completed  : {len(unpaid)} rentals (KSh {outstanding:,.0f} outstanding)")
        print("=" * 40)

    