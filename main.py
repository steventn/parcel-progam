import csv
import hash_table, package
import truck

PACKAGE_PATH = 'resources/WGUPS Package File.csv'
DISTANCE_PATH = 'resources/WGUPS Distance Table.csv'

def main():

    def read_csv(path):
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                new_package = package.Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], "At hub")
                package_info.put(row[0], new_package)

    def load_csv_data(path):
        csv_data = {}
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read and discard the header row

            for row in csv_reader:
                address = row[0]
                distances = {}
                for i, distance in enumerate(row[1:], start=1):
                    distances[header[i]] = float(distance)
                csv_data[address] = distances

        return csv_data

    def get_distance(address1, address2, csv_data):
        if address1 in csv_data and address2 in csv_data[address1]:
            return csv_data[address1][address2]
        else:
            return None

    package_info = hash_table.HashMap(40)
    read_csv(PACKAGE_PATH)
    packages = [package_info.get("1"), package_info.get("2"), package_info.get("3")]
    new_truck = truck.Truck("", "", "", packages, "", "", "", "")

    distance_one = ""
    distance_two = ""

    for item in new_truck.packages:
        distance_one = item.address
        distance_two = item.address

    distance_data = load_csv_data(DISTANCE_PATH)
    print(get_distance(distance_one, distance_two, distance_data))



if __name__ == "__main__":
    main()

