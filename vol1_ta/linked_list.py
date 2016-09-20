# linked_lists.py
"""Volume II Lab 4: Data Structures 1 (Linked Lists)
<Name>
<Class>
<Date>
"""


# Problem 1
class Node(object):
    """A basic node class for storing data. Only int, str, float or long data is permitted."""
    def __init__(self, data):
        """Store 'data' in the 'value' attribute."""
        if type(data) in [int, str, long, float]:
            self.value = data
        else: raise TypeError("Invalid data type "+str(type(data)))
        


class LinkedListNode(Node):
    """A node class for doubly linked lists. Inherits from the 'Node' class.
    Contains references to the next and previous nodes in the linked list.
    """
    def __init__(self, data):
        """Store 'data' in the 'value' attribute and initialize
        attributes for the next and previous nodes in the list.
        """
        Node.__init__(self, data)       # Use inheritance to set self.value.
        self.next = None
        self.prev = None


class LinkedList(object):
    """Doubly linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def __init__(self):
        """Initialize the 'head' and 'tail' attributes by setting
        them to 'None', since the list is empty initially.
        """
        self.head = None
        self.tail = None
        self.len = 0

    def append(self, data):
        """Append a new node containing 'data' to the end of the list."""
        # Create a new node to store the input data.
        new_node = LinkedListNode(data)
        if self.head is None:
            # If the list is empty, assign the head and tail attributes to
            # new_node, since it becomes the first and last node in the list.
            self.head = new_node
            self.tail = new_node
        else:
            # If the list is not empty, place new_node after the tail.
            self.tail.next = new_node               # tail --> new_node
            new_node.prev = self.tail               # tail <-- new_node
            # Now the last node in the list is new_node, so reassign the tail.
            self.tail = new_node
        self.len += 1

    # Problem 2
    def find(self, data):
        """Return the first node in the list containing 'data'.
        If no such node exists, raise a ValueError.

        Examples:
            >>> l = LinkedList()
            >>> for i in [1,3,5,7,9]:
            ...     l.append(i)
            ...
            >>> node = l.find(5)
            >>> node.value
            5
            >>> l.find(10)
            ValueError: <message>
        """
        if self.head is None:
            raise ValueError("Empty List")
        
        cur = self.head
        while cur is not None:
            if cur.value == data:
                return cur
            cur = cur.next
        
        raise ValueError("No node with value "+str(data))
#        raise NotImplementedError("Problem 2 Incomplete")

    # Problem 3
    def __len__(self):
        """Return the number of nodes in the list.

        Examples:
            >>> l = LinkedList()
            >>> for i in [1,3,5]:
            ...     l.append(i)
            ...
            >>> len(l)
            3
            >>> l.append(7)
            >>> len(l)
            4
        """
        pass
#        raise NotImplementedError("Problem 3 Incomplete")

    # Problem 3
    def __str__(self):
        """String representation: the same as a standard Python list.

        Examples:
            >>> l1 = LinkedList()   |   >>> l2 = LinkedList()
            >>> for i in [1,3,5]:   |   >>> for i in ['a','b',"c"]:
            ...     l1.append(i)    |   ...     l2.append(i)
            ...                     |   ...
            >>> print(l1)           |   >>> print(l2)
            [1, 3, 5]               |   ['a', 'b', 'c']
        """
        s = "["
        if self.head is not None:
            cur = self.head
            s += repr(cur.value)
            cur = cur.next
            while cur is not None:
                s += ", " + repr(cur.value)
                cur = cur.next
        return s + "]"
        
        
#        raise NotImplementedError("Problem 3 Incomplete")

    # Problem 4
    def remove(self, data):
        """Remove the first node in the list containing 'data'. Return nothing.

        Raises:
            ValueError: if the list is empty, or does not contain 'data'.

        Examples:
            >>> print(l1)       |   >>> print(l2)
            [1, 3, 5, 7, 9]     |   [2, 4, 6, 8]
            >>> l1.remove(5)    |   >>> l2.remove(10)
            >>> l1.remove(1)    |   ValueError: <message>
            >>> l1.remove(9)    |   >>> l3 = LinkedList()
            >>> print(l1)       |   >>> l3.remove(10)
            [3, 7]              |   ValueError: <message>
        """
        if self.head is None:
            raise ValueError("Cannot remove from empty list")
        
        cur = self.head
        if cur.value == data:
            if cur is self.tail:
                self.tail = None
                self.head = None
            else:
                self.head.prev = None
                self.head = self.head.next
                self.len -= 1
        else:
            cur = cur.next
            while cur is not None:
                if cur.value == data:
                    self.len -= 1
                    if cur is self.tail:
                        self.tail = cur.prev
                        self.tail.next = None
                    else:
                        cur.prev.next = cur.next
                        cur.next.prev = cur.prev
                    return
                cur = cur.next
            
            #if we got here, the element was not found
            raise ValueError("Cannot remove element that is not in the list!")        
         

    # Problem 5
    def insert(self, data, place):
        """Insert a node containing 'data' immediately before the first node
        in the list containing 'place'. Return nothing.

        Raises:
            ValueError: if the list is empty, or does not contain 'place'.

        Examples:
            >>> print(l1)           |   >>> print(l1)
            [1, 3, 7]               |   [1, 3, 5, 7, 7]
            >>> l1.insert(7,7)      |   >>> l1.insert(3, 2)
            >>> print(l1)           |   ValueError: <message>
            [1, 3, 7, 7]            |
            >>> l1.insert(5,7)      |   >>> l2 = LinkedList()
            >>> print(l1)           |   >>> l2.insert(10,10)
            [1, 3, 5, 7, 7]         |   ValueError: <message>
        """
        el = self.find(place)
        new = LinkedListNode(data)
        if el is self.head:
            new.next = el
            el.prev = new
            self.head = new
            self.len += 1
        else:
            new.next = el
            new.prev = el.prev
            el.prev.next = new
            el.prev = new
            self.len += 1
            

l = LinkedList()
#l.find(10)
l.append(1)
l.append("b")
l.insert(2,"b")
print l
# Problem 6: Write a Deque class.


# Problem 7
def prob7(infile, outfile):
    """Reverse the file 'infile' by line and write the results to 'outfile'."""
    pass
    #raise NotImplementedError("Problem 7 Incomplete")
    
    
