
import pytest
from fraction import Fraction


# ----------------------------------------------------------------------
# Initialiser
# ----------------------------------------------------------------------
def test_init_stores_values():
    f = Fraction(3, 4)
    assert f.numerator == 3
    assert f.denominator == 4


def test_init_default_denominator():
    f = Fraction(5)
    assert f.numerator == 5
    assert f.denominator == 1


def test_init_reduces_to_lowest_terms():
    f = Fraction(6, 8)
    assert (f.numerator, f.denominator) == (3, 4)


def test_init_negative_numerator():
    f = Fraction(-2, 4)
    assert (f.numerator, f.denominator) == (-1, 2)


def test_init_zero_numerator():
    f = Fraction(0, 5)
    assert (f.numerator, f.denominator) == (0, 1)


@pytest.mark.parametrize("denominator", [0, -1, -5])
def test_init_denominator_not_positive_raises(denominator):
    with pytest.raises(ValueError):
        Fraction(1, denominator)


@pytest.mark.parametrize("numerator, denominator", [
    (1.5, 2), (1, 2.0), ("1", 2), (1, "2"), (True, 2), (None, 1),
])
def test_init_non_integer_raises(numerator, denominator):
    with pytest.raises(TypeError):
        Fraction(numerator, denominator)


def test_attributes_are_read_only():
    f = Fraction(1, 2)
    with pytest.raises(AttributeError):
        f.numerator = 5
    with pytest.raises(AttributeError):
        f.denominator = 5


# ----------------------------------------------------------------------
# Comparisons
# ----------------------------------------------------------------------
def test_eq():
    assert Fraction(1, 2) == Fraction(2, 4)
    assert Fraction(2, 1) == 2
    assert not (Fraction(1, 2) == Fraction(1, 3))


def test_ne():
    assert Fraction(1, 2) != Fraction(1, 3)
    assert not (Fraction(1, 2) != Fraction(3, 6))


def test_lt():
    assert Fraction(1, 3) < Fraction(1, 2)
    assert Fraction(-1, 2) < Fraction(1, 3)
    assert not (Fraction(1, 2) < Fraction(1, 2))


def test_le():
    assert Fraction(1, 3) <= Fraction(1, 2)
    assert Fraction(1, 2) <= Fraction(2, 4)
    assert not (Fraction(2, 3) <= Fraction(1, 2))


def test_gt():
    assert Fraction(3, 4) > Fraction(2, 3)
    assert Fraction(1, 2) > 0
    assert not (Fraction(1, 2) > Fraction(1, 2))


def test_ge():
    assert Fraction(3, 4) >= Fraction(2, 3)
    assert Fraction(2, 4) >= Fraction(1, 2)
    assert not (Fraction(1, 3) >= Fraction(1, 2))


def test_compare_with_other_type():
    # __eq__ returns NotImplemented, so Python falls back to False
    assert (Fraction(1, 2) == "1/2") is False
    assert Fraction(1, 2) != 0.5
    assert Fraction(1, 2).__eq__("1/2") is NotImplemented
    with pytest.raises(TypeError):
        Fraction(1, 2) < "a"


def test_hash_equal_fractions():
    assert hash(Fraction(1, 2)) == hash(Fraction(2, 4))
    assert len({Fraction(1, 2), Fraction(2, 4), Fraction(3, 6)}) == 1


# ----------------------------------------------------------------------
# Arithmetic
# ----------------------------------------------------------------------
def test_add():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    assert Fraction(1, 2) + 1 == Fraction(3, 2)
    assert 1 + Fraction(1, 2) == Fraction(3, 2)


def test_sub():
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)
    assert Fraction(1, 3) - Fraction(1, 2) == Fraction(-1, 6)
    assert 1 - Fraction(1, 4) == Fraction(3, 4)


def test_mul():
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)
    assert Fraction(1, 3) * 3 == 1
    assert 2 * Fraction(1, 4) == Fraction(1, 2)


def test_truediv():
    assert Fraction(1, 2) / Fraction(1, 4) == 2
    assert Fraction(1, 2) / 2 == Fraction(1, 4)


def test_truediv_by_negative_keeps_denominator_positive():
    result = Fraction(1, 2) / Fraction(-1, 3)
    assert result == Fraction(-3, 2)
    assert result.denominator > 0


def test_truediv_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0, 1)


def test_arithmetic_with_other_type_raises():
    with pytest.raises(TypeError):
        Fraction(1, 2) + "a"


# ----------------------------------------------------------------------
# Unary operators and conversions
# ----------------------------------------------------------------------
def test_neg():
    assert -Fraction(1, 2) == Fraction(-1, 2)
    assert -Fraction(-3, 4) == Fraction(3, 4)


def test_abs():
    assert abs(Fraction(-3, 4)) == Fraction(3, 4)
    assert abs(Fraction(3, 4)) == Fraction(3, 4)


def test_float():
    assert float(Fraction(1, 4)) == pytest.approx(0.25)
    assert float(Fraction(-1, 3)) == pytest.approx(-0.333333333)


# ----------------------------------------------------------------------
# String representations
# ----------------------------------------------------------------------
def test_str():
    assert str(Fraction(3, 4)) == "3/4"
    assert str(Fraction(-6, 8)) == "-3/4"


def test_repr():
    assert repr(Fraction(3, 4)) == "Fraction(3, 4)"
    # repr should be valid Python that recreates the same object
    assert eval(repr(Fraction(2, 6))) == Fraction(1, 3)