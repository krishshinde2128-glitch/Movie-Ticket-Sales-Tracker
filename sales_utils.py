import csv
import datetime
import matplotlib.pyplot as plt 

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

def plot_revenue_graph():
    revenue_by_show = {}
    try:
        with open('sales.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['status'] == 'Booked':
                    s_id = row['show_id']
                    amount = float(row['total_amount'])
                    
                    if s_id in revenue_by_show:
                        revenue_by_show[s_id] += amount
                    else:
                        revenue_by_show[s_id] = amount
    except FileNotFoundError:
        print("No data to plot.")
        return

    if not revenue_by_show:
        print("No sales found to plot.")
        return

    shows = list(revenue_by_show.keys())      
    earnings = list(revenue_by_show.values()) 

    plt.figure(figsize=(8, 5)) 
    
    plt.bar(shows, earnings, color='skyblue', width=0.5)

    plt.xlabel('Show ID')
    plt.ylabel('Revenue ($)')
    plt.title('Total Revenue per Movie')
    
    for i in range(len(shows)):
        plt.text(i, earnings[i], f"${earnings[i]}", ha='center', va='bottom')

    print("Opening graph window...")
    plt.show()