"""
Test script for the SafariDrive Rentals project.

Run from the folder that holds all the project files:
    python main.py

Each check prints [PASS] or [FAIL]; a summary is shown at the end.
"""
import io
import sys
from contextlib import redirect_stdout

from vehilces import Vehicle, EconomyCar, SUV, LuxuryCar
from customer import Customer
from rentals import Rental, RentalStatus
from payment import Payment, MpesaPayment, CardPayment, CashPayment
from car_rental import CarRentalSysytem

passed = 0
failed = 0


# ---------------------------------------------------------------- helpers
def section(title):
    print(f"\n=== {title} ===")


def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name}")


def expect_error(name, exc_type, func, *args, **kwargs):
    """Passes only if func raises exactly the kind of error we expect."""
    try:
        func(*args, **kwargs)
    except exc_type:
        check(name, True)
    except Exception as e:
        check(f"{name} (wrong error: {type(e).__name__})", False)
    else:
        check(f"{name} (no error raised)", False)


def quiet(func, *args, **kwargs):
    """Run func and capture what it prints. Returns (result, printed_text)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result, buffer.getvalue()


def close(a, b):
    return abs(a - b) < 0.01


def make_fleet():
    return (
        EconomyCar("KDA 111A", "Toyota", "Vitz", 2019, 3000),
        SUV("KDB 222B", "Toyota", "Prado", 2021, 8000),
        LuxuryCar("KDC 333C", "Mercedes", "E-Class", 2022, 20000),
    )


def make_customer(customer_id="C001", name="Amina Otieno"):
    return Customer(customer_id, name, "0712345678", "12345678", "DL-998877")


def make_completed_rental(days=3, actual_days=3, damage=0):
    """A fresh SUV rental that has already been returned (3 days = KSh 26,000)."""
    _, suv, _ = make_fleet()
    rental = Rental("R001", make_customer(), suv, days)
    rental.complete_rental(actual_days, damage)
    return rental


# ---------------------------------------------------------------- vehicles
def test_vehicles():
    section("VEHICLES")
    economy, suv, luxury = make_fleet()

    expect_error("Vehicle is abstract and cannot be created", TypeError,
                 Vehicle, "X", "Make", "Model", 2020, 1000)
    expect_error("negative daily rate rejected", ValueError,
                 EconomyCar, "X", "Make", "Model", 2020, -1)

    check("economy cost = rate x days (3 days = 9000)", close(economy.calculate_rental_cost(3), 9000))
    check("SUV cost adds KSh 2000 service charge (3 days = 26000)", close(suv.calculate_rental_cost(3), 26000))
    check("luxury cost adds 10% insurance (3 days = 66000)", close(luxury.calculate_rental_cost(3), 66000))

    check("vehicle starts available", economy.is_available())
    economy.mark_as_rented()
    check("mark_as_rented makes it unavailable", not economy.is_available())
    economy.mark_as_available()
    check("mark_as_available makes it available again", economy.is_available())

    _, out = quiet(suv.display_details)
    check("display_details shows registration and availability",
          "KDB 222B" in out and "Available : Yes" in out)


# ---------------------------------------------------------------- customer
def test_customer():
    section("CUSTOMER")
    expect_error("empty driving licence rejected", ValueError,
                 Customer, "C001", "Amina", "0712345678", "12345678", "")

    customer = make_customer()
    check("new customer has no rentals", customer.rentals == [])

    _, out = quiet(customer.view_rental_history)
    check("empty history prints a friendly message", "No rentals yet." in out)

    _, suv, _ = make_fleet()
    rental = Rental("R001", customer, suv, 2)
    customer.add_rental(rental)
    check("add_rental stores the rental", customer.rentals == [rental])

    _, out = quiet(customer.view_rental_history)
    check("history prints rental details", "R001" in out and "Prado" in out)

    _, out = quiet(customer.display_details)
    check("display_details shows name and rental count", "Amina Otieno" in out and "Rentals : 1" in out)


# ---------------------------------------------------------------- rental
def test_rental():
    section("RENTAL")
    economy, suv, luxury = make_fleet()
    customer = make_customer()

    # creation
    rental = Rental("R001", customer, suv, 3)
    check("new rental is ACTIVE", rental.status == RentalStatus.ACTIVE)
    check("vehicle is marked rented on creation", not suv.is_available())
    check("base cost comes from the vehicle (26000)", close(rental.base_cost, 26000))
    check("late fee and damage charge start at 0", rental.late_fee == 0 and rental.damage_fee == 0)
    check("actual_days starts as None", rental.actual_days is None)
    check("rental starts unpaid", not rental.is_paid())
    check("total before return equals base cost", close(rental.calculate_total(), 26000))

    expect_error("cannot rent an unavailable vehicle", ValueError, Rental, "R002", customer, suv, 2)
    expect_error("zero rental days rejected", ValueError, Rental, "R003", customer, economy, 0)
    check("failed rental did not lock the vehicle", economy.is_available())

    # invalid returns (rental is still ACTIVE after each failure)
    expect_error("actual days below 1 rejected", ValueError, rental.complete_rental, 0)
    expect_error("negative damage charge rejected", ValueError, rental.complete_rental, 3, -50)
    check("rental still ACTIVE after rejected returns", rental.status == RentalStatus.ACTIVE)

    # on-time return
    rental.complete_rental(3)
    check("on-time return sets status COMPLETED", rental.status == RentalStatus.COMPLETED)
    check("on-time return frees the vehicle", suv.is_available())
    check("on-time return has no late fee", rental.late_fee == 0)
    check("actual days recorded", rental.actual_days == 3)

    expect_error("cannot complete a rental twice", ValueError, rental.complete_rental, 3)
    expect_error("cannot cancel a completed rental", ValueError, rental.cancel_rental)

    # early return
    early = Rental("R004", customer, economy, 5)
    early.complete_rental(3)
    check("early return has no late fee", early.late_fee == 0)
    check("early return keeps the agreed base cost (15000)", close(early.calculate_total(), 15000))

    # late return with damage: SUV rate 8000 -> penalty 1600/day x 2 late days = 3200
    late = Rental("R005", customer, suv, 3)
    late.complete_rental(5, damage_charge=500)
    check("late fee = 20% of daily rate x late days (3200)", close(late.late_fee, 3200))
    check("damage charge recorded", late.damage_fee == 500)
    check("total = base + late + damage (29700)", close(late.calculate_total(), 29700))

    # late fee does NOT include SUV service charge or luxury insurance
    lux_late = Rental("R006", customer, luxury, 2)
    lux_late.complete_rental(3)
    check("late fee ignores luxury insurance (20000 x 20% x 1 = 4000)", close(lux_late.late_fee, 4000))

    # cancellation
    cancel_me = Rental("R007", customer, economy, 2)
    cancel_me.cancel_rental()
    check("cancel sets status CANCELLED", cancel_me.status == RentalStatus.CANCELLED)
    check("cancel frees the vehicle", economy.is_available())
    expect_error("cannot cancel twice", ValueError, cancel_me.cancel_rental)
    expect_error("cannot complete a cancelled rental", ValueError, cancel_me.complete_rental, 2)

    # payment flag
    rental.mark_as_paid()
    check("mark_as_paid / is_paid work together", rental.is_paid())

    # printing
    _, out = quiet(late.display_rental_details)
    check("receipt shows id, status and total", "R005" in out and "COMPLETED" in out and "29700.00" in out)
    check("__str__ gives a readable line", "R005" in str(late) and "COMPLETED" in str(late))


# ---------------------------------------------------------------- payments
def test_payments():
    section("PAYMENTS")
    expect_error("Payment is abstract and cannot be created", TypeError, Payment, make_completed_rental())

    # M-Pesa
    rental = make_completed_rental()
    mpesa = MpesaPayment(rental, "0712345678")
    check("amount is taken from the rental total (26000)", close(mpesa.amount, 26000))
    ok, out = quiet(mpesa.process_payment)
    code = mpesa.transaction_code
    check("M-Pesa payment succeeds", ok is True)
    check("transaction code is 10 uppercase letters/digits",
          code is not None and len(code) == 10 and code.isalnum() and code == code.upper())
    check("M-Pesa output shows the code and amount",
          "Processing M-Pesa payment..." in out and code in out and "26,000" in out)
    check("rental is marked paid after success", rental.is_paid())

    ok, out = quiet(MpesaPayment(rental, "0712345678").process_payment)
    check("paying an already-paid rental fails", ok is False and "already paid" in out)

    # payment on a rental that is not completed
    _, suv, _ = make_fleet()
    active = Rental("R002", make_customer(), suv, 3)
    ok, out = quiet(CardPayment(active, "4417").process_payment)
    check("paying an ACTIVE rental fails", ok is False and "not been completed" in out)
    check("failed payment leaves rental unpaid", not active.is_paid())

    # Card
    rental = make_completed_rental()
    card = CardPayment(rental, "4417")
    ok, out = quiet(card.process_payment)
    check("card payment succeeds", ok is True and rental.is_paid())
    check("card output matches the expected message", "Card ending 4417 charged KSh 26,000" in out)
    check("only the last 4 digits are stored", card.last_digits == "4417" and not hasattr(card, "card_number"))

    expect_error("full card number rejected", ValueError, CardPayment, make_completed_rental(), "4417123412341234")
    expect_error("too few digits rejected", ValueError, CardPayment, make_completed_rental(), "417")
    expect_error("non-digit characters rejected", ValueError, CardPayment, make_completed_rental(), "44a7")

    # Cash
    rental = make_completed_rental()
    cash = CashPayment(rental, 20000)
    ok, out = quiet(cash.process_payment)
    check("cash below the bill fails", ok is False and "short" in out)
    check("failed cash payment leaves rental unpaid", not rental.is_paid())

    ok, out = quiet(CashPayment(rental, 26000).process_payment)
    check("exact cash succeeds with zero change", ok is True and "Change due:    KSh 0" in out)

    rental = make_completed_rental()
    ok, out = quiet(CashPayment(rental, 30000).process_payment)
    check("cash above the bill succeeds", ok is True and rental.is_paid())
    check("cash output shows received amount and change",
          "Cash received: KSh 30,000" in out and "KSh 4,000" in out and "Cash payment of KSh 26,000 recorded." in out)


# ---------------------------------------------------------------- system
def test_system():
    section("CAR RENTAL SYSTEM")
    system = CarRentalSysytem()
    economy, suv, luxury = make_fleet()
    amina = make_customer("C001", "Amina Otieno")
    brian = make_customer("C002", "Brian Mwangi")

    check("system name is SafariDrive Rentals", system.name == "SafariDrive Rentals")

    # fleet and customers
    for vehicle in (economy, suv, luxury):
        system.add_vehicle(vehicle)
    system.register_customer(amina)
    system.register_customer(brian)
    check("3 vehicles and 2 customers registered", len(system.vehicles) == 3 and len(system.customers) == 2)

    expect_error("duplicate vehicle rejected", ValueError, system.add_vehicle, economy)
    expect_error("duplicate customer ID rejected", ValueError, system.register_customer, make_customer("C001"))

    check("find_vehicle returns the vehicle", system.find_vehicle("KDB 222B") is suv)
    check("find_vehicle returns None when missing", system.find_vehicle("NOPE") is None)
    check("find_customer returns the customer", system.find_customer("C002") is brian)
    check("find_customer returns None when missing", system.find_customer("C999") is None)

    # browsing
    available, out = quiet(system.show_available_vehicles)
    check("all 3 vehicles are listed as available", len(available) == 3 and "KDA 111A" in out)

    check("search by class", system.search_vehicles(SUV) == [suv])
    check("search by name string (case-insensitive)", system.search_vehicles("luxurycar") == [luxury])
    check("search by max daily rate", system.search_vehicles(max_daily_rate=5000) == [economy])
    check("search by type and rate together", system.search_vehicles(SUV, 5000) == [])
    check("search with no filters returns all available", len(system.search_vehicles()) == 3)

    # renting
    r1 = system.rent_vehicle(amina, suv, 3)
    check("first rental gets ID R001", r1.rental_id == "R001")
    check("rental stored in the system and in the customer's history",
          r1 in system.rentals and r1 in amina.rentals)
    check("rented vehicle is unavailable", not suv.is_available())

    r2 = system.rent_vehicle(brian, economy, 2)
    check("second rental gets ID R002", r2.rental_id == "R002")

    check("rented vehicles disappear from search", system.search_vehicles(max_daily_rate=5000) == [])
    available, _ = quiet(system.show_available_vehicles)
    check("only the luxury car is still listed", available == [luxury])

    expect_error("unregistered customer cannot rent", ValueError,
                 system.rent_vehicle, make_customer("C999"), luxury, 2)
    expect_error("vehicle outside the fleet cannot be rented", ValueError,
                 system.rent_vehicle, amina, SUV("KDX 999X", "Nissan", "X-Trail", 2020, 7000), 2)
    expect_error("unavailable vehicle cannot be rented", ValueError, system.rent_vehicle, brian, suv, 2)
    expect_error("zero days rejected", ValueError, system.rent_vehicle, amina, luxury, 0)
    check("failed rentals were not recorded", len(system.rentals) == 2)

    # returning
    system.return_vehicle(r1, 5, damage_charge=500)
    check("returned rental is COMPLETED and vehicle freed",
          r1.status == RentalStatus.COMPLETED and suv.is_available())
    check("late return total = 29700", close(r1.calculate_total(), 29700))

    system.return_vehicle(r2, 2)
    check("on-time return total = 6000", close(r2.calculate_total(), 6000))

    outsider = Rental("R999", amina, SUV("KDY 888Y", "Honda", "CR-V", 2020, 7000), 2)
    expect_error("rental from outside the system cannot be returned", ValueError,
                 system.return_vehicle, outsider, 2)

    # payments and revenue
    check("revenue starts at zero", system.revenue == 0)

    ok, _ = quiet(system.process_payment, MpesaPayment(r1, "0712345678"))
    check("M-Pesa payment processed", ok is True and system.revenue == 29700)

    ok, _ = quiet(system.process_payment, CashPayment(r2, 1000))
    check("failed cash payment does not change revenue", ok is False and system.revenue == 29700)

    ok, _ = quiet(system.process_payment, CashPayment(r2, 10000))
    check("successful cash payment adds to revenue", ok is True and system.revenue == 35700)

    ok, _ = quiet(system.process_payment, CardPayment(r1, "4417"))
    check("duplicate payment is rejected and revenue unchanged", ok is False and system.revenue == 35700)

    check("only successful payments are recorded", len(system.payments) == 2)

    expect_error("payment for a foreign rental rejected", ValueError,
                 system.process_payment, MpesaPayment(outsider, "0712345678"))

    def try_to_set_revenue():
        system.revenue = 1

    expect_error("revenue is read-only", AttributeError, try_to_set_revenue)

    # more rentals for the listings and report
    r3 = system.rent_vehicle(amina, luxury, 2)
    system.return_vehicle(r3, 3)                      # late, left unpaid
    check("luxury late rental total = 44000 + 4000 = 48000", close(r3.calculate_total(), 48000))

    r4 = system.rent_vehicle(brian, suv, 4)           # stays active

    r5 = system.rent_vehicle(brian, economy, 1)
    r5.cancel_rental()
    check("cancelled rental frees the vehicle", economy.is_available())

    active, out = quiet(system.show_active_rentals)
    check("show_active_rentals lists only ACTIVE rentals", active == [r4] and "R004" in out)

    completed, out = quiet(system.show_completed_rentals)
    check("show_completed_rentals lists COMPLETED rentals", completed == [r1, r2, r3])

    check("customer history includes every rental",
          len(amina.rentals) == 2 and len(brian.rentals) == 3)

    _, out = quiet(system.generate_report)
    check("report shows name, revenue and outstanding balance",
          "SAFARIDRIVE RENTALS" in out and "35,700" in out and "48,000" in out)
    check("report counts rentals by status",
          "Active          : 1" in out and "Completed       : 3" in out and "Cancelled       : 1" in out)

    return system


# ---------------------------------------------------------------- run all
if __name__ == "__main__":
    test_vehicles()
    test_customer()
    test_rental()
    test_payments()
    system = test_system()

    section("SAMPLE REPORT")
    system.generate_report()

    print(f"\nResults: {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)