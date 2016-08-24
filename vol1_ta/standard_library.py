# standard_library.py
"""Introductory Labs: The Standard Library
<Name> Benjamin Pachev
<Class> Math 321 (TA)
<Date> Aug 24, 2016
"""

import calculator as calc
import box
import sys
import random

# Problem 1
def prob1(l):
    """Accept a list 'l' of numbers as input and return a new list with the
    minimum, maximum, and average of the contents of 'l'.
    """
    return [min(l), max(l), sum(l)/float(len(l))]


# Problem 2
def prob2():
    """Programmatically determine which Python objects are mutable and which
    are immutable. Test numbers, strings, lists, tuples, and dictionaries.
    Print your results to the terminal.
    """
    num = 0
    new_num = num
    new_num += 1
    print "Are numbers mutable? ",num == new_num

    word = "alph"
    new_word = word
    new_word += "a"
    print "Are strings mutable? ",word==new_word

    t = (1)
    new_t = t
    new_t += (1)
    print "Are tuples mutable? ",new_t==t

    l = [1]
    new_l = l
    new_l.append(1)
    print "Are lists mutable? ",l==new_l

    d = {}
    new_d = d
    new_d[1] = 0
    print "Are dicts mutable? ", d == new_d


# Problem 3: Create a 'calculator' module and implement this function.
def prob3(a,b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any methods other than those that are imported from your
    'calculator' module.

    Parameters:
        a (float): the length one of the sides of the triangle.
        b (float): the length the other nonhypotenuse side of the triangle.

    Returns:
        The length of the triangle's hypotenuse.
    """
    return calc.sqrt(calc.add(calc.multiply(a,a), calc.multiply(b,b)))

def prompt(msg):
    """
    Prompt the user for a string input and return the input value.

    Parameters:
        msg -- the prompt name (eg, if msg=Name, the prompt will look like Name: )

    Returns:
        The value input by the user.
    """

    val = ""

    while not len(val):
        val = raw_input(msg+": ")

    return val


def dice_roll(faces=6):
    r = random.randint(1,faces)
    return r

def remove_list(l, exclude):
    s = set(exclude)
    return [x for x in l if x not in exclude]

# Problem 4: Implement shut the box.
if __name__ == "__main__":
    name = ""

    if len(sys.argv) < 2:
        name = prompt("Player name")
    else:
        name = sys.argv[1]

    remaining = range(1,10)

    while True:
        print "Numbers left: ",remaining

        if sum(remaining) > 6:
            #roll two dice
            roll = dice_roll()+dice_roll()
        else:
            #roll only one die
            roll = dice_roll()

        print "Roll: ",roll
        if not box.isvalid(roll, remaining):
            print ("Game over!")
            break

        choices = []

        while not len(choices):
            raw_nums = prompt("Numbers to eliminate")
            choices = box.parse_input(raw_nums, remaining)
            if not len(choices):
                print ("Invalid input")

        remaining = remove_list(remaining, choices)
        if sum(remaining) == 0:
            break

    print "Score for Player %s: %d points" % (name, sum(remaining))
    if sum(remaining) == 0:
        print ("Congratulations! You emptied the box!")
