#!/bin/python3

"""
This file contains the code under test for the example bug.
The sqrt() method fails on x <= 0.
"""
from math import cos as rcos
from math import sin as rsin
from math import tan as rtan


def sqrt(x):
    """Computes the square root of x, using the Newton-Raphson method"""
    x = max(x, 0)
    approx = None
    guess = x / 2
    while approx != guess:
        approx = guess
        guess = (approx + x / approx) / 2
    return approx


def tan(x):
    return rtan(x)


def cos(x):
    return rcos(x)


def sin(x):
    return rsin(x)


def main(arg):
    return eval(arg)
