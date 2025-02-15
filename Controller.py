import Hash
import Loader
import route_breakdown


# Function to load trucks by taking the package_file and distance_table as parameters and returning a trucks list,
# modified package_hash table, loader object that holds the Package_File and Distance_Table information.
# This function loads the package information into the package hash then collects all package ids where the package
# has a deadline. The deadline list is then sorted from by the minimal distance between package addresses. The sorted
# deadline list and packages that don't have a deadline are concatenated to a single delivery route.
# The package hash is processed to identify and mark packages with a special notes. Trucks are created and use the
# modified package hash to sort the packages into the right truck or hub pending the package note.
# Packages are then updated with the truck the package is in. O(n^2)
def load_trucks(Package_File, Distance_Table):
    # Creates loader object
    loader = Loader.Loader()  # O(1)

    trucks = []

    # Loader object uses member function to read in Package_File file and load data into loader object
    loader.count_package_data(Package_File)  # O(n)

    # Package hash is created with the amount of packages found in the loader function
    package_hash = Hash.ChainingHashTable(loader.amount_of_packages)  # O(n)

    # Loader object reads in the empty package hash and loads the package information
    # into the package hash
    packages = loader.load_package_data(package_hash)  # O(n)

    # Loader object loads the distance data from the Distance_Table file and loads data into the loader object
    loader.load_distance_data(Distance_Table)  # O(n^2)

    # Function from route_breakdown that finds packages that have a deadline and saves the package ids to a list
    deadlines, eods = route_breakdown.find_deadlines(packages, trucks)  # O(n)

    # Function from route_breakdown finds the minimal distance between each package address in the deadline list
    sorted_deadline_list = route_breakdown.min_distance(deadlines, loader, package_hash)  # O(n^2)

    # [15, 16, 34, 14, 25, 20, 31, 6, 40, 1, 29, 37, 30, 13]
    # Function grammer_check.int_list_trim formats list into a more readable form
    sorted_deadline_list = route_breakdown.int_list_trim(sorted_deadline_list)  # O(n)

    # [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 32, 33, 35, 36, 38, 39]
    # Function from route_breakdown finds packages that done have a deadline and appends them to a list
    the_rest_of_the_list = route_breakdown.get_the_rest(sorted_deadline_list, packages)  # O(n)

    # [15, 16, 34, 14, 26, 25, 19, 20, 21, 32, 31, 17, 6, 4, 40, 1, 2, 7, 28, 29, 5, 10, 33, 38, 37, 8, 30, 3, 39,
    # 13, 27, 35, 36, 12, 9, 24, 22, 11, 23, 18]
    # Concatenating sorted_deadline_list and the_rest_of_the_list lists
    delivery_route = sorted_deadline_list + the_rest_of_the_list

    # ====================================================================================================================
    # nums = []
    # for i in range(1, 40):
    #     nums.append(i)
    # delivery_route = nums
    # ====================================================================================================================

    # Function from route_breakdown sets package status based on special note, used for sorting later
    route_breakdown.process_packages(delivery_route, package_hash)  # O(n)

    # Function from route_breakdown takes processed package hash and route and sorts packages
    # into each truck of hub list
    trucks, hub_list = route_breakdown.get_trucks_and_hub_list(delivery_route, package_hash)  # O(n^2)

    # Function from route_breakdown processes the package hash listing which truck each package is in
    route_breakdown.process_trucks(trucks, hub_list, package_hash)  # O(n^2)

    return trucks, package_hash, loader


