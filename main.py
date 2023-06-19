# Steven Nguyen, ID #010596963

import csv
from datetime import datetime, time
from hash_table import HashMap
from package import Package
from truck import Truck


PACKAGE_PATH = 'resources/WGUPS Package File.csv'
DISTANCE_PATH = 'resources/WGUPS Distance Table.csv'


# Creates a new list with just address information
# Time complexity: O(N)
# Space complexity: O(1)
def create_address_list(distance_data):
    for row in distance_data:
        if row and row[0] == "DISTANCE BETWEEN HUBS IN MILES":
            return row[2:]


# Creates a new list with just distance between addresses information
# Time complexity: O(N)
# Space complexity: O(N)
def create_distance_list(distance_data):
    hub_distances = []

    for row in distance_data[1:]:
        hub_distances.append(row[2:])

    return hub_distances


# Creates a hash map with package ID as the key and the package object as the value
# Time complexity: O(N)
# Space complexity: O(N)
def create_package_hash(package_data):
    package_info = HashMap(40)
    for row in package_data:
        new_package = Package(row[0], row[1], row[2], row[4], row[5], row[6], row[7], "At hub", None)
        package_info.put(row[0], new_package)
    return package_info


# Returns the index of an address in the address list
# Time complexity: O(N)
# Space complexity: O(1)
def get_address_index(address, hub_addresses):
    for index, hub_address in enumerate(hub_addresses):
        if address in hub_address:
            return index


# Returns the distance of two address indexes
# Time complexity: O(1)
# Space complexity: O(1)
def get_distance_between_addresses(address_x, address_y, hub_distances):
    exact_distance = hub_distances[address_x][address_y]
    if exact_distance == "":
        exact_distance = hub_distances[address_y][address_x]
    return float(exact_distance)


# List of packages to be sorted using the nearest neighbor algorithm
# Time complexity: O(N^2)
# Space complexity: O(N)
def deliver_packages(truck, package_info, hub_addresses, hub_distances):
    undelivered_packages = []
    # Takes all packages from the truck and places it in the undelivered_package list to be sorted
    # Time complexity: O(N^2)
    for package_id in truck.packages:
        package = package_info.get(package_id)
        if package_id == "9":
            package.address = "410 S State St"
            package.zip_code = "84111"
        package.departed_time = truck.departed_time
        undelivered_packages.append(package)
        truck.load += float(package.mass)

    # Clears out the Truck's packages property to later be filled with packages using nearest neighbor
    truck.packages.clear()
    amount_of_undelivered_packages = len(undelivered_packages)

    # Loops until all undelivered_packages are sorted
    # Time complexity: O(N)
    while amount_of_undelivered_packages > 0:
        # Set an initial high address distance
        next_address_distance = 100
        next_package = None

        # Time complexity: O(N)
        for package in undelivered_packages:
            truck_address_index = get_address_index(truck.location, hub_addresses)
            package_address_index = get_address_index(package.address, hub_addresses)
            distance_between = get_distance_between_addresses(truck_address_index, package_address_index, hub_distances)
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


# Create logic to assign package state, depending on delivery_time, user input time, and departed_time
# Time complexity: O(1)
# Space complexity: O(1)
def update_delivery_status(package, input_time):
    if package.departed_time > input_time:
        package.delivery_status = "At Hub"
    elif package.delivery_time <= input_time and package.delivery_time >= package.departed_time:
        package.delivery_status = "Delivered"
    elif package.departed_time < input_time:
        package.delivery_status = "In Route"


# Logic to create address and distance lists, load trucks, and deliver packages
# Time complexity: O(N)
# Space complexity: O(N)
def main_logic():
    with open(DISTANCE_PATH, 'r') as file:
        reader = csv.reader(file)
        distance_data = list(reader)

    # Create address and distance lists
    hub_addresses = create_address_list(distance_data)
    hub_distances = create_distance_list(distance_data)

    with open(PACKAGE_PATH, 'r') as csvfile:
        reader = csv.reader(csvfile)
        package_data = list(reader)

    # Create package hash map
    package_info_hash = create_package_hash(package_data)

    # Manually loading all packages for each truck
    truck_one_package_ids = ["13", "14", "15", "16", "19", "20", "1", "40", "4", "21", "5", "37", "34", "33", "30", "29"]
    truck_two_package_ids = ["3", "38", "36", "18", "9", "26", "24", "33", "39", "35"]
    truck_three_package_ids = ["6", "32", "25", "28", "31", "12", "17", "22", "2", "7", "8", "9", "10", "11", "27", "23"]

    current_date = datetime.now().date()
    time_object_one = time(8, 0, 0)
    time_object_two = time(10, 20, 0)
    time_object_three = time(9, 5, 0)

    start_time_one = datetime.combine(current_date, time_object_one)
    start_time_two = datetime.combine(current_date, time_object_two)
    start_time_three = datetime.combine(current_date, time_object_three)

    # Create all truck objects
    truck_one = Truck(start_time_one, None, truck_one_package_ids, 0.0, 0.0)
    truck_two = Truck(start_time_two, None, truck_two_package_ids, 0.0, 0.0)
    truck_three = Truck(start_time_three, None, truck_three_package_ids, 0.0, 0.0)

    truck_one.departed_time = start_time_one
    truck_two.departed_time = start_time_two
    truck_three.departed_time = start_time_three

    # Deliver packages on each truck
    deliver_packages(truck_one, package_info_hash, hub_addresses, hub_distances)
    deliver_packages(truck_three, package_info_hash, hub_addresses, hub_distances)
    truck_two.current_time = start_time_two
    truck_two.departed_time = start_time_two
    deliver_packages(truck_two, package_info_hash, hub_addresses, hub_distances)

    total_mileage = truck_one.mileage + truck_two.mileage + truck_three.mileage

    def start_program():
        print("╔═════════════════════════════════════════════╗")
        print("║                    WGUPS                    ║")
        print("║                                             ║")
        print("║ Western Governors University Parcel Service ║")
        print("╚═════════════════════════════════════════════╝")
        print(f"Truck 1: {truck_one_package_ids}"
              f"\nTruck 2: {truck_two_package_ids}"
              f"\nTruck 3: {truck_three_package_ids}\n")

        options = ["Check status of One Package", "Check status of All Packages", "Print All Package status and total milage"]

        print("Please select an option: ")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        selected_option = input("Enter the number corresponding to your choice: ")

        if selected_option == "1" or selected_option == "2":
            input_time = input("Enter a time with format (HH:MM:SS): ")
            hour, minute, second = map(int, input_time.split(":"))

            match_date = start_time_one.date()
            input_time_object = time(hour, minute, second)

            datetime_time = datetime.combine(match_date, input_time_object)

            if selected_option == "1":
                input_package_id = input("Enter a package ID: ")
                package = package_info_hash.get(input_package_id)
                update_delivery_status(package, datetime_time)
                print(f"[Package {input_package_id}]: {package}")

            if selected_option == "2":
                for key in package_info_hash.keys():
                    package_info = package_info_hash.get(key)
                    update_delivery_status(package_info, datetime_time)
                    print(f"[Package {key}]: {package_info}")

        if selected_option == "3":
            print("╔═════════════════════════════════════════════╗")
            print(f"║    Total Milage: {total_mileage}                      ║")
            print("╚═════════════════════════════════════════════╝")
            for key in package_info_hash.keys():
                package_info = package_info_hash.get(key)
                update_delivery_status(package_info, truck_two.current_time)
                print(f"[Package {key}]: {package_info}")

    start_program()


if __name__ == "__main__":
    main_logic()
