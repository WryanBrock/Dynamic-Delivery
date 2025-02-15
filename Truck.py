# Truck Class
class Truck:

    # Function to initialize a truck object O(1)
    def __init__(self, id, status, packages, miles_traveled, driver, start, end):
        self.id = id
        self.status = status
        self.packages = packages
        self.miles_traveled = miles_traveled
        self.driver = driver
        self.start = start
        self.end = end

    # Function to return a string representation of a truck object O(1)
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (
            self.id, self.status, self.packages, self.miles_traveled, self.driver, self.end, self.end )

    # Function to add miles to trucks package list O(1)
    def add_miles(self, miles):
        self.miles_traveled += miles

    # Function to return miles traveled by truck O(1)
    def get_miles(self):
        return self.miles_traveled

    # Function to set miles traveled for the truck O(1)
    def set_miles(self, miles):
        self.miles_traveled = miles

    # Function to set the packages data member O(1)
    def set_package(self, packages):
        self.packages = packages

    # Function to return packages on the truck O(1)
    def get_packages(self):
        return self.packages

    # Function to set the status in truck object O(1)
    def set_status(self, message):
        self.status = message

    # Function to return the truck status O(1)
    def get_status(self):
        return self.status

    # Function to set driver to truck O(1)
    def set_driver(self, driver):
        self.driver = driver

    # Function to return if a driver is aboard the truck object O(1)
    def get_driver(self):
        return self.driver

    # Function to return the truck id O(1)
    def get_id(self):
        return self.id

    # Function to set the truck start time O(1)
    def set_start(self, start):
        self.start = start

    # Function to set the truck end time O(1)
    def set_end(self, end):
        self.end = end

    # Function to return the start time O(1)
    def get_start(self):
        return self.start

    # Function to return the end time O(1)
    def get_end(self):
        return self.end