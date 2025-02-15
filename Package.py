# Package Class
class Package:
    def __init__(self, p_id, p_address, p_city, p_state, p_zip, p_deadline, p_mass, p_note, p_status):
        self.id = p_id
        self.address = p_address
        self.city = p_city
        self.state = p_state
        self.zip = p_zip
        self.deadline = p_deadline
        self.mass = p_mass
        self.note = p_note
        self.status = p_status

    # String function to print a package object O(1)
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.id, self.address, self.city, self.state, self.zip, self.deadline, self.mass, self.note, self.status)

    # Get package id O(1)
    def get_id(self):
        return self.id

    # Get package address O(1)
    def get_address(self):
        return self.address

    # Get package city O(1)
    def get_city(self):
        return self.city

    # Get package state O(1)
    def get_state(self):
        return self.state

    # Get package zip O(1)
    def get_zip(self):
        return self.zip

    # Get package deadline O(1)
    def get_deadline(self):
        return self.deadline

    # Get package mass O(1)
    def get_mass(self):
        return self.mass

    # Get package note O(1)
    def get_note(self):
        return self.note

    # Get package status O(1)
    def get_status(self):
        return self.status

    # Set package status O(1)
    def set_status(self, status):
        self.status = status

    # Set package address O(1)
    def set_address(self, add):
        self.address = add

    # Set package zip O(1)
    def set_zip(self, zip):
        self.zip = zip
