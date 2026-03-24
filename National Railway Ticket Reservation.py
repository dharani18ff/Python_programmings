from abc import ABC, abstractmethod
import random
import datetime


# ─── Payment Abstraction ────────────────────────────────────────────────────

class PaymentMethod(ABC):
    def __init__(self, amount: float):
        self.amount = amount

    @abstractmethod
    def process_payment(self):
        pass


class CardPayment(PaymentMethod):
    def __init__(self, amount: float, card_number: str):
        super().__init__(amount)
        self.card_number = card_number

    def process_payment(self):
        print(f"  Processing Card Payment of ₹{self.amount:.2f} using card ending in {self.card_number[-4:]}")


class UPIPayment(PaymentMethod):
    def __init__(self, amount: float, upi_id: str):
        super().__init__(amount)
        self.upi_id = upi_id

    def process_payment(self):
        print(f"  Processing UPI Payment of ₹{self.amount:.2f} via UPI ID: {self.upi_id}")


class NetBankingPayment(PaymentMethod):
    def __init__(self, amount: float, bank_name: str):
        super().__init__(amount)
        self.bank_name = bank_name

    def process_payment(self):
        print(f"  Processing Net Banking Payment of ₹{self.amount:.2f} via {self.bank_name}")


# ─── Core Domain Classes ─────────────────────────────────────────────────────

