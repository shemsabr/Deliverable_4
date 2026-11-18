import pytest

from temperature import Temperature


# Test requirement 1: Celsius is the default unit, and units ignore case.
def test_initialization():
    assert Temperature(25).unit == "C"
    assert Temperature(25, "f").unit == "F"
    assert Temperature(25, "k").unit == "K"


# Test requirement 3: value and unit can be read but not reassigned.
def test_read_only_attributes():
    temperature = Temperature(25, "C")
    assert temperature.value == 25
    assert temperature.unit == "C"
    with pytest.raises(AttributeError):
        temperature.value = 30
    with pytest.raises(AttributeError):
        temperature.unit = "F"


# Test requirement 1: Invalid units must raise ValueError.
def test_invalid_units():
    for unit in ("X", "Celsius", ""):
        with pytest.raises(ValueError):
            Temperature(25, unit)
    with pytest.raises(ValueError):
        Temperature(25).convert_to("X")


# Test requirement 1: No temperature may be below absolute zero.
@pytest.mark.parametrize("value, unit", [(-273.16, "C"), (-459.68, "F"), (-0.01, "K")])
def test_below_absolute_zero(value, unit):
    with pytest.raises(ValueError):
        Temperature(value, unit)


# Test requirement 4: All five reference points in the assignment.
@pytest.mark.parametrize("celsius, fahrenheit, kelvin", [
    (-273.15, -459.67, 0),   # Absolute zero
    (-40, -40, 233.15),      # Celsius-Fahrenheit crossover
    (0, 32, 273.15),        # Freezing point of water
    (37, 98.6, 310.15),     # Human body temperature
    (100, 212, 373.15),    # Boiling point of water
])
def test_reference_conversions(celsius, fahrenheit, kelvin):
    for temp in (Temperature(celsius, "C"), Temperature(fahrenheit, "F"), Temperature(kelvin, "K")):
        assert temp.to_celsius() == pytest.approx(celsius, abs=1e-9)
        assert temp.to_fahrenheit() == pytest.approx(fahrenheit, abs=1e-9)
        assert temp.to_kelvin() == pytest.approx(kelvin, abs=1e-9)


# Test requirement 4: C -> F -> K -> C must reproduce the starting value.
def test_round_trip():
    original = Temperature(37, "C")
    final = original.convert_to("f").convert_to("K").convert_to("c")
    assert final == original
    assert final.unit == "C"
    assert final.value == pytest.approx(original.value, abs=1e-9)


# Test requirement 4: convert_to returns a new object, not the original.
def test_convert_to_returns_new_temperature():
    original = Temperature(0, "C")
    converted = original.convert_to("f")
    assert converted is not original
    assert converted.unit == "F"
    assert converted.value == pytest.approx(32)


# Test requirements 2 and 6: Equality uses the specified tolerance.
def test_floating_point_tolerance():
    assert Temperature(273.15, "K") == Temperature(273.15 + 5e-10, "K")
    assert Temperature(273.15, "K") != Temperature(273.15 + 2e-9, "K")



# Test requirement 6: All six operators work with mixed units.
def test_cross_unit_comparisons():
    freezing_c = Temperature(0, "C")
    freezing_f = Temperature(32, "F")
    boiling_k = Temperature(373.15, "K")
    assert freezing_c == freezing_f
    assert not (freezing_c != freezing_f)
    assert freezing_c < boiling_k
    assert freezing_f <= boiling_k
    assert boiling_k > freezing_c
    assert boiling_k >= freezing_f
    assert freezing_c <= freezing_f
    assert freezing_f >= freezing_c


# Test requirement 6: Comparisons with other types return NotImplemented.
@pytest.mark.parametrize("method", ["__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__"])
def test_non_temperature_comparison(method):
    assert getattr(Temperature(0), method)(42) is NotImplemented


# Test requirement 5: String output and developer representation.
def test_string_formatting():
    assert str(Temperature(25, "C")) == "25.00 °C"
    assert str(Temperature(273.15, "K")) == "273.15 K"
    assert repr(Temperature(25.0, "C")) == "Temperature(25.0, 'C')"

