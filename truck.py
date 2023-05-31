class Truck:
    def __init__(self, location, current_time, departed_time):
        self.location = location
        self.departed_time = departed_time
        self.current_time = current_time

    def __str__(self):
        return f"{self.location}, {self.departed_time}, {self.current_time}"
