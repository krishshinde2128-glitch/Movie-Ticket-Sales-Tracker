class Ticket:
    def __init__(self, transaction_id, show_id, seats_booked, total_amount, status="Booked"):
        self.transaction_id = transaction_id
        self.show_id = show_id
        self.seats_booked = int(seats_booked)
        self.total_amount = float(total_amount)
        self.status = status  

    def cancel(self):
        self.status = "Cancelled"
        print(f"Transaction {self.transaction_id} has been cancelled.")

    def __str__(self):
        return f"Ticket #{self.transaction_id} | Show ID: {self.show_id} | Seats: {self.seats_booked} | Status: {self.status}"

