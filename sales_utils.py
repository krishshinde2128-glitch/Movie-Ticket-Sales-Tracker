import csv
import datetime

# --- 1. The Decorator (Requirement: "Decorator for automatic logging") ---
def log_event(func):
    """
    This is a Decorator. It acts like a wrapper around other functions.
    Whenever a function with @log_event is called, this code runs first
    to print a log message with the current time.
    """
    def wrapper(*args, **kwargs):
        # Get the current time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {now}] Executing: {func.__name__}...")
        
        # Run the actual function
        result = func(*args, **kwargs)
        
        print(f"[LOG] Finished: {func.__name__}")
        return result
    return wrapper

# --- 2. Helper to Generate Unique IDs ---
def generate_transaction_id():
    """
    Creates a unique ID based on the current timestamp.
    Example: TXN202312091030
    """
    return "TXN" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# --- 3. Save to CSV ---
def save_transaction(transaction_id, show_id, seats, amount, status="Booked"):
    """
    Appends a new transaction row to 'sales.csv'.
    """
    with open('sales.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaction_id, show_id, seats, amount, status])

# --- 4. Update CSV (For Cancellations) ---
def update_transaction_status(transaction_id, new_status):
    """
    Reads all sales, finds the matching ID, updates it, and re-saves the file.
    This is necessary because we can't easily 'edit' a text file line in place.
    """
    rows = []
    found = False
    
    # Read all existing data
    with open('sales.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == transaction_id: # match ID
                row[4] = new_status # Update status column
                found = True
            rows.append(row)
            
    # Write everything back if we found it
    if found:
        with open('sales.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return True
    return False