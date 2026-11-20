"""
INF201 - Deliverable 4, Task 2: Fractions

A Fraction class where both numerator and denominator are integers and the
denominator is strictly positive (> 0). Fractions are always stored in
lowest terms, e.g. Fraction(2, 4) is stored as 1/2.
"""

from math import gcd


class Fraction:
    """A fraction numerator/denominator with integer parts and denominator > 0."""

    # ------------------------------------------------------------------
    # Initialiser
    # ------------------------------------------------------------------
    def __init__(self, numerator, denominator=1):
        # Both parts must be integers (bool is a subclass of int, so we exclude it)
        for part in (numerator, denominator):
            if not isinstance(part, int) or isinstance(part, bool):
                raise TypeError("Numerator and denominator must be integers.")

        # The denominator must be strictly positive
        if denominator <= 0:
            raise ValueError("Denominator must be strictly positive (> 0).")

        # Reduce to lowest terms, e.g. 6/8 -> 3/4
        common = gcd(numerator, denominator)
        self._numerator = numerator // common
        self._denominator = denominator // common

    # Read-only access to numerator and denominator
    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    @staticmethod
    def _to_fraction(other):
        """Convert an int to a Fraction. Return None for unsupported types."""
        if isinstance(other, Fraction):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Fraction(other, 1)
        return None

    @staticmethod
    def _make(numerator, denominator):
        """Create a Fraction, moving a negative sign from the denominator
        to the numerator (needed after division)."""
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        return Fraction(numerator, denominator)

    # ------------------------------------------------------------------
    # Comparisons: a/b ? c/d  <=>  a*d ? c*b  (valid because b, d > 0)
    # ------------------------------------------------------------------
    def __eq__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self.numerator * other.denominator >= other.numerator * self.denominator

    # Equal fractions must have equal hashes (needed because we define __eq__)
    def __hash__(self):
        return hash((self.numerator, self.denominator))

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------
    def __add__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        # a/b + c/d = (a*d + c*b) / (b*d)
        return Fraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def __radd__(self, other):  # supports 1 + Fraction(1, 2)
        return self.__add__(other)

    def __sub__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        # a/b - c/d = (a*d - c*b) / (b*d)
        return Fraction(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator,
        )

    def __rsub__(self, other):  # supports 1 - Fraction(1, 2)
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        # a/b * c/d = (a*c) / (b*d)
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator,
        )

    def __rmul__(self, other):  # supports 2 * Fraction(1, 3)
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by a zero fraction.")
        # (a/b) / (c/d) = (a*d) / (b*c)
        return self._make(
            self.numerator * other.denominator,
            self.denominator * other.numerator,
        )

    # ------------------------------------------------------------------
    # Unary operators and conversions
    # ------------------------------------------------------------------
    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __abs__(self):
        return Fraction(abs(self.numerator), self.denominator)

    def __float__(self):
        return self.numerator / self.denominator

    # ------------------------------------------------------------------
    # String representations
    # ------------------------------------------------------------------
    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"