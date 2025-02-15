import math
import time
import Truck


# Function returns a deadline list and eod list by either using a parameter list if the list isn't empty or
# searching through the package hash.  O(n)
def find_deadlines(package_hash, package_list):
    package_route = []
    if not package_list:
        for i in range(len(package_hash.table)):
            package = package_hash.search(i + 1)
            if "EOD" not in package.deadline:
                package_route.append(i + 1)
    else:
        package_route = package_list
    times = []
    for i in package_route:
        package = package_hash.search(i)
        text = package.deadline
        split_text = text.split(':')
        time_w_id = "{}, {}".format(split_text[0], package.id)
        times.append(time_w_id)
    num_list = []
    deadline_list = []
    eod_list = []
    for i in times:
        both = i.split(',')
        time_ = both[0]
        num = int(both[1])
        if "EOD" in time_:
            eod_list.append(int(num))
        elif not num_list:
            num_list.append(num)
            deadline_list.append(i)
        elif time_ > deadline_list[0]:
            num_list = [num] + num_list
            deadline_list = [i] + deadline_list
        else:
            num_list.append(num)
            deadline_list.append(i)
    return num_list, eod_list


# Function returns a sorted list with the minimal amount of distance between each package stop recursively O(n^2)
def min_distance(deadlines, loader, package_hash):
    route_list = []
    fact = True
    while fact:
        sorted_deadlines, left_overs = next_closest(deadlines, loader, package_hash)  # O(n)
        route_list.append(sorted_deadlines)
        last = sorted_deadlines[-1]
        left_overs.insert(0, last)
        deadlines = left_overs
        if len(sorted_deadlines) == 1:
            fact = False
    return route_list


# Function used recursively with the min_distance function, takes in a list, loader object and package hash
# and returns two list O(n)
def next_closest(list_of_deadlines, loader, packages):
    new_list = []
    left_overs = []
    smallest = 0.0
    index = ''
    addresses = loader.get_addresses()
    distances = loader.get_distances()
    if len(new_list) == 0:
        new_list.append(list_of_deadlines[0])
        list_of_deadlines.remove(list_of_deadlines[0])
    zero = 0
    for i in list_of_deadlines:
        start = packages.search(int(new_list[0]))
        add_start = get_address_id(start, addresses)
        end = packages.search(int(i))
        add_end = get_address_id(end, addresses)
        miles = get_distance(add_start, add_end, distances)
        if miles == 0:
            zero = zero + 1
            new_list.append(i)
        elif smallest == 0:
            zero = zero + 1
            smallest = miles
            left_overs.append(i)
            index = i
        elif miles < smallest:
            if miles != 0:
                smallest = miles
                index = i
                left_overs.append(i)
        else:
            left_overs.append(i)
    if zero == 1:
        new_list.append(index)
        left_overs.remove(index)

    return new_list, left_overs


# Function takes in a list and return list that does not have duplicates O(n^2)
def int_list_trim(dead_line_list):
    new_list = []
    for item in dead_line_list:
        if len(item) != 1:
            item.remove(item[-1])
    for item in dead_line_list:
        if len(item) > 1:
            for i in range(len(item)):
                new_list.append(item[i])
        else:
            new_list.append(item[0])
    return new_list


# Function returns an address id by using a package and addresses parameter O(n)
def get_address_id(package, addresses):
    address_index = 0
    address_and_zip = package.address + ' ' + package.zip
    for i in range(len(addresses)):
        if addresses[i] == address_and_zip:
            address_index = i
    return address_index


# Function returns miles between the start and end parameters O(1)
def get_distance(start, end, distances):
    if distances[start][end] == "" or distances[start][end] == 0:
        miles = float(distances[end][start])
    else:
        miles = float(distances[start][end])
    return miles


# Utility function to return a list of packages not in sorted list O(n)
def get_the_rest(sorted_list, packages):
    new_list = []
    list_size = len(packages.table)
    for i in range(1, list_size + 1):
        if i not in sorted_list:
            new_list.append(i)
    return new_list


