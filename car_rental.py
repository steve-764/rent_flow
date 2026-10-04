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
    for vehicle in self.vehicles:
        if not vehicle.is_available():
            continue
        if vehicle_type is not None:
            if isinstance(vehicle_type, str):
                if type(vehicle).__name__.lower() != vehicle_type.lower():
                    continue
            elif not isinstance(vehicle, vehicle_type):
                continue
        if max_daily_rate is not None and vehicle.daily_rate > max_daily_rate:
            continue
        results.append(vehicle)
    return results


    