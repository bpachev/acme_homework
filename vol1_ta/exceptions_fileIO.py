# exceptions_fileIO.py
"""Introductory Labs: Exceptions and File I/O.
<Name>
<Class>
<Date>
"""
from random import choice
import os

# Problem 1
def arithmagic():
    step_1 = raw_input("Enter a 3-digit number where the first and last "
                                            "digits differ by 2 or more: ")
    if len(step_1) != 3: raise ValueError("The first number has length not equal to 3.")
    if abs(int(step_1[2])-int(step_1[0])) < 2: raise ValueError ("The difference of the first and last digit is less than two.")

    step_2 = raw_input("Enter the reverse of the first number, obtained "
                                            "by reading it backwards: ")
    if step_2 != step_1[::-1]: raise ValueError("The first number is not the reverse of the second.")

    step_3 = raw_input("Enter the positive difference of these numbers: ")
    if int(step_3) != abs(int(step_2)-int(step_1)): raise ValueError("The third number isn't the positive difference of the first two.")
    step_4 = raw_input("Enter the reverse of the previous result: ")
    if step_4 != step_3[::-1]: raise ValueError("The fourth number is not the reverse of the third.")
    print str(step_3) + " + " + str(step_4) + " = 1089 (ta-da!)"


# Problem 2
def random_walk(max_iters=1e12):
    walk = 0
    direction = [-1, 1]
    try:
        for i in xrange(int(max_iters)):
            walk += choice(direction)
    except KeyboardInterrupt:
        print "Process Interrupted at iteration %d" % i
    else:
        print "Process Completed"

    return walk

# Problems 3 and 4: Write a 'ContentFilter' class.

class ContentFilter():
    validModes = {"w", "a"}

    def __init__(self, fname):
        if not isinstance(fname, str):
            raise TypeError("The filename must be a string")

        self.fname = fname

        with open(fname, "r") as f:
            self.contents = f.read()

        self.word_list = [l.split() for l in self.contents.splitlines()]
        self.compute_stats()

    @staticmethod
    def check_mode(mode):
        if mode not in ContentFilter.validModes:
            raise ValueError("Invalid mode \"%s\" for writing" % mode)

    def uniform(self, fname, mode="w", case="upper"):
        self.check_mode(mode)
        new_contents = ""
        if case == "upper":
            new_contents = self.contents.upper()
        elif case == "lower":
            new_contents = self.contents.lower()
        else:
            raise ValueError("Invalid case " + str(case))

        with open(fname, mode) as f:
            f.write(new_contents)

    def reverse(self, fname, mode="w", unit="line"):
        self.check_mode(mode)
        if unit == "line":
            with open(fname, mode) as f:
                for l in reversed(self.word_list):
                    f.write()

    def transpose(self, fname, mode = "w"):
        self.check_mode(mode)

    def compute_stats(self):
        self.num_lines = len(self.word_list)
        self.num_digits = sum(c.isdigit() for c in self.contents)
        self.num_alpha = sum(c.isalpha() for c in self.contents)
        self.num_space = sum(c.isspace() for c in self.contents)
        self.num_chars = len(self.contents)

    def __str__(self):
        res = "Source file:\t{}\nTotal characters:\t{}\n"\
        "Alphabetic characters:\t{}\nNumerical characters:\t{}\nWhitespace characters:\t{}\n"\
        "Number of lines\t{}"
        return res.format(self.fname, self.num_chars, self.num_alpha, self.num_digits, self.num_space, self.num_lines)

    def __repr__(self):
        return str(self)

cf = ContentFilter("test.txt")
cf.reverse("out.txt")
print cf
