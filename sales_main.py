import csv  # We use the built-in CSV module instead of Pandas
from show_class import Show
from ticket_class import Ticket
import sales_utils

# --- 1. Load Data ---
shows_list = Show.load_shows('shows.csv')

def view_shows():
    print("\n--- Available Shows ---")
    # REQUIREMENT: "List comprehensions for show filtering"
    display_lines = [str(s) for s in shows_list]
    for line in display_lines:
        print(line)

@sales_utils.log_event
def book_ticket():
    view_shows()
    try:
        s_id = input("\nEnter Show ID to book: ")
        seats = int(input("Enter number of seats: "))
        
        selected_show = None
        for s in shows_list:
            if s.show_id == s_id:
                selected_show = s
                break
        
        if selected_show:
            # REQUIREMENT: "Lambda to calculate revenue instantly"
            calc_cost = lambda price, count: price * count
            total_cost = calc_cost(selected_show.price, seats)
            
            txn_id = sales_utils.generate_transaction_id()
            new_ticket = Ticket(txn_id, s_id, seats, total_cost)
            
            sales_utils.save_transaction(txn_id, s_id, seats, total_cost)
            
            print(f"\nSUCCESS! Ticket Booked.")
            print(new_ticket)
        else:
            print("Error: Show ID not found.")
            
    except ValueError:
        print("Error: Please enter valid numbers for seats.")

@sales_utils.log_event
def cancel_ticket():
    txn_id = input("\nEnter Transaction ID to cancel: ")
    success = sales_utils.update_transaction_status(txn_id, "Cancelled")
    
    if success:
        print("Success: Ticket has been cancelled.")
    else:
        print("Error: Transaction ID not found.")

def analyze_data():
    """
    Analyzes sales using standard Python (No Pandas/Matplotlib).
    """
    print("\n--- SALES REPORT ---")
    
    total_revenue = 0.0
    revenue_by_show = {} # Dictionary to store revenue per show
    
    try:
        with open('sales.csv', mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Only count active bookings
                if row['status'] == 'Booked':
                    amount = float(row['total_amount'])
                    s_id = row['show_id']
                    
                    # 1. Add to total global revenue
                    total_revenue += amount
                    
                    # 2. Add to specific show revenue
                    if s_id in revenue_by_show:
                        revenue_by_show[s_id] += amount
                    else:
                        revenue_by_show[s_id] = amount
        
        # --- Print the Text Report ---
        print(f"TOTAL REVENUE COLLECTED: ${total_revenue}")
        print("\n--- Revenue Breakdown by Show ---")
        
        if not revenue_by_show:
            print("No sales data available yet.")
        else:
            for s_id, revenue in revenue_by_show.items():
                print(f"Show ID {s_id}: ${revenue}")
                
    except FileNotFoundError:
        print("Error: No sales data found (sales.csv missing).")

# --- Main Menu Loop ---
def main():
    while True:
        print("\n=== MOVIE TICKET SYSTEM ===")
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