# Function to return a delivery list by using a sorted_list, not_in_sorted_list, loader, package_hash parameters to
# find the packages from not_in_sorted_list in the area around each of the packages in the sorted_list by calculating
# finding the distance between packages in sorted_list, calculating the mid-point of that distance, create a
# right triangle using start or end points, the mid_point, and a perpendicular point from the travel plane.
# By setting the perpendicular side of triangle to the same distance as the distance to the mid-point
# we can calculate the resultant with the Pythagorean theorem, by doubling the resultant we have the limit in which
# the area of the calculation of the not_in_sorted_list packages. This area circles the start and end any other packages
# in the circle. Packages outside the area will be ignored O(n^2)
def on_the_way(sorted_list, not_in_sorted_list, loader, packages):
    delivery_list = []
    total_miles = 0.0
    addresses = loader.get_addresses()  # O(1)
    distances = loader.get_distances()  # O(1)
    # for every num in the sorted list check other packages for the next closest location in the area close by
    if len(delivery_list) == 0:
        delivery_list.append(sorted_list[0])
        sorted_list.remove(sorted_list[0])
    for num in sorted_list:
        start = packages.search(delivery_list[-1])  # O(1)
        end = packages.search(num)  # O(1)
        add_start = get_address_id(start, addresses)  # O(n)
        add_end = get_address_id(end, addresses)  # O(n)
        miles = get_distance(add_start, add_end, distances)  # O(1)
        if miles != 0:
            half_way = miles / 2
            resultant = math.sqrt(half_way ** 2 + half_way ** 2)
            area = resultant + resultant
            for item in not_in_sorted_list:
                mid_point = packages.search(item)  # O(1)
                mid_point_add = get_address_id(mid_point, addresses)  # O(n)
                distance_to_a = get_distance(add_start, mid_point_add, distances)  # O(1)
                distance_to_b = get_distance(mid_point_add, add_end, distances)  # O(1)
                area_sum = distance_to_b + distance_to_a
                if area_sum < area:
                    delivery_list.append(item)
                    not_in_sorted_list.remove(item)
                    total_miles = total_miles + area_sum
            if num != delivery_list[-1]:
                delivery_list.append(num)
        else:
            delivery_list.append(num)
    not_in_sorted_list.insert(0, delivery_list[-1])
    delivery_list.remove(delivery_list[-1])
    route_list = min_distance(not_in_sorted_list, loader, packages)  # O(n^2)
    remaining_list_sorted = int_list_trim(route_list)  # O(n)
    delivery_list = delivery_list + remaining_list_sorted
    return delivery_list


# Function processes the package hash by setting packages status with a special note O(n)
def process_packages(delivery_list, packages):
    for i in delivery_list:
        package = packages.search(i)
        note = package.get_note()
        if note:
            if 'Delayed' in note:
                package.set_status("delayed")
            elif 'delivered' in note:
                delivered_note = package.get_note()
                delivered_note = delivered_note[23:]
                numbers = delivered_note.split(", ")
                half_way = []
                for j in numbers:
                    half_way.append(int(j))
                package.set_status("list")
            elif 'truck' in note:
                truck_note = package.get_note()
                note = truck_note[21:]
                if "1" in note:
                    package.set_status("1")
                elif "2" in note:
                    package.set_status("2")
                elif "3" in note:
                    package.set_status("3")

            elif 'Wrong' in note:
                package.set_status("wrong address")