# Controller Class
class Controller:

    # Function to initialize the controller object using an inputted time   # O(1)
    def __init__(self, time_input):
        self.time = time_input

    # Function to set the time for the controller object  # O(1)
    def set_time(self, new_time):
        self.time = new_time

    # Function returns the time from the controller object  # O(1)
    def get_time(self):
        return self.time

    # Function delivers the packages by using a list of loaded trucks, the package hash and a loader object by
    # using a while loop to assign drivers to available trucks and runs the routes of those trucks until finished or
    # times up. O(n^4)
    def deliver_packages(self, trucks, package_hash, loader):
        total_miles = 0.0
        drivers = 2
        done = False
        flag = True
        flag2 = True
        driver_flag = True
        eods = []
        wrong_add_list = []
        del_list = []
        driver_counter = 0

        while  not done:
            start_del = ""

            # This code block takes the del_list modified later in the function and finds the earliest time
            if len(del_list) == drivers and len(del_list) != 0:
                nums1 = del_list[0].split(":")
                nums = del_list[1].split(":")
                if 1 != len(nums1) and 1 != len(nums):
                    hours2 = float(nums1[0])
                    minutes1 = nums1[1]
                    mins1 = round(float(minutes1) / 60, 2)
                    hours = float(nums[0])
                    minutes = nums[1]
                    mins = round(float(minutes) / 60, 2)
                    del_it1 = hours2 + mins1
                    del_it2 = hours + mins
                    if del_it1 > del_it2:
                        del_list[0] = del_list[1]
                    start_del = del_list[0]

            # Function from route_breakdown assigns drivers to trucks and returns the amount of available drives
            drivers = route_breakdown.get_drivers(trucks, drivers)  # O(n)

            # Secondary loop to select each truck and deliver packages pending if the truck has a driver
            for truck in trucks:
                trigger_word = "loaded"

                # code block sets the start time for the remaining trucks
                if driver_counter == 2 and driver_flag:
                    truck.set_start(start_del)  # O(1)
                else:
                    truck.set_start("08:00")
                # code block appends additional packages to available truck
                if trigger_word == truck.get_status():  # O(1)
                    new_list = truck.get_packages() + eods + wrong_add_list  # O(1)
                    truck.set_package(new_list)  # O(1)

                # code block checks if the truck has a driver
                if truck.get_driver():  # O(1)

                    # Function from route_breakdown delivers the packages of an individual truck using the package hash,
                    # controller object time and loader object. Function returns the truck the was out delivering,
                    # and 3 separate flags used to pass information between functions
                    truck, load_others, load_wrong, driver_flag = route_breakdown.run_route(package_hash, truck,
                                                                                            self.time,
                                                                                            loader)  # O(n^2)
                    # updating total miles after delivery
                    total_miles = total_miles + truck.get_miles()

                    # code block checks 2 boolean variables and sets information to a packages status
                    if load_wrong and flag:
                        for j in range(len(package_hash.table)):
                            package = package_hash.search(j + 1)  # O(1)
                            note = package.get_note()  # O(1)
                            if "Wrong" in note:
                                package.set_zip("84111")  # O(1)
                                package.set_address("410 S State St")  # O(1)
                                wrong_add_list.append(package.get_id())
                                package.set_status(f"Correct address found")  # O(1)
                                flag = False

                    # code block checks 2 boolean variables and sets information to a packages status
                    if load_others and flag2:
                        for i in range(len(package_hash.table)):
                            package2 = package_hash.search(i + 1)  # O(1)
                            status2 = package2.get_status()  # O(1)
                            note2 = package2.get_note()  # O(1)
                            if "delayed" in status2 and "Wrong" not in note2:
                                eods.append(package2.get_id())  # O(1)
                                t_sum = 0
                                if drivers == 0:
                                    t_sum = 3
                                package2.set_status(f"received at 9:05 am, in truck {t_sum}")  # O(1)
                                flag2 = False

                    # code block checks to see if the truck is done and releases the driver
                    if "done" in truck.get_status():
                        drivers = drivers + 1
                        truck.set_driver(0)
                        driver_counter = driver_counter + 1
                        del_list.append(truck.get_end())

                # code block checks drivers and boolean and sets trucks status
                if not driver_flag and drivers != 0:
                    truck.set_status("done")  # O(1)
            out = 0
            # code block loops through trucks list and checks to see if all the trucks are done
            for t in trucks:
                if "done" in t.get_status():
                    out = out + 1

            # code block checks truck counter and ends the main loop
            if out == 3:
                done = True

                # code block prints the miles of each truck and shows the total amount of miles traveled
                for truck in trucks:
                    mls = truck.get_miles()
                    print(f"truck {truck.get_id() + 1} has traveled {round(mls, 2)} miles")
                print(f"All trucks traveled {round(total_miles, 2)} miles \nat {self.time}")
                print()

        return
