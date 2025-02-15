import csv


# Loader Class
class Loader:

    # Function to initialize the loader object O(1)
    def __init__(self):
        self.package_hash = None
        self.amount_of_packages = 0
        self.packages = []
        self.addresses = []
        self.distances = []

    # Function counts the amount of packages in the file and appends each row to a list in the loader object O(n)
    def count_package_data(self, file_name):
        with open(file_name, newline='') as Packages:
            packages = csv.reader(Packages, delimiter=',')
            next(packages)
            next(packages)
            next(packages)
            count = 0
            for row in packages:
                count = count + 1
                self.packages.append(row)
            self.amount_of_packages = count

    # Function runs through the package list in loader object inserts values into a package hash then returns the
    # hash O(n)
    def load_package_data(self, package_hash):
        for row in self.packages:
            p_id = int(row[0])
            p_address = row[1]
            p_city = row[2]
            p_state = row[3]
            p_zip = row[4]
            p_deadline = row[5]
            p_mass = row[6]
            p_note = row[7]
            p_status = 'received'
            package_hash.insert(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_mass, p_note, p_status)
        return package_hash

    # Function to load the distance data from the given file into the loader object O(n^2)
    def load_distance_data(self, file_name):
        with open(file_name, newline='') as Distances:
            addresses = []
            distance_list = []
            just_distance_rows = []
            just_distances_list = []
            distances = csv.reader(Distances, delimiter='"')
            next(distances)
            next(distances)
            next(distances)
            flag = False
            for row in distances:
                if not row:
                    flag = True
                if flag and row != []:
                    distance_list.append(row)
            for item in distance_list:
                dis_list = item[2].split()
                just_distance_rows.append(dis_list)
                item[1] = item[1].lstrip()
                item[1] = item[1].replace("(", "")
                item[1] = item[1].replace(")", "")
                addresses.append(item[1])
            for row in just_distance_rows:
                for line in row:
                    word = line.split(',')
                    word.remove('')
                    if "HUB" in word:
                        word.remove("HUB")
                    just_distances_list.append(word)
                    self.addresses = addresses
                    self.distances = just_distances_list

    # Get package data from the loader object O(1)
    def get_packages(self):
        return self.packages

    # Get address data from the loader object O(1)
    def get_addresses(self):
        return self.addresses

    # Get distance data from the loader object O(1)
    def get_distances(self):
        return self.distances

    # Get the amount of packages in the loader object O(1)
    def get_amount_of_packages(self):
        return self.amount_of_packages