# Function returns loaded trucks and a list of packages ids that are at the hub by using the delivery_route and
# package hash. Trucks are loaded by parsing the packages by package notes making sure not to load more than 16 O(n^2)
def get_trucks_and_hub_list(delivery_route, package_hash):
    truck_list_1 = []
    truck_list_2 = []
    truck_list_3 = []
    hub = []
    waiting_list = []
    merge_list = []
    all_list = []
    # code block
    for i in delivery_route:
        package = package_hash.search(i)
        status = package.get_status()
        if "list" in status:
            merge_list.append(i)

    for merge_list_item in merge_list:
        group_list = []
        package = package_hash.search(merge_list_item)
        delivered_note = package.get_note()
        delivered_note = delivered_note[23:]
        numbers = delivered_note.split(", ")
        if merge_list_item not in group_list:
            group_list.append(merge_list_item)
        for i in numbers:
            group_list.append(int(i))
        all_list.append(group_list)

    merge_set = set()
    for i in all_list:
        for j in i:
            try:
                delivery_route.remove(j)
            except:
                pass
            merge_set.add(j)

    for i in delivery_route:

        package = package_hash.search(i)
        status = package.get_status()

        if "2" in status:
            truck_list_2.append(i)

        elif "1" in status:
            truck_list_1.append(i)

        elif "3" in status:
            truck_list_3.append(i)

    for i in delivery_route:
        package = package_hash.search(i)
        status = package.get_status()
        if "received" in status:
            waiting_list.append(i)

        elif "delayed" in status:
            hub.append(i)

        elif "wrong address" in status:
            hub.append(i)

    trucks = []
    truck_lists = [truck_list_1, truck_list_2, truck_list_3]

    for h in truck_lists:
        if len(h) < 16:
            if merge_set:
                for r in merge_set:
                    h.append(r)
                merge_set.clear()
                if waiting_list:
                    index = 0
                    for w in waiting_list:
                        if len(h) < 16:
                            h.append(w)
                            index = index + 1
                    for d in waiting_list[:index]:
                        waiting_list.remove(d)
            else:
                if waiting_list:
                    index2 = 0
                    for m in waiting_list:
                        if len(h) < 16:
                            h.append(m)
                            index2 = index2 + 1
                    for e in waiting_list[:index2]:
                        waiting_list.remove(e)
                else:
                    index3 = 0
                    for g in hub:
                        if len(h) < 16:
                            h.append(g)
                            index3 = index3 + 1
                    for y in waiting_list[:index3]:
                        hub.remove(y)

    for i, g in enumerate(truck_lists):

        if len(g) <= 16:
            truck = Truck.Truck(i, "loaded", g, 0, 0, "", "")
            trucks.append(truck)

    return trucks, hub


# Function processes package status in each truck and hub list O(n^2)
def process_trucks(trucks, hub_list, package_hash):
    for truck in trucks:
        truck_list = truck.get_packages()
        for i in truck_list:
            package = package_hash.search(i)
            package.set_status(f"package is in truck {truck.get_id() + 1}")
    for j in hub_list:
        package = package_hash.search(j)
        if "wrong" in package.get_status():
            package.set_status(f"package is in truck {truck.get_id() + 1}")


# Function assigns drivers to a truck based on truck status and amount of drivers O(n)
def get_drivers(trucks, drivers):
    for truck in trucks:
        finished = truck.get_status()  # O(1)
        with_driver = truck.get_driver()  # O(1)
        if not with_driver and "done" not in finished and drivers > 0:
            truck.set_driver(True)  # O(1)
            truck.set_status("loaded and driver aboard")  # O(1)
            drivers = drivers - 1
    return drivers


# Function checks current time and returns flags if timer has been tripped, and converts time to a float object O(1)
def check_if(times_up, total_time):
    stop = False
    package_flag = False
    load_wrong = False
    start = time.strptime(times_up, "%I:%M:%S %p")
    # convert
    hours = float(start.tm_hour)
    minutes = float(start.tm_min) / 60
    converted_time = hours + minutes
    # check to end
    if total_time >= converted_time:
        stop = True
    # check for packages
    if total_time >= 9.08:
        package_flag = True
    if total_time >= 10.33:
        load_wrong = True
    return stop, package_flag, converted_time, load_wrong


# Function convert a float time object and return a formatted string O(n)
def convert_time(total_time):
    time_str = str(total_time)
    nums = time_str.split(".")
    hours = nums[0]
    minutes = nums[1]
    minutes = "." + minutes
    mins = str(float(minutes) * 60)
    delivered_at = mins.split(".")
    if len(delivered_at[0]) == 1:
        holder = delivered_at[0]
        holder = "0" + holder
        delivered_at[0] = holder

    return f"{hours}:{delivered_at[0]}"


