import csv
import hash_table
import package
import truck
import datetime
from dateutil.parser import parse


PACKAGE_PATH = 'resources/WGUPS Package File.csv'
DISTANCE_PATH = 'resources/WGUPS Distance Table.csv'


def main_logic():
    def create_address_list():
        with open(DISTANCE_PATH, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        for row in data:
            if row and row[0] == "DISTANCE BETWEEN HUBS IN MILES":
                hub_addresses = row[2:]
                return hub_addresses

    def create_distance_list():
        with open(DISTANCE_PATH, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            data = list(reader)

        hub_distances = []

        for row in data:
            hub_distances.append(row[2:])

        return hub_distances

    def create_package_hash():
        package_info = hash_table.HashMap(40)

        with open(PACKAGE_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                new_package = package.Package(row[0], row[1], row[2], row[4], row[5], row[6], row[7], "At hub", None)
                package_info.put(row[0], new_package)

        return package_info

    def get_address_index(address):
        hub_addresses = create_address_list()
        for index, hub_addresses in enumerate(hub_addresses):
            if address in hub_addresses:
                return index

    def get_distance_between_addresses(address_x, address_y):
        hub_distances = create_distance_list()
        exact_distance = hub_distances[address_x][address_y]
        if exact_distance == "":
            exact_distance = hub_distances[address_y][address_x]
        return float(exact_distance)

    package_info_hash = create_package_hash()
    truck_one_package_ids = ["13", "14", "15", "16", "19", "20", "29", "30", "40", "5", "7", "8", "9", "10", "11", "12"]
    truck_two_package_ids = ["3", "36", "38", "1", "31", "34", "37", "2", "4", "17", "18", "21", "22", "23", "24"]
    truck_three_package_ids = ["6", "9", "25", "28", "32", "26", "27", "33", "39"]

    start_time = datetime.timedelta(hours=8)

    truck_one = truck.Truck("", start_time, "", truck_one_package_ids, "", 0.0, 0.0)
    truck_two = truck.Truck("", start_time, "", truck_two_package_ids, "", 0.0, 0.0)
    truck_three = truck.Truck("", None, "", truck_three_package_ids, "", 0.0, 0.0)

    def deliver_packages(truck):
        # List of packages to be sorted using the nearest neighbor algorithm
        undelivered_packages = []
        # Takes all packages from the truck and places it in the undelivered_package list to be sorted
        # O(n) operation
        for package_id in truck.packages:
            package = package_info_hash.get(package_id)
            undelivered_packages.append(package)
            truck.load += float(package.mass)

        # Clears out the Truck's packages property
        truck.packages.clear()
        amount_of_undelivered_packages = len(undelivered_packages)

        # Loops until all undelivered_packages are sorted
        while amount_of_undelivered_packages > 0:
            next_address_distance = 100
            next_package = None

            for package in undelivered_packages:
                truck_address_index = get_address_index(truck.location)
                package_address_index = get_address_index(package.address)
                distance_between = get_distance_between_addresses(truck_address_index, package_address_index)
                if distance_between <= next_address_distance:
                    next_address_distance = distance_between
                    next_package = package

            truck.packages.append(next_package.package_id)
            undelivered_packages.remove(next_package)
            amount_of_undelivered_packages = len(undelivered_packages)
            truck.mileage += next_address_distance
            truck.location = next_package.address
            truck.add_truck_time(next_address_distance)
            next_package.delivery_time = truck.current_time

    deliver_packages(truck_one)
    deliver_packages(truck_two)
    truck_three_start_time = min(truck_one.current_time, truck_two.current_time)
    truck_three.current_time = truck_three_start_time
    deliver_packages(truck_three)
    total_mileage = truck_one.mileage + truck_two.mileage + truck_three.mileage
    print(total_mileage)

    def check_packages(truck):
        for package in truck.packages:
            content = package_info_hash.get(package)
            if content.delivery_deadline != "EOD":
                time_obj = parse(content.delivery_deadline)
                time_components = time_obj.time()
                timedelta_obj = datetime.timedelta(hours=time_components.hour, minutes=time_components.minute,
                                          seconds=time_components.second)
                if timedelta_obj >= content.delivery_time:
                    print("Pass")
                else:
                    print("Fail")
                    print(content)

    print("--Truck1--")
    check_packages(truck_one)
    print("--Truck2--")
    check_packages(truck_two)
    print("--Truck3--")
    check_packages(truck_three)


def start_program():
    print("╔═════════════════════════════════════════════╗")
    print("║                    WGUPS                    ║")
    print("║                                             ║")
    print("║ Western Governors University Parcel Service ║")
    print("║                                             ║")
    print("╚═════════════════════════════════════════════╝")

    options = ["Check status of One Package", "Check status of All Packages", "Option 3"]

    print("Please select an option:")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    selected_option = input("Enter the number corresponding to your choice: ")

    if selected_option == "1" or selected_option == "2":
        time = input("Enter a time with format (HH:MM:SS) :")


if __name__ == "__main__":
    # start_program()
    main_logic()
