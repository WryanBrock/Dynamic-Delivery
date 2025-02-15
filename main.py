# Name: Wryan Ledbetter Student ID: 001334580

import time
import Controller

# Start of program  # O(n^4) and change
if __name__ == "__main__":

    # Times for the start and end of the day
    time_start_input = "08:00:00 AM"
    time_end_input = "05:00:00 PM"

    # Reading in the input time from user
    time_input = time.strptime(input("what is the time?\n"), "%H:%M")

    # Format times for easy readability
    start = time.strptime(time_start_input, "%I:%M:%S %p")
    end = time.strptime(time_end_input, "%I:%M:%S %p")
    format_time = time.strftime("%I:%M:%S %p", time_input)
    format_time_start = time.strftime("%I:%M:%S %p", start)
    format_time_end = time.strftime("%I:%M:%S %p", end)

    # Check to see if the time input is in the range of the start and end time
    if start <= time_input < end:

        # Initializing controller object with format_time parameter
        controller = Controller.Controller(format_time)  # O(1)

        # Using the controller object's function to create the package_hash object, loader object, and loaded trucks
        # list
        # trucks = Controller.load_trucks(sys.argv[1], sys.argv[2]))
        trucks, package_hash, loader = Controller.load_trucks('WGUPS-Package-File.csv', 'WGUPS-Distance-Table.csv')  # O(n^2)

        # Used to end program
        done = False
        # Using the controller object's function to deliver packages inside the trucks in the trucks list
        controller.deliver_packages(trucks, package_hash, loader)  # O(n^4)

        # Main loop for program
        while not done:
            print()

            # Selection menu for users
            answer = int(input("The time is {}\n"
                               "Please choose an option\n"
                               "1. select a package by id\n"
                               "2. select all packages\n"
                               "3. change time of day\n"
                               "4. end\n".format(controller.get_time().lstrip("0"))))  # O(1)
            print()

            # Statement selects a package from the package_hash based on the id and returns it to the screen
            if 1 == answer:
                package_id = int(input("what is the id number?"))

                print(f"{package_hash.search(package_id)}")

            # Statement selects all packages from the package_hash based on the id and returns them to the screen
            elif 2 == answer:
                for i in range(len(package_hash.table)):
                    print(f"{package_hash.search(i+1)}")

            # Statement change the input time and redelivers the packages, while saving the package info in the
            # package_hash
            elif 3 == answer:
                new_time = time.strptime(input("what time would you like to change it to?\n"), "%H:%M")
                if start <= new_time < end:
                    format_time = time.strftime("%I:%M:%S %p", new_time)
                    controller.set_time(format_time)  # O(1)
                    trucks, package_hash, loader = Controller.load_trucks('WGUPS-Package-File.csv',
                                                                          'WGUPS-Distance-Table.csv')  # O(n^2)
                    controller.deliver_packages(trucks, package_hash, loader)  # O(n^4)
                else:
                    print("Try another time\n"
                          "Business hours are between\n"
                          "8am and 5pm")

            # Statement to end the program
            elif 4 == answer:
                done = True

            # Used in case menu choice wasn't between 1 and 4
            else:
                print("try again")
    # Used if time input was outside start and end times
    else:
        print("Try another time\n"
              "Business hours are between\n"
              "8am and 5pm")
