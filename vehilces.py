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

    def display_details(self):
        print(f"Reg Number : {self.registration_number}")
        print(f"Make : {self.make}")
        print(f"Model : {self.model}")
        print(f"Year : {self.year}")
        print(f"Daily rate : {self.daily_rate}")
        print(f"Available : {self.__available}")


    @abstractmethod
    def calculate_rental_cost(self, days):
        pass


class EconomyCar(Vehicle):
    def __init__(self, registration_number, make, model, year, daily_rate):
        super().__init__(registration_number, make, model, year, daily_rate)

    def calculate_rental_cost(self, days):
        return self.daily_rate * days


class SUV(Vehicle):
    def __init__(self, registration_number, make, model, year, daily_rate):
        super().__init__(registration_number, make, model, year, daily_rate)

    # suv has ksh 2000 service charge added
    def calculate_rental_cost(self, days):
        return (self.daily_rate * days) + 2000


class LuxuryCar(Vehicle):
    def __init__(self, registration_number, make, model, year, daily_rate):
        super().__init__(registration_number, make, model, year, daily_rate)

    # luxury cars have a 10% insurance charge of total rent cost
    def calculate_rental_cost(self, days):
        return (self.daily_rate * days) + ((self.daily_rate * days) * 0.1)


# test 
car1= EconomyCar("KDK 123A", "Toyota", "Axio", 2022, 3000)
car2 = SUV("KBG 222B", "Toyota", "Prado", 2022, 8000)
car3 = LuxuryCar("KGD 678C", "Mercedes", "E-Class", 2022, 15000)

car1.display_details()

# print(car1.calculate_rental_cost(3))
# print(car2.calculate_rental_cost(3))
# print(car3.calculate_rental_cost(3))