# SafariDrive Rentals - Car Rental Management System

The project involved using Python to create an object-oriented system for managing a car rental business: a fleet of vehicles, registered customers, rentals from start to return, payments, and a management report.

The requirements for the project are outlined in the LuxDevHQ [github page](https://github.com/LuxDevHQ/LuxDevHQ-Data-Science-Guide/tree/main/Projects/RentFlow%20%E2%80%93%20Car%20Rental%20Management%20System-OOP%20Project).

## Business Rules
The main business rules that are to be implented are: 

| Rule | Detail |
|---|---|
| Economy car | Daily rate x days |
| SUV | Daily rate x days + KSh 2,000 service charge |
| Luxury car | Daily rate x days + 10% insurance |
| Late return | Penalty is 20% of the vehicle's daily rate for each extra day. The service charge and insurance are not applied again. |
| Rental lifecycle | `ACTIVE` -> `COMPLETED`, or `ACTIVE` -> `CANCELLED` |
| Payment | Only a `COMPLETED`, unpaid rental can be paid |

I broke down these business rules into 5 interconnected classes as follows: 

![Rent Flow class diagram](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/csstf97gg1kowox1q65f.png)

## Running the program

Lets explore a quick run of the system to view how it meets the business requirements:

### Registering customers and adding vehicles to the system.

We can start by registering some customers and creating vehicles, across the three vehicle classes, into the system.

![Adding vehicles and customers](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/xe7lejdwbnfkdxhl04li.png)

### Renting a vehicle to a customer

We can view the available vehicles and rent a vehicle to a customer as follows:

```python 
system.show_available_vehicles()
rental1 = system.rent_vehicle(customer1, car2, 4)
```
When we view the available vehicles after the rental, we expect to see one less vehicle in the list as follows:

![available cars](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/b1p0025i7tjwa0w01rrx.png)

If we try to rent the same vehicle to the customer again:


![renting same car](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/9qdlp6v75broht34jfbo.png)

We expect an error to be thrown since the vehicle is no longer available.

```bash
Error: Vehicle KDJ 456B is not available.
```

### Charging customer for rental returned

We can view a scenario where the customer returns the vehicle 2 days later than the period booked. In this instance the customer pays their bill using a card.

The system is able to identify that the vehicle was returned late thus the appropriate fines are added to the final charge. 


![Card payment 2 days late](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/73tue2wdbs1trkrxtamw.png)

### Simulating customer paying with cash

I can illustrate a scenario where another customer pays with cash. In this case the customer hands over too much money thus the need to figure out the change due.


![cash payment](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/yc8aoz2wdq5138xbud8s.png)

### Simulating Mpesa payment

The system also processes payments done through Mpesa by internally creating a code for the payment as follows:


![Mpesa payment](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/ywb370k98cpsgyzk3yfq.png) 

### Simulating a cancelled rental

The system also allows a customer to cancel a rental.
When a customer cancels a rental, the vehicle is cleared to be booked again and the transaction is marked as cancelled.
I can illustrate this scenario as below:


![cancelled rental](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/09hwra2c6y0j5fcs9y60.png)

### Viewing a customer rental history

After simulating a series of rentals, we can view the rental history of each customer as follows:


![customer history](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/nb99i7srb2cwy3i8b2ic.png)

### Viewing the manager level report 

The system finally combines all those records into a simple manager level report:


![manager level report](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/dlj1reoowsuz9gn8liel.png)

The report highlights the number of vehicles currently actively booked, the number of completed rentals and the number of cancelled rentals.

The report also highlights the revenue collected from the completed rentals and any due revenue from a rental where the vehicle has been returned.

## How does this project meet Object-Oriented Principles?

### Encapsulation
I used encapsulation in this project to ensure sensitive data is kept private and can only be changed through controlled methods. 

A vehicle's availability (`__available`) is hidden, so the only way to change it is through `mark_as_rented()` and `mark_as_available()`.

 A rental's payment flag (`__paid`) can only be changed with `mark_as_paid()`, and the system's `__revenue` is exposed through a read-only `revenue` property, so no outside code can change the revenue.

I also used constructors to validate the input (negative daily rates, missing driving licenses and invalid rental days are rejected), so objects can never be created in a broken state.

### Inheritance

I used inheritance in the project to ensure classes that share behaviour inherit it instead of repeating it. `EconomyCar`, `SUV` and `LuxuryCar` all extend `Vehicle`, so they get the registration number, make, model, year, daily rate and availability logic from the parent class `Vehicle`, and only define what makes them different: their pricing.

The parent vehicle class is defined as : 
![parent class](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/5ui21ekb39er0ypmf9ld.png)

The `EconomyCar`, `SUV` and `LuxuryCar` classes inherit from it and define their different `calculate_rental_cost` as follows:

![pricing models](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/lgk5s2shertn7yb9ct3r.png)


In the same way, `MpesaPayment`, `CardPayment` and `CashPayment` extend `Payment`, inheriting the link to the rental, the amount and the shared validation and finalisation steps.

### Polymorphism

The same method call behaves differently depending on the object it is called on. `calculate_rental_cost(days)` returns a different result for an economy car, an SUV and a luxury car, yet `Rental` simply calls `vehicle.calculate_rental_cost(days)` without checking which type it holds. 

Likewise, `process_payment()` generates a transaction code for Mpesa, prints a charge confirmation for a card, and checks the cash handed over and works out change for cash. 


`CarRentalSystem.process_payment()` handles all three with a single line, because every payment type responds to the same call in its own way.


### Abstraction

`Vehicle` and `Payment` are abstract classes. They define *what* every vehicle or payment must be able to do, using `@abstractmethod` for `calculate_rental_cost()` and `process_payment()`, but leave *how* to the subclasses.

The vehicle class defines `calculate_rental_cost` that must be implemented by the `EconomyCar`, `SUV` and `LuxuryCar`classes as follows:

![Vehicle abstraction](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/77bgzg68ri2n97mbco57.png)

The `EconomyCar`, `SUV` and `LuxuryCar` classes implement `calculate_rental_cost` by enforcing their own separate requirements to figure out the `rental_cost` as follows:

![vehicle class abstraction](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/bmbaib9qg3iyoigerkww.png)


The rest of the system (`Rental`, `CarRentalSystem`) depends only on these simple contracts and not on the details of each type. 


## The Real-World Problem this project addresses.

Small and medium car rental businesses often run on notebooks, spreadsheets and memory. That causes problems that cost real money such as :

- **Double bookings.** The same car gets promised to two customers because nobody updated the record.
- **Inconsistent pricing.** Different vehicle types carry different charges (a service fee on SUVs, insurance on luxury cars), and staff calculate them by hand and sometimes get them wrong.
- **Missed late fees and damage charges.** When a car comes back late or damaged, the extra charges are forgotten or worked out differently each time.
- **Messy payments.** Customers pay by Mpesa, card or cash, and each method needs different handling. Cash needs change, and Mpesa needs a transaction reference.
- **No clear picture of the business.** The owner can't easily see which cars are out, who owes money, or how much has actually been earned.

The system replaces that guesswork with one source. A vehicle can only be rented if it is available. Costs, late penalties and damage charges are calculated by the same rules every time. A payment is only recorded when it succeeds, and revenue only grows from successful payments. A single report shows the state of the whole business.


## Running the Project

The project has a set of simple test data in the `main.py` file to test the various scenarios that the system is expected to encounter.
Run the main file through the code: 

```bash
python main.py
```

I also included a file `test.py` file that runs a full set of checks covering vehicles, customers, rentals, payments and the manager class, printing `[PASS]` or `[FAIL]` for each, followed by a sample management report.

To run the test file simply run the code:
```python
python test.py
```