import csv
from show_class import Show
from ticket_class import Ticket
import sales_utils


shows_list = Show.load_shows('shows.csv')

def get_booked_seats_count(show_id):
    count = 0
    try:
        with open('sales.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['show_id'] == show_id and row['status'] == 'Booked':
                    count += int(row['seats_booked'])
    except FileNotFoundError:
        return 0 
    return count

def view_shows():
    print("\n") 
    print(f"{'ID':<6} {'Movie Name':<25} {'Time':<10} {'Seats':<10} {'Price':<6}")
    
    for s in shows_list:
        taken = get_booked_seats_count(s.show_id)
        available = s.total_seats - taken
        print(f"{s.show_id:<6} {s.movie_name:<25} {s.time:<10} {available}/{s.total_seats:<9} {s.price:<6}")
    print()

@sales_utils.log_event
def book_ticket():
    view_shows()
    try:
        s_id = input("\nEnter Show ID to book: ")

        selected_show = None
        for s in shows_list:
            if s.show_id == s_id:
                selected_show = s
                break
        if selected_show:
            taken = get_booked_seats_count(s_id)
            available = selected_show.total_seats - taken

            if available == 0:
                print("Sorry! This show is SOLD OUT.")
                return
            seats = int(input(f"Enter number of seats (Max {available}): "))
            
            if seats <= 0:
                print("Error: Number of seats must be positive.")
                return
            
            if seats > available:
                print(f"Error: Only {available} seats are available.")
                return
    
            calc_cost = lambda price, count: price * count
            total_cost = calc_cost(selected_show.price, seats)
            
            TIC_id = sales_utils.generate_transaction_id()
            new_ticket = Ticket(TIC_id, s_id, seats, total_cost)
            
            sales_utils.save_transaction(TIC_id, s_id, seats, total_cost)
            
            print(f"\nSUCCESS! Ticket Booked.")
            print(new_ticket)
        else:
            print("Error: Show ID not found.")
            
    except ValueError:
        print("Error: Please enter valid numbers.")

@sales_utils.log_event
def cancel_ticket():
    TIC_id = input("\nEnter Transaction ID to cancel (without the #): ")
    success = sales_utils.update_transaction_status(TIC_id, "Cancelled")
    if success:
        print("Success: Ticket has been cancelled.")
    else:
        print("Error: Transaction ID not found.")

def analyze_data():
    print("\n SALES REPORT ")
    total_revenue = 0.0
    revenue_by_show = {} 
    
    try:
        with open('sales.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['status'] == 'Booked':
                    amount = float(row['total_amount'])
                    s_id = row['show_id']
                    total_revenue += amount
                    if s_id in revenue_by_show:
                        revenue_by_show[s_id] += amount
                    else:
                        revenue_by_show[s_id] = amount
        
        print(f"TOTAL REVENUE COLLECTED: ${total_revenue}")
        print("\n Revenue Breakdown by Show ID:")
        if not revenue_by_show:
            print("No sales data available yet.")
        else:
            for s_id, revenue in revenue_by_show.items():
                print(f"Show ID {s_id}: ${revenue}\n")           
    except FileNotFoundError:
        print("Error: No sales data found.")

def main():
    while True:
        print("MOVIE TICKET SYSTEM ")
        print("1. View Shows")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. Analyze Data (Report)")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            view_shows()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            cancel_ticket()
        elif choice == '4':
            analyze_data()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()