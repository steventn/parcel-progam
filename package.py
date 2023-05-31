class Package:
    def __init__(self, package_id, address, city, zip_code, delivery_deadline, mass, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.special_notes = special_notes

    def __str__(self):
        return f"{self.package_id}, {self.address}, {self.city}, {self.zip_code}, {self.delivery_deadline}, {self.mass}, {self.special_notes}"
