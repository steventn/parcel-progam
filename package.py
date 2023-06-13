import csv
import hash_table

class Package:
    def __init__(self, package_id, address, city, zip_code, delivery_deadline, mass, special_notes, delivery_status,
                 departure_time, delivery_time):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.departure_time = departure_time
        self.delivery_time = delivery_time

    def __str__(self):
        return f"{self.package_id}, {self.address}, {self.city}, {self.zip_code}, {self.delivery_deadline}, " \
               f"{self.mass}, {self.special_notes}, {self.delivery_status}, {self.delivery_time}, {self.departure_time}"