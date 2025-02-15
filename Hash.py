import Package


# ChainingHashTable Class
class ChainingHashTable:

    # initialize the hash table O(n)
    def __init__(self, initial_capacity):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table O(n)
    def insert(self, p_id, p_address, p_city, p_state, p_zip, p_deadline, p_mass, p_note, p_status):
        p = Package.Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_mass, p_note, p_status)
        hash_item = hash(p_id) % len(self.table)
        item_list = self.table[hash_item]

        # update item if it's in the list
        for j in item_list:
            if j[0] == p_id:
                j[1] = p
                return
        key_pair = [p_id, p]
        item_list.append(key_pair)

    # Searches for an item with matching id in the hash table O(n)
    def search(self, id):
        # get the bucket list where this key would be
        item = hash(id) % len(self.table)
        item_list = self.table[item]

        # search for the id in the list
        for i in item_list:
            if i[0] == id:
                return i[1]

    # Removes an item from the hash table O(n)
    def remove(self, id):
        item = hash(id) % len(self.table)
        item_list = self.table[item]

        # remove the item from the list if it is present
        for s in item_list:
            if s[0] == id:
                item_list.remove([s[0], s[1]])
