import csv
import datetime

def log_event(func):
    def log(*args, **kwargs):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG {now}] Executing: {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"[LOG] Finished: {func.__name__}")
        return result
    return log

def generate_transaction_id():
    return "TIC" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
def save_transaction(transaction_id, show_id, seats, amount, status="Booked"):
    with open('sales.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaction_id, show_id, seats, amount, status])

def update_transaction_status(transaction_id, new_status):
    rows = []
    found = False
    with open('sales.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == transaction_id: 
                row[4] = new_status 
                found = True
            rows.append(row)
    if found:
        with open('sales.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return True
    return False