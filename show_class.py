import csv

class Show:
    def __init__(self, show_id, movie_name, time, screen_no, total_seats, price):
        
        self.show_id = show_id
        self.movie_name = movie_name
        self.time = time
        self.screen_no = screen_no
        # Convert numeric values from strings to integers for math later
        self.total_seats = int(total_seats) 
        self.price = int(price)

    def __str__(self):
        
        return f"[{self.show_id}] {self.movie_name} | Time: {self.time} | Total Seats: {self.total_seats} | Price: {self.price}"

    @staticmethod
    def load_shows(filename):
        
        all_shows = [] 
        
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file) # Reads rows as dictionaries
                
                for row in reader:
                    # Create a Show object for each row in the CSV
                    new_show = Show(
                        row['show_id'], 
                        row['movie_name'], 
                        row['time'], 
                        row['screen_no'], 
                        row['total_seats'], 
                        row['price']
                    )
                    all_shows.append(new_show)
                    
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
            
        return all_shows

