#!/usr/bin/env python

# Copyright (C) 2010 Kristian B. Oelgaard
#
# This file is part of FFC.
#
# FFC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FFC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with FFC. If not, see <http://www.gnu.org/licenses/>.
#
# First added:  2010-01-06
# Last changed: 2010-02-01

# Pyhton modules
import unittest
import time

# FFC modules
from ffc.quadrature.reduce_operations import expand_operations, reduce_operations
from ffc.quadrature.symbolics import *
from ffc.quadrature.sumobj import _group_fractions
from ffc.cpp import format, set_float_formatting
from ffc.parameters import FFC_PARAMETERS
set_float_formatting(FFC_PARAMETERS['precision'])
from ffc.log import error, push_level, pop_level, CRITICAL

class TestFloatOperators(unittest.TestCase):

    def testFloatOperators(self):
        "Test binary operators"

        f0 = FloatValue(0.0)
        f2 = FloatValue(2.0)
        f3= FloatValue(3.0)
        fm1= FloatValue(-1.0)
        fm3= FloatValue(-3.0)

        x = Symbol("x", GEO)
        y = Symbol("y", GEO)
        z = Symbol("z", GEO)

        p0 = Product([f2, x])
        p1 = Product([x, y])
        p2 = Product([f2, z])
        p3 = Product([y, x, z])
        p4 = Product([fm1, f2, x])

        S0 = Sum([p0, fm3])
        S1 = Sum([x, y])
        S2 = Sum([S1, fm3])
        S3 = Sum([p4, fm3])
        S4 = Sum([fm3, Product([fm1, Sum([x, y])])])

        F0 = Fraction(f2, y)
        F1 = Fraction(FloatValue(-1.5), x)
        F2 = Fraction(fm3, S1)

        SF0 = Sum([f3, F1])
        SF1 = Sum([f3, Product([fm1, F1])])

        # Test FloatValue '+'
        self.assertEqual(str(f2 + fm3), str(fm1))
        self.assertEqual(str(f2 + fm3 + fm3 + f2 + f2), str(f0))
        self.assertEqual(str(f0 + p0), str(p0))
        self.assertEqual(str(fm3 + p0), str(S0))
        self.assertEqual(str(fm3 + S1), str(S2))
        self.assertEqual(str(f3 + F1), str(SF0))

        # Test FloatValue '-'
        self.assertEqual(str(f2 - fm3), str(FloatValue(5)))
        self.assertEqual(str(f0 - p0), str(p4))
        self.assertEqual(str(fm3 - p0), str(S3))
        self.assertEqual(str(fm3 - S1), str(S4))
        self.assertEqual(str(f3 - F1), str(SF1))

        # Test FloatValue '*', only need one because all other cases are
        # handled by 'other'
        self.assertEqual(str(f2*f2), '%s' % format["float"](4))

        # Test FloatValue '/'
        self.assertEqual(str(fm3/f2), str(FloatValue(-1.5)))
        self.assertEqual(str(f2/y), str(F0))
        self.assertEqual(str(fm3/p0), str(F1))
        self.assertEqual(str(fm3/S1), str(F2))
        # Silence output
        push_level(CRITICAL)
        self.assertRaises(Exception, f2.__div__, F0)
        self.assertRaises(Exception, f2.__div__, f0)
        self.assertRaises(Exception, f2.__div__, Product([f0, y]))
        pop_level()


if __name__ == "__main__":

    # Run all returned tests
    runner = unittest.TextTestRunner()
    runner.run(TestFloatOperators('testFloatOperators'))