class Passenger:
    def __init__(self, name: str, age: int, gender: str, id_proof: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.id_proof = id_proof

    def display(self):
        print(f"  Passenger : {self.name} | Age: {self.age} | Gender: {self.gender} | ID: {self.id_proof}")


class Train:
    def __init__(self, train_number: str, train_name: str, source: str,
                 destination: str, departure: str, arrival: str,
                 total_seats: int, fare_per_seat: float):
        self.train_number = train_number
        self.train_name = train_name
        self.source = source
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.fare_per_seat = fare_per_seat

    def display(self):
        print(f"  Train      : [{self.train_number}] {self.train_name}")
        print(f"  Route      : {self.source} → {self.destination}")
        print(f"  Timings    : Dep {self.departure}  |  Arr {self.arrival}")
        print(f"  Fare/Seat  : ₹{self.fare_per_seat:.2f}")
        print(f"  Seats Avail: {self.available_seats}/{self.total_seats}")


class Ticket:
    def __init__(self, passenger: Passenger, train: Train,
                 seat_class: str, seats_booked: int, journey_date: str):
        self.pnr = str(random.randint(1000000000, 9999999999))
        self.passenger = passenger
        self.train = train
        self.seat_class = seat_class
        self.seats_booked = seats_booked
        self.journey_date = journey_date
        self.total_fare = train.fare_per_seat * seats_booked
        self.booking_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "CONFIRMED"

    def display(self):
        print(f"  PNR Number : {self.pnr}")
        print(f"  Status     : {self.status}")
        print(f"  Journey Dt : {self.journey_date}")
        print(f"  Seat Class : {self.seat_class}")
        print(f"  Seats      : {self.seats_booked}")
        print(f"  Total Fare : ₹{self.total_fare:.2f}")
        print(f"  Booked At  : {self.booking_time}")


# ─── Railway Reservation System ──────────────────────────────────────────────

class RailwayReservationSystem:
    def __init__(self):
        self._trains: dict[str, Train] = {}
        self._bookings: dict[str, Ticket] = {}

    # ── Train Management ───────────────────────────────────────
    def add_train(self, train: Train):
        self._trains[train.train_number] = train
        print(f"  ✔ Train '{train.train_name}' ({train.train_number}) added to the system.")

    def show_trains(self):
        if not self._trains:
            print("  No trains available.")
            return
        print(f"  {'No.':<6} {'Train Name':<30} {'Source':<15} {'Destination':<15} "
              f"{'Departure':<12} {'Arrival':<12} {'Avail':<8} {'Fare'}")
        print("  " + "-" * 105)
        for i, t in enumerate(self._trains.values(), 1):
            print(f"  {i:<6} {t.train_name:<30} {t.source:<15} {t.destination:<15} "
                  f"{t.departure:<12} {t.arrival:<12} {t.available_seats:<8} ₹{t.fare_per_seat:.2f}")

    # ── Booking ────────────────────────────────────────────────
    def book_ticket(self, train_number: str, passenger: Passenger,
                    seat_class: str, seats_requested: int,
                    journey_date: str, payment: PaymentMethod) -> Ticket | None:
        train = self._trains.get(train_number)
        if not train:
            print(f"  ✘ Train {train_number} not found.")
            return None
        if train.available_seats < seats_requested:
            print(f"  ✘ Only {train.available_seats} seat(s) available. Cannot book {seats_requested}.")
            return None

        print(f"  Initiating payment...")
        payment.process_payment()

        train.available_seats -= seats_requested
        ticket = Ticket(passenger, train, seat_class, seats_requested, journey_date)
        self._bookings[ticket.pnr] = ticket
        print(f"  ✔ Ticket booked successfully! PNR: {ticket.pnr}")
        return ticket

    # ── Cancellation ───────────────────────────────────────────
    def cancel_ticket(self, pnr: str) -> bool:
        ticket = self._bookings.get(pnr)
        if not ticket:
            print(f"  ✘ PNR {pnr} not found.")
            return False
        if ticket.status == "CANCELLED":
            print(f"  ✘ Ticket {pnr} is already cancelled.")
            return False

        ticket.train.available_seats += ticket.seats_booked
        ticket.status = "CANCELLED"
        refund = ticket.total_fare * 0.80
        print(f"  ✔ Ticket {pnr} cancelled. Refund of ₹{refund:.2f} will be processed.")
        return True

    # ── PNR Status ─────────────────────────────────────────────
    def check_pnr_status(self, pnr: str):
        ticket = self._bookings.get(pnr)
        if not ticket:
            print(f"  ✘ PNR {pnr} not found.")
            return
        print(f"\n  ── PNR Status ──────────────────────────────")
        ticket.display()
        print(f"  ── Passenger Info ──────────────────────────")
        ticket.passenger.display()
        print(f"  ── Train Info ──────────────────────────────")
        ticket.train.display()

    # ── View All Bookings ──────────────────────────────────────
    def show_all_bookings(self):
        if not self._bookings:
            print("  No bookings found.")
            return
        print(f"  {'PNR':<14} {'Passenger':<20} {'Train':<30} {'Date':<14} {'Seats':<8} {'Fare':<12} Status")
        print("  " + "-" * 110)
        for ticket in self._bookings.values():
            print(f"  {ticket.pnr:<14} {ticket.passenger.name:<20} "
                  f"{ticket.train.train_name:<30} {ticket.journey_date:<14} "
                  f"{ticket.seats_booked:<8} ₹{ticket.total_fare:<10.2f} {ticket.status}")


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    system = RailwayReservationSystem()

    print("\n" + "=" * 60)
    print("   NATIONAL RAILWAY TICKET RESERVATION SYSTEM")
    print("=" * 60)

    # ── Add trains ────────────────────────────────────────────
    print("\n[1] Adding Trains to the System")
    print("-" * 60)
    system.add_train(Train("12001", "Shatabdi Express",   "Chennai",  "Bangalore", "06:00", "10:30", 100, 550.00))
    system.add_train(Train("12951", "Rajdhani Express",   "Mumbai",   "Delhi",     "17:00", "08:35", 150, 1200.00))
    system.add_train(Train("11078", "Jhelum Express",     "Pune",     "Jammu",     "11:30", "09:45", 80,  850.00))
    system.add_train(Train("22691", "Rajdhani SF Express","Bangalore","Delhi",     "20:00", "23:45", 120, 1400.00))

    # ── Display available trains ───────────────────────────────
    print("\n[2] Available Trains")
    print("-" * 60)
    system.show_trains()

    # ── Booking 1 – Card Payment ───────────────────────────────
    print("\n[3] Booking Ticket — Passenger: Dharani")
    print("-" * 60)
    passenger1 = Passenger("Dharani", 25, "Male", "AADHAAR-1234")
    payment1 = CardPayment(1100.00, "1234567890123456")
    ticket1 = system.book_ticket(
        train_number="12001",
        passenger=passenger1,
        seat_class="AC 2-Tier",
        seats_requested=2,
        journey_date="2026-04-10",
        payment=payment1
    )

    # ── Booking 2 – UPI Payment ────────────────────────────────
    print("\n[4] Booking Ticket — Passenger: Priya")
    print("-" * 60)
    passenger2 = Passenger("Priya", 30, "Female", "PAN-ABCDE1234F")
    payment2 = UPIPayment(1200.00, "priya@upi")
    ticket2 = system.book_ticket(
        train_number="12951",
        passenger=passenger2,
        seat_class="Sleeper",
        seats_requested=1,
        journey_date="2026-04-15",
        payment=payment2
    )

    # ── Booking 3 – Net Banking ────────────────────────────────
    print("\n[5] Booking Ticket — Passenger: Ravi")
    print("-" * 60)
    passenger3 = Passenger("Ravi", 45, "Male", "AADHAAR-5678")
    payment3 = NetBankingPayment(2800.00, "State Bank of India")
    ticket3 = system.book_ticket(
        train_number="22691",
        passenger=passenger3,
        seat_class="AC 1-Tier",
        seats_requested=2,
        journey_date="2026-04-20",
        payment=payment3
    )

    # ── PNR Status Check ───────────────────────────────────────
    if ticket1:
        print(f"\n[6] PNR Status Check — PNR: {ticket1.pnr}")
        print("-" * 60)
        system.check_pnr_status(ticket1.pnr)

    # ── All Bookings ───────────────────────────────────────────
    print("\n[7] All Current Bookings")
    print("-" * 60)
    system.show_all_bookings()

    # ── Cancel a Ticket ────────────────────────────────────────
    if ticket2:
        print(f"\n[8] Cancelling Ticket — PNR: {ticket2.pnr}")
        print("-" * 60)
        system.cancel_ticket(ticket2.pnr)

    # ── Updated Bookings After Cancellation ───────────────────
    print("\n[9] All Bookings After Cancellation")
    print("-" * 60)
    system.show_all_bookings()

    # ── Invalid Booking Attempt ────────────────────────────────
    print("\n[10] Attempting to book on a non-existent train")
    print("-" * 60)
    system.book_ticket(
        train_number="99999",
        passenger=passenger1,
        seat_class="Sleeper",
        seats_requested=1,
        journey_date="2026-04-25",
        payment=UPIPayment(850.00, "dharani@upi")
    )

    # ── Updated Available Seats ────────────────────────────────
    print("\n[11] Updated Train Availability")
    print("-" * 60)
    system.show_trains()

    print("\n" + "=" * 60)
    print("   Reservation session complete. Thank you!")
    print("=" * 60 + "\n")
