import csv

class Show:
    def __init__(self, show_id, movie_name, time, screen_no, total_seats, price):
        
        self.show_id = show_id
        self.movie_name = movie_name
        self.time = time
        self.screen_no = screen_no
        self.total_seats = int(total_seats) 
        self.price = int(price)

    def __str__(self):
        return f"[{self.show_id}] {self.movie_name} | Time: {self.time} | Total Seats: {self.total_seats} | Price: {self.price}"

    @staticmethod
    def load_shows(file):
        all_shows = [] 
        try:
            with open(file, mode='r') as file:
                reader = csv.DictReader(file) 
                for row in reader:
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
            print(f"Error: The file {file} was not found.")  
        return all_shows

