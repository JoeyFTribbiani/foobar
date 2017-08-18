'''
Problem
Disorderly Escape
=================

Oh no! You've managed to free the bunny prisoners and escape Commander Lambdas exploding space station, but her team of elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll be shot out of the sky!

Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted her space station in the middle of a quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial bodies in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations each quadrant could possibly have, so that you can pick the optimal quadrant through which youll make your jump.

There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid, configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations, if you exchange the position of any two columns or any two rows some number of times, youll find that all of those configurations are equivalent in that way - in grouping, rather than order.

Write a function answer(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations that can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states. Equivalency is defined as above: any two star grids with each celestial body in the same state where the actual order of the rows and columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width and height of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each grid, the number of states of those bodies is between 2 and 20, inclusive. The answer can be over 20 digits long, so return it as a decimal string.  The intermediate values can also be large, so you will likely need to use at least 64-bit integers.

For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent) or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.

00
00

In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or column would keep it in the same state.

00 00 01 10
01 10 00 00

1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 4 positions.  All four of the above configurations are equivalent.

00 11
11 00

2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply moves them between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row with two bodies in state 1, and two columns with one of each state.

01 10
01 10

2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because there's no way to transpose the grid.

01 10
10 01

2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent to each other.

01 10 11 11
11 11 01 10

3 noisy celestial bodies, similar to the case where only one of four is noisy.

11
11

4 noisy celestial bodies.

There are 7 distinct, non-equivalent grids in total, so answer(2, 2, 2) would return 7.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) w = 2
    (int) h = 2
    (int) s = 2
Output:
    (string) "7"

Inputs:
    (int) w = 2
    (int) h = 3
    (int) s = 4
Output:
    (string) "430"

'''


'''
This problem is kinda math problems.
I searched some infos online to help me to understand.
Give credit to
https://math.stackexchange.com/questions/2113657/burnsides-lemma-applied-to-grids-with-interchanging-rows-and-columns
This solution applies Burnside's Lemma.
'''

import fractions
import copy
import collections


class TermItem(object):
    def __init__(self, coefficient=fractions.Fraction(1.0), item=None):
        self.coefficient = coefficient
        if not item:
            self.item = collections.defaultdict(int)
        else:
            self.item = item


def lcm(a, b):
    return abs(a * b) / fractions.gcd(a, b) if a and b else 0


def add(a, b):
    c = a + b
    for i in range(len(c) - 1):
        for j in range(i + 1, len(c)):
            if set(c[i].item.items()) == set(c[j].item.items()):
                c[i].coefficient += c[j].coefficient
                c[j].coefficient = fractions.Fraction(0.0)
    return [item for item in c if item.coefficient != fractions.Fraction(0.0)]


def multiplyTerm(termItem, term):
    c = copy.deepcopy(term)
    for it in c:
        for sub, n in termItem.item.items():
            it.item[sub] += n
    return c


cycleIndexCache = {}


# create cycle index symmetric group
def cycleIndexSymM(n):
    global cycleIndexCache
    if n == 0:
        return [TermItem()]

    if n in cycleIndexCache:
        return cycleIndexCache[n]

    term = []
    for i in range(1, n + 1):
        term = add(term, multiplyTerm(TermItem(fractions.Fraction(1.0), {i: 1}), cycleIndexSymM(n - i)))
    for item in term:
        item.coefficient *= fractions.Fraction(1, n)
    cycleIndexCache[n] = term
    return cycleIndexCache[n]


def cycleIndexSymMN(m, n):
    termM = cycleIndexSymM(m)
    termN = cycleIndexSymM(n)

    term = []

    for itemM in termM:
        for itemN in termN:
            term += TermItem(itemM.coefficient * itemN.coefficient, cyclesProd(itemM.item, itemN.item)),
    return term


# merge items from cycle A and cycle B
def cyclesProd(itemA, itemB):
    l = collections.defaultdict(int)
    for la, insa in itemA.items():
        for lb, insb in itemB.items():
            lcmV = lcm(la, lb)
            l[lcmV] += la * insa * lb * insb / lcmV

    return l


def answer(w, h, s):
    term = cycleIndexSymMN(w, h)

    res = 0
    for termItem in term:
        expo = 0
        for e in termItem.item.values():
            expo += e
        res += termItem.coefficient * s ** expo
    return int(res)

