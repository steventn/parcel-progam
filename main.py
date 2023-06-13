import csv
import hash_table, package
import truck

PACKAGE_PATH = 'resources/WGUPS Package File.csv'
DISTANCE_PATH = 'resources/WGUPS Distance Table.csv'


def main():
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
        with open(PACKAGE_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                new_package = package.Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], "At hub")
                package_info.put(row[0], new_package)

    def get_address_index(address):
        hub_addresses = create_address_list()
        for index, hub_addresses in enumerate(hub_addresses):
            if address in hub_addresses:
                return index

    def get_distance_between_addresses(address_x, address_y):
        hub_distances = create_distance_list()
        exact_distance = hub_distances[address_x][address_y]
        if exact_distance == "":
            return hub_distances[address_y][address_x]
        return exact_distance

    package_info = hash_table.HashMap(40)
    create_package_hash()

    truck_one_packages = [package_info.get("13"), package_info.get("14"), package_info.get("15"), package_info.get("16"), package_info.get("19"), package_info.get("20")]
    truck_two_packages = [package_info.get("3"), package_info.get("18"), package_info.get("36"), package_info.get("38")]
    new_truck = truck.Truck("", "", "", truck_one_packages, "", "", "", "")

    def deliver_packages(truck):
        # List of packages to be sorted using the nearest neighbor algorithm
        undelivered_packages = []
        # Takes all packages from the truck and places it in the undelivered_package list to be sorted
        # O(n) operation
        for id in truck.packages:
            package = package_info.get(id)
            undelivered_packages.append(package)

        # Clears out the Truck's packages property
        truck.packages.clear()
        amount_of_undelivered_packages = len(undelivered_packages)

        # Loops until all undelivered_packages are sorted
        while amount_of_undelivered_packages > 0:
            next_address_distance = 100
            next_package = None

            for package in undelivered_packages:
                truck_address_index = get_address_index(truck.location)
                package_address_index = get_address_index(package.location)
                distance_between = get_distance_between_addresses(truck_address_index, package_address_index)
                if distance_between <= next_address_distance:
                    next_address_distance = distance_between
                    next_package = package

            truck.packages.append(next_package.ID)
            undelivered_packages.remove(next_package)
            truck.mileage += next_address_distance
            truck.address = next_package.address
            truck.add_truck_time(next_address_distance)
            next_package.delivery_time = truck.current_time
            next_package.departure_time = truck.departed_time


    package_one = new_truck.packages[0].address
    package_two = new_truck.packages[1].address
    print(package_one)
    print(package_two)
    distance_one_index = get_address_index(package_one)
    distance_two_index = get_address_index(package_two)
    distance = get_distance_between_addresses(distance_one_index, distance_two_index)
    print(distance)



if __name__ == "__main__":
    main()

