class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''

    def __init__(self, name: str, number: str) -> None:
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''

    def __init__(self, key: str, value: Contact) -> None:
        self.key = key
        self.value = value
        self.next = None  # next Node or None


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, number): Inserts a new contact into the hash table (or updates).
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''

    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("HashTable size must be > 0")
        self.size = size
        self.data = [None] * size  # each slot is None or a Node (head of chain)

    def hash_function(self, key: str) -> int:
        """
        Convert key (name) to an index using ord().
        """
        total = 0
        for ch in key:
            total += ord(ch)
        return total % self.size

    def insert(self, key: str, number: str) -> None:
        """
        Insert a new Contact (name=key, phone=number).
        If name already exists, update the number.
        Collisions: separate chaining (linked list).
        """
        index = self.hash_function(key)
        head = self.data[index]

        # Empty bucket
        if head is None:
            self.data[index] = Node(key, Contact(key, number))
            return

        # Traverse chain: update if found
        current = head
        while current is not None:
            if current.key == key:
                current.value.number = number  # update existing
                return
            if current.next is None:
                break
            current = current.next

        # Not found -> add new node at end
        current.next = Node(key, Contact(key, number))

    def search(self, key: str):
        """
        Return Contact if found, else None.
        """
        index = self.hash_function(key)
        current = self.data[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def print_table(self) -> None:
        """
        Print the hash table structure for debugging.
        """
        for i in range(self.size):
            current = self.data[i]
            if current is None:
                print(f"Index {i}: Empty")
            else:
                line = f"Index {i}:"
                while current is not None:
                    line += f" - {current.value}"
                    current = current.next
                print(line)


# Test your hash table implementation here.
if __name__ == "__main__":
    table = HashTable(10)

    # Empty table
    table.print_table()

    # Insert
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    table.print_table()

    # Search
    print("\nSearch result:", table.search("John"))

    # Collision test (depends on hash function)
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    table.print_table()

    # Duplicate update
    table.insert("Rebecca", "999-444-9999")
    table.print_table()

    # Not found
    print(table.search("Chris"))  # None


"""
-------------------- DESIGN MEMO (200–300 words) --------------------

A hash table is a good structure for fast lookups because it can usually find a
contact in O(1) time. Instead of scanning every contact like a list would, the
hash table uses a hash function to convert a contact’s name (the key) into an
index in an array. This allows the program to jump directly to the correct area
of memory, which stays fast even when there are hundreds of contacts.

I handled collisions using separate chaining. Each index in the array can store
the start of a linked list. When two different names hash to the same index, the
new contact is added into that linked list instead of overwriting the existing
one. Searching works by hashing the name to find the correct index, then walking
through only that index’s linked list until the contact is found or the list ends.
This keeps searching efficient because it avoids checking unrelated contacts.

Engineers choose hash tables over lists when they need quick exact searches by a
key, like looking up a contact by name. A list is simpler but becomes slow as it
grows because it requires O(n) searching. A tree can keep data ordered and support
range queries, but for simple “find this exact name” lookups, a hash table is often
faster and simpler. When order is not important and speed matters, a hash table is
a strong choice.

-------------------------------------------------------------------
"""
