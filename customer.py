class Customer():
    def __init__(self, customer_id, name, phone_number, national_id, driving_licence):
        if not driving_licence:
            raise ValueError("You must enter a driving licence number.")

        self.customer_id = customer_id
        self.name = name
        self.phone_number = phone_number
        self.national_id = national_id
        self.driving_licence = driving_licence
        self.rentals = []

    def display_details(self):
        print(f"Customer ID : {self.customer_id}")
        print(f"Name : {self.name}")
        print(f"Phone number : {self.phone_number}")
        print(f"National ID : {self.national_id}")
        print(f"Driving licence : {self.driving_licence}")
        print(f"Rentals : {len(self.rentals)}")

    def add_rental(self, rental):
        self.rentals.append(rental)

    def view_rental_history(self):
        if not self.rentals:
            print("No rentals yet.")
            return
        print(f"=== {self.name} Rental History  ===")
        for rental in self.rentals:
            print(rental)