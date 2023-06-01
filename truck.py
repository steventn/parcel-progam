class Truck:
    def __init__(self, location, current_time, departed_time, packages, capacity, speed, load, mileage):
        self.location = location
        self.departed_time = departed_time
        self.current_time = current_time
        self.total_distance = 0
        self.packages = packages
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.mileage = mileage


    def __str__(self):
        return f"{self.location}, {self.departed_time}, {self.current_time}"
