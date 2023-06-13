import datetime

class Truck:
    def __init__(self, location, current_time, departed_time, packages, capacity, load, mileage):
        self.location = location
        self.departed_time = departed_time
        self.current_time = current_time
        self.total_distance = 0
        self.packages = packages
        self.capacity = capacity
        self.speed = 18
        self.load = load
        self.mileage = mileage


    def __str__(self):
        return f"{self.location}, {self.departed_time}, {self.current_time}, {self.total_distance}, {self.packages}, " \
               f"{self.capacity}, {self.speed}, {self.load}, {self.mileage}"

    def add_truck_time(self, miles):
        self.current_time += datetime.timedelta(hours=miles/self.speed)