# Function delivers packages assigned to each truck until done or until time limit is met. Function uses the same
# sorting functions used earlier in the package processing and also uses my personal algorithm to calculate other
# package locations on the way. O(n^2)
def run_route(package_hash, truck, times_up, loader):
    the_time = times_up.split(":")
    fir = float(the_time[0])
    # code block checks if its pm and changes the float time accordingly
    if "PM" in the_time[2]:
        fir = fir + 12.0
    sec = float(the_time[1]) / 60
    watch = fir + sec
    addresses = loader.get_addresses()  # O(1)
    distances = loader.get_distances()  # O(1)
    package_list = truck.get_packages()  # O(1)
    deadlines, eods = find_deadlines(package_hash, package_list)  # O(n)
    load_other_packages = False
    load_wrong = False
    load_wrong_flag = False
    driver_flag = False
    zero_t = ""
    package_flag = False

    # code block checks if the deadlines list is empty to see which list to find the minimal distance between
    if len(deadlines) == 0:
        sorted_list = min_distance(eods, loader, package_hash)  # O(n^2)
    else:
        sorted_list = min_distance(deadlines, loader, package_hash)  # O(n^2)
    sorted_deadline_list = int_list_trim(sorted_list)  # O(n)
    delivery_route = on_the_way(sorted_deadline_list, eods, loader, package_hash)

    new_miles = 0.0
    new_miles = new_miles + get_distance(get_address_id(package_hash.search(delivery_route[0]), addresses), 0,
                                         distances)  # O(n)

    # code block sets the truck start time
    if truck.get_start() != "" and truck.get_start() != "08:00":  # O(1)
        start_t = time.strptime(truck.get_start(), "%I:%M")  # O(1)
        # convert
        hours = float(start_t.tm_hour)
        minutes = float(start_t.tm_min) / 60
        converted_time = hours + minutes
        total_time = converted_time
    else:
        total_time = 8.0
    truck_time = new_miles / 18
    total_time = total_time + truck_time
    counter = 0
    # check to see if time is up
    if watch > total_time:

        for j in truck.get_packages():
            package = package_hash.search(j)  # O(1)
            package.set_status(f"package in truck {truck.get_id() + 1} - in route")  # O(1)
        truck.add_miles(new_miles)  # O(1)
        # loop through the delivery_route list
        for i in range(len(delivery_route)):

            # checks if i is the last number in the list
            if i != len(delivery_route) - 1:
                # check to see if time is up
                if watch > total_time:
                    counter = counter + 1
                    start = package_hash.search(delivery_route[i])  # O(1)
                    end = package_hash.search(delivery_route[i + 1])  # O(1)
                    add_start = get_address_id(start, addresses)  # O(n)
                    add_end = get_address_id(end, addresses)  # O(n)
                    newer_miles = get_distance(add_start, add_end, distances)  # O(1)
                    truck_time = newer_miles / 18
                    total_time1 = total_time
                    total_time = total_time + truck_time
                    # check to see if time is up
                    if watch > total_time:

                        # at previous location
                        if new_miles == 0 and newer_miles == 0:
                            start.set_status(f"package delivered at {zero_t} by truck {truck.get_id() + 1}")  # O(1)
                            end.set_status(
                                f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1} ")  # O(1)

                        # at previous location &  new location
                        elif new_miles == 0 and newer_miles > 0:
                            start.set_status(f"package delivered at {zero_t} by truck {truck.get_id() + 1}")  # O(1)
                            end.set_status(
                                f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1} ")  # O(1)

                        # new location and old location
                        elif new_miles > 0 and newer_miles > 0:
                            if i == 0:
                                start.set_status(
                                    f"package delivered at {convert_time(total_time1)} by truck {truck.get_id() + 1} ")  # O(1)
                                end.set_status(
                                    f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1} ")  # O(1)
                            else:
                                end.set_status(
                                    f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1} ")  # O(1)

                        # old location and current zero
                        elif new_miles > 0 and newer_miles == 0:
                            start.set_status(
                                f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1}")  # O(1)
                            end.set_status(
                                f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1} ")  # O(1)
                            zero_t = convert_time(total_time)  # O(n)
                        if i == len(delivery_route) - 2:
                            end.set_status(
                                f"package delivered at {convert_time(total_time)} by truck {truck.get_id() + 1} ")  # O(1)

                        # Function checks the time and returns flags accordingly
                        done, package_flag, converted_time, load_wrong_flag = check_if(times_up, total_time)  # O(1)

                    # code block checks for flags from functions and sets boolean values in this function block
                    if counter != len(delivery_route):
                        driver_flag = True
                    if package_flag:
                        load_other_packages = True
                    if load_wrong_flag:
                        load_wrong = True
                    truck.add_miles(newer_miles)  # O(1)
                    new_miles = newer_miles

        truck.set_status("done")  # O(1)

        truck.set_end(convert_time(total_time))  # O(n)
    else:
        truck.set_status("done")  # O(1)
    return truck, load_other_packages, load_wrong, driver_flag
