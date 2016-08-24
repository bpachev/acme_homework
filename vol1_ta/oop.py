# oop.py
"""Introductory Labs: Object Oriented Programming.
<Name> Benjamin Pachev
<Class> Math 321 (TA)
<Date> Aug 24, 2016
"""

class Backpack(object):
    """A Backpack object class. Has a name and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        contents (list): the contents of the backpack.
    """

    # Problem 1: Modify __init__() and put(), and write dump().
    def __init__(self, name, color, max_size = 5):
        """Set the name and initialize an empty contents list.

        Inputs:
            name (str): the name of the backpack's owner.

        Returns:
            A Backpack object wth no contents.
        """
        self.name = name
        self.color = color
        self.max_size = max_size
        self.contents = []

    def put(self, item):
        """Add 'item' to the backpack's list of contents."""
        if len(self.contents) >= self.max_size:
            print "No Room!"
        else:
            self.contents.append(item)


    def take(self, item):
        """Remove 'item' from the backpack's list of contents."""
        self.contents.remove(item)

    def dump(self):
        self.contents = []

    # Magic Methods -----------------------------------------------------------

    # Problem 3: Write __eq__() and __str__().
    def __add__(self, other):
        """Add the number of contents of each Backpack."""
        return len(self.contents) + len(other.contents)

    def __lt__(self, other):
        """Compare two backpacks. If 'self' has fewer contents
        than 'other', return True. Otherwise, return False.
        """
        return len(self.contents) < len(other.contents)

    def __eq__(self, other):
        """Compare two backpacks by name, color, and number of contents"""
        return self.name == other.name and self.color == other.color and len(self.contents) == len(other.contents)

    def __str__(self):
        res = "Owner:\t\t%s\nColor:\t\t%s\nSize:\t\t%d\nMax Size:\t%d\nContents:\t%s"
        return res % (self.name, self.color, len(self.contents), self.max_size, str(self.contents))

def test_backpack():
    testpack = Backpack("Barry", "black") # Instantiate the object.
    if testpack.max_size != 5: # Test an attribute.
        print("Wrong default max_size!")
    for item in ["pencil", "pen", "paper", "computer"]:
        testpack.put(item) # Test a method.
    print(testpack.contents)

# An example of inheritance. You are not required to modify this class.
class Knapsack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit
            in the knapsack.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """
    def __init__(self, name, color, max_size=3):
        """Use the Backpack constructor to initialize the name, color,
        and max_size attributes. A knapsack only holds 3 item by default
        instead of 5.

        Inputs:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit
                in the knapsack. Defaults to 3.

        Returns:
            A Knapsack object with no contents.
        """
        Backpack.__init__(self, name, color, max_size)
        self.closed = True

    def put(self, item):
        """If the knapsack is untied, use the Backpack.put() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.put(self, item)

    def take(self, item):
        """If the knapsack is untied, use the Backpack.take() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.take(self, item)


# Problem 2: Write a 'Jetpack' class that inherits from the 'Backpack' class.
class Jetpack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit
            in the knapsack.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """
    def __init__(self, name, color, max_size=2, fuel=10):
        """Use the Backpack constructor to initialize the name, color,
        and max_size attributes. A jetpack only holds 2 item by default
        instead of 5.

        Inputs:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit
                in the jetpack. Defaults to 2.
            fuel (int): the amount of fuel the jetpack starts with

        Returns:
            A Jetpack object with no contents.
        """
        Backpack.__init__(self, name, color, max_size)
        self.fuel = fuel

    def fly(self, num_fuel):
        """Spend num_fuel amount of fuel if num_fuel <= fuel."""
        if num_fuel <= self.fuel:
            self.fuel -= num_fuel
        else:
            print ("Not enough fuel!")



    def dump(self):
        """Dump the contents and empty the fuel."""
        self.fuel = 0
        Backpack.dump(self)

def test_jetpack():
    j = Jetpack("Bob", "red")
    print j.fuel == 10
    j.fly(6)
    print j.fuel == 4
    j.fly(6)
    j.dump()
    print j.fuel == 0

# Problem 4: Write a 'ComplexNumber' class.
class ComplexNumber():
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __add__(self, other):
        return ComplexNumber(self.real+other.real, self.imag+other.imag)

    def __mul__(self, other):
        return ComplexNumber(self.real*other.real-self.imag*other.imag, self.real*other.imag + other.real * self.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag-other.imag)

    def __abs__(self):
        return (self.real**2 + self.imag**2) ** .5

    def __div__(self, other):
        d = abs(other)**2
        res = self * other.conjugate()
        res.imag /= d
        res.real /= d
        return res

    def __str__(self):
        return "%f + %fj"%(self.real, self.imag)

    def __repr__(self):
        return str(self)
