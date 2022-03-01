import chaining_hash_node
from chaining_hash_node import ChainingHashNode

class ChainingHashSet():
    def __init__(self, capacity=0):
        self.hash_table = [None] * capacity
        self.table_size = 0
        self.capacity = capacity
        self.node = ChainingHashNode()

    def get_hash_code(self, key):
        """Hash function that calculates a hash code for a given key using the modulo division.
        :param key:
        		Key for which a hash code shall be calculated according to the length of the hash table.
        :return:
        		The calculated hash code for the given key.
        """
        N = len(self.hash_table)
        hash_function = key % N
        return hash_function

    def get_hash_table(self):
        """(Required for testing only)
        :return the hash table.
        """
        """for i in range(len(self.hash_table)):
            print(self.hash_table[i])"""
        return self.hash_table

    def set_hash_table(self, table):
        """(Required for testing only) Set a given hash table..
        :param table: Given hash table which shall be used.

        !!!
        Since this method is needed for testing we decided to implement it.
        You do not need to change or add anything.
        !!!

        """
        self.hash_table = table
        self.capacity = len(table)
        self.table_size = 0
        for node in table:
            while node is not None:
                self.table_size += 1
                node = node.next

    def get_table_size(self):
        """returns the number of stored keys (keys must be unique!)."""
        return self.table_size

    def insert(self, key):
        """Inserts a key and returns True if it was successful. If there is already an entry with the
          same key, the new key will not be inserted and False is returned.
         :param key:
         		The key which shall be stored in the hash table.
         :return:
         		True if key could be inserted, or False if the key is already in the hash table.
         :raises:
         		a ValueError if any of the input parameters is None.
         """

        if key is None:
            raise ValueError

        place = self.get_hash_code(key)
        node = self.hash_table[place]

        if node is None:
            self.hash_table[place] = ChainingHashNode(key)
            self.table_size += 1
            return True

        ok=0
        prev = node
        while node is not None:
            prev = node
            node = node.next
            if prev.key == key:
                ok = 1

        if ok == 0:
            prev.next = ChainingHashNode(key)
            self.table_size += 1
            return True
        else:
            return False


    def contains(self, key):
        """Searches for a given key in the hash table.
         :param key:
         	    The key to be searched in the hash table.
         :return:
         	    True if the key is already stored, otherwise False.
         :raises:
         	    a ValueError if the key is None.
         """
        if key is None:
            raise ValueError

        place = self.get_hash_code(key)
        node=self.hash_table[place]

        while node is not None and node.key != key:
            node = node.next

        if node is not None:
            return True
        else:
            return False

    def remove(self, key):
        """Removes the key from the hash table and returns True on success, False otherwise.
        :param key:
        		The key to be removed from the hash table.
        :return:
        		True if the key was found and removed, False otherwise.
        :raises:
         	a ValueError if the key is None.
        """

        if key is None:
            raise ValueError

        if self.contains(key) is False:
            return False
        else:

            place = self.get_hash_code(key)
            current_node = self.hash_table[place]

            if current_node.key == key:
                if current_node.next != None:
                    current_node.key = current_node.next.key
                    current_node.next = current_node.next.next
                    self.table_size -= 1
                    return True
                elif current_node.next == None:
                    self.hash_table[place]=None
                    self.table_size -= 1
                    return True

            elif current_node.key != key:
                while current_node.next.key != key:
                    current_node = current_node.next

                key_node= current_node.next

                if key_node.next != None:
                    current_node.next = key_node.next
                    self.table_size -= 1
                    return True
                elif key_node.next == None:
                    current_node.next=None
                    self.table_size -= 1
                    return True



    def clear(self):
        """Removes all stored elements from the hash table by setting all nodes to None.
        """

        self.table_size=0
        self.hash_table = [None] * self.capacity
        self.capacity = self.capacity

    def to_string(self):
        """Returns a string representation of the hash table (array indices and stored keys) in the format
            Idx_0 {Node, Node, ... }, Idx_1 {...}
            e.g.: 0 {13}, 1 {82, 92, 12}, 2 {2, 32}, """
        list=[]
        for i in self.hash_table:
            for j in self.hash_table[i][1]:
                list.append(j.key)

            return (f"{i} {list}")


