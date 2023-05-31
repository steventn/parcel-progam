import csv
import hash_table, package


def main():
    # read package CSV and store it into a hash table
    package_info = hash_table.HashMap(40)

    path = 'resources/WGUPS Package File.csv'

    def read_csv(path):
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                new_package = package.Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                package_info.put(row[0], new_package)

    read_csv(path)

    print(package_info.get("5"))

if __name__ == "__main__":
    main()

