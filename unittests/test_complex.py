from solutions import *
import pytest

@pytest.fixture
def set_up_complex_nums():
 number_1 = ComplexNumber(1, 2)
 number_2 = ComplexNumber(5, 5)
 number_3 = ComplexNumber(2, 9)
 return number_1, number_2, number_3


def test_complex_addition(set_up_complex_nums):
 number_1, number_2, number_3 = set_up_complex_nums
 assert number_1 + number_2 == ComplexNumber(6, 7)
 assert number_1 + number_3 == ComplexNumber(3, 11)
 assert number_2 + number_3 == ComplexNumber(7, 14)
 assert number_3 + number_3 == ComplexNumber(4, 18)

def test_complex_multiplication(set_up_complex_nums):
 number_1, number_2, number_3 = set_up_complex_nums
 assert number_1 * number_2 == ComplexNumber(-5, 15)
 assert number_1 * number_3 == ComplexNumber(-16, 13)
 assert number_2 * number_3 == ComplexNumber(-35, 55)
 assert number_3 * number_3 == ComplexNumber(-77, 36)

def test_complex_division(set_up_complex_nums):
 number_1, number_2, number_3 = set_up_complex_nums
 assert number_1 / number_2 == ComplexNumber(.3, .1)
 assert number_1 / number_3 == ComplexNumber(0.23529411764705882, -0.058823529411764705)
 assert number_3 / number_1 == ComplexNumber(4, 1)
 assert number_3 / number_2 == ComplexNumber(1.1, .7)

def test_complex_subtraction(set_up_complex_nums):
 number_1, number_2, number_3 = set_up_complex_nums
 assert number_1 - number_2 == ComplexNumber(-4,-3)
 assert number_1 - number_3 == ComplexNumber(-1,-7)
 assert number_2 - number_3 == ComplexNumber(3,-4)
 assert number_3 - number_3 == ComplexNumber(0, 0)

def test_complex_norm(set_up_complex_nums):
 number_1, number_2, number_3 = set_up_complex_nums
 assert number_1.norm() == (number_1.real**2 + number_1.imag**2)**.5
 assert number_2.norm() == (number_2.real**2 + number_2.imag**2)**.5
 assert number_3.norm() == (number_3.real**2 + number_3.imag**2)**.5


def test_complex_conjugate(set_up_complex_nums):
 number_1, number_2, number_3 = set_up_complex_nums
 assert number_1.conjugate() == ComplexNumber(1,-2)
 assert number_2.conjugate() == ComplexNumber(5,-5)
 assert number_3.conjugate() == ComplexNumber(2,-9)

