"""
Python Module to solve fractions without in-built Fraction Module.

Author: Roshaan Mehmood

GitHub: https://github.com/roshaan55/pythmath
"""

from pythmath import absolute, gcd


class Fraction:

    """
    This class simplifies the fraction and solves the fraction.

    It takes two argument numerator and denominator and return its
    fraction value for example if Fraction(2, 4) the fraction will
    be 1/2. The default value of numerator is 0 and the default
    value of denominator is 1.

    It does not support float or string values in Fraction() arguments.
    For Float and string values there are seperate functions defined.

    For Float:
    ---------
        - float_to_frac()
        It takes float value as parameter and returns the value in fraction.
        Example:
            Fraction.float_to_frac(0.25)
            >> 1/4

    For String:
    ----------
        - frac_to_float()
        It takes fraction string as parameter and returns the value in float.
        Examples:
            Fraction.frac_to_float("1/4")
            >> 0.25
            Fraction.frac_to_float("1 1/4")
            >> 1.25


    """

    def __init__(self, numerator=0, denominator=1):

        """
        Simplifies and solves the fractions and performs all the basic
        addition, subtraction, multiplication and division of fractions.

        :param numerator: Value of numerator, defaults to 0
        :param denominator: Value of denominator, defaults to 1
        """

        self.numerator = int(numerator / gcd(absolute(denominator), absolute(numerator)))
        self.denominator = int(denominator / gcd(absolute(denominator), absolute(numerator)))
        if self.denominator < 0:
            self.denominator = absolute(self.denominator)
            self.numerator = -1 * self.numerator
        elif self.denominator == 0:
            raise ZeroDivisionError("Division by Zero")
        elif isinstance(numerator, float) and isinstance(denominator, float):
            raise TypeError("Both numerator and denominator must be of integer type")
        elif isinstance(denominator, float):
            raise TypeError("Denominator must be of integer type")
        elif isinstance(numerator, float):
            raise TypeError("Numerator must be integer value. For float value use float_to_frac function")

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return str(self.numerator) + "/" + str(self.denominator)

    def __rsub__(self, b):
        return self.__sub__(b)

    def __sub__(self, b):
        """a - b"""
        da, db = self.denominator, b.denominator
        return Fraction(self.numerator * db - b.numerator * da,
                        da * db)

    def __add__(self, b):
        """a + b"""
        da, db = self.denominator, b.denominator
        return Fraction(self.numerator * db + b.numerator * da, da * db)

    def __mul__(self, b):
        """a * b"""
        return Fraction(self.numerator * b.numerator, self.denominator * b.denominator)

    def __truediv__(self, b):
        """a / b"""
        return Fraction(self.numerator * b.denominator, self.denominator * b.numerator)

    def __floordiv__(self, b):
        """a // b"""
        return (self.numerator * b.denominator) // (self.denominator * b.numerator)

    def __divmod__(self, b):
        """(a // b, a % b)"""
        da, db = self.denominator, b.denominator
        div, n_mod = divmod(self.numerator * db, da * b.numerator)
        return div, Fraction(n_mod, da * db)

    def __mod__(self, b):
        """a % b"""
        da, db = self.denominator, b.denominator
        return Fraction((self.numerator * db) % (b.numerator * da), da * db)

    @classmethod
    def float_to_frac(cls, flt):
        """
        Converts an exact floating number to proper fraction or improper fraction.

        Proper Fraction: A fraction where the numerator is less than the denominator, then it is known as a
        proper fraction.

        Improper Fraction: A fraction where the numerator is greater than the denominator, then it is known as an
        improper fraction.

        :param flt: Floating Number
        :return: Fraction from a floating number
        """
        if flt == 0.0 or 0:
            return 0
        elif isinstance(flt, float):
            flt_str = str(flt)
            flt_split = flt_str.split('.')
            numerator = int(''.join(flt_split))
            denominator = 10 ** len(flt_split[1])
            return Fraction(numerator, denominator)
        elif not isinstance(flt, float):
            return "Value must be in float(decimal) eg: 0.1"

    @classmethod
    def frac_to_float(cls, frac_str):
        """
        Converts the proper fraction, improper fraction and mixed fraction to exact floating number.

        Proper Fraction: A fraction where the numerator is less than the denominator, then it is known as a
        proper fraction.

        Improper Fraction: A fraction where the numerator is greater than the denominator, then it is known as an
        improper fraction.

        Mixed Fraction: A mixed fraction is the combination of a natural number and fraction. It is basically an
        improper fraction.

        :param frac_str: Fraction string ex: "1 1/2" or "3/5"
        :return: Fraction or mixed(whole) fraction to exact floating number.
        """
        try:
            return float(frac_str)
        except ValueError:
            num, denom = frac_str.split('/')
            try:
                leading, num = num.split(' ')
                whole = float(leading)
            except ValueError:
                whole = 0
            frac = float(num) / float(denom)
            return whole - frac if whole < 0 else whole + frac
