from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, registration_number, make, model, year, daily_rate):
        if daily_rate < 0:
            raise ValueError("Daily rate cannot be negative.")

        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.__available = True          # private

    def is_available(self):
        return self.__available

    def mark_as_rented(self):
        self.__available = False

    def mark_as_available(self):
        self.__available = True

    @abstractmethod
    def calculate_rental_cost(self, days):
        pass


class economyCar(Vehicle):
    def calculate_rental_cost(self, days):
        return self.daily_rate * days


class suv(Vehicle):
    def calculate_rental_cost(self, days):
        return (self.daily_rate * days) + 2000

class luxuryCar(Vehicle):
    def calculate_rental_cost(self, days):
        return (self.daily_rate * days) + ((self.daily_rate * days) * 0.1)

car1= luxuryCar("KDK 123A", "Toyota", "Axio", 2022, 15000)

print(car1.calculate_rental_cost(3))