import math


class Temperature:
    """Represent a temperature in Celsius, Fahrenheit, or Kelvin."""

    # Requirement 2: Use this tolerance when comparing floating-point values.
    TOLERANCE = 1e-9

    def __init__(self, value: float, unit: str = "C"):
        # Requirement 1: Accept a temperature value and a unit.
        # Convert the unit to uppercase so 'c', 'C', etc. are accepted.
        unit = unit.upper()

        # Requirement 1: Reject units other than C, F, and K.
        if unit not in ("C", "F", "K"):
            raise ValueError("Unit must be C, F, or K")

        # Convert to Kelvin temporarily to check the absolute-zero limit.
        if unit == "C":
            kelvin = value + 273.15
        elif unit == "F":
            kelvin = (value - 32) * 5 / 9 + 273.15
        else:
            kelvin = value
 
        # Requirement 1 (using requirement 2's tolerance):
        # Reject values that are more than 1e-9 K below absolute zero.
        if kelvin < -self.TOLERANCE:
            raise ValueError("Temperature cannot be below absolute zero")

        # Requirement 3: Store the data privately, behind read-only properties.
        self._value = value
        self._unit = unit

    @property
    def value(self) -> float:
        # Requirement 3: Allow reading, but not assigning, temperature.value.
        return self._value

    @property
    def unit(self) -> str:
        # Requirement 3: Allow reading, but not assigning, temperature.unit.
        return self._unit

    def to_celsius(self) -> float:
        # Requirement 4: Convert the stored temperature to Celsius.
        if self.unit == "C":
            return self.value
        if self.unit == "K":
            return self.value - 273.15
        return (self.value - 32) * 5 / 9

    def to_fahrenheit(self) -> float:
        # Requirement 4: Convert the stored temperature to Fahrenheit.
        if self.unit == "F":
            return self.value
        if self.unit == "C":
            return self.value * 9 / 5 + 32
        return (self.value - 273.15) * 9 / 5 + 32

    def to_kelvin(self) -> float:
        # Requirement 4: Convert the stored temperature to Kelvin.
        if self.unit == "K":
            return self.value
        if self.unit == "C":
            return self.value + 273.15
        return (self.value - 32) * 5 / 9 + 273.15
    def convert_to(self, target_unit: str) -> "Temperature":
        # Requirement 4: Convert to a requested unit, ignoring letter case.
        target_unit = target_unit.upper()
        if target_unit == "C":
            return Temperature(self.to_celsius(), "C")
        if target_unit == "F":
            return Temperature(self.to_fahrenheit(), "F")
        if target_unit == "K":
            return Temperature(self.to_kelvin(), "K")
        # Requirement 4: Invalid target units must raise ValueError.
        raise ValueError("Target unit must be C, F, or K")

    def __repr__(self) -> str:
        # Requirement 5: Provide an unambiguous, developer-friendly form.
        return f"Temperature({self.value!r}, {self.unit!r})"

    def __str__(self) -> str:
        # Requirement 5: Display two decimal places and the degree/unit symbol.
        return f"{self.value:.2f} °{self.unit}" if self.unit != "K" else f"{self.value:.2f} K"

    def _difference(self, other):
        # Requirement 6: Only compare Temperature objects.
        if not isinstance(other, Temperature):
            return NotImplemented
        # Convert both temperatures to Kelvin before comparing them.
        return self.to_kelvin() - other.to_kelvin()

    def __eq__(self, other):
        # Requirement 6: Equality across different units, within tolerance.
        difference = self._difference(other)
        if difference is NotImplemented:
            return NotImplemented
        return math.isclose(difference, 0.0, abs_tol=self.TOLERANCE, rel_tol=0)

    def __ne__(self, other):
        # Requirement 6: Inequality is the opposite of equality.
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        # Requirement 6: Strictly less than, allowing for tolerance.
        difference = self._difference(other)
        if difference is NotImplemented:
            return NotImplemented
        return difference < -self.TOLERANCE

    def __le__(self, other):
        # Requirement 6: Less than or approximately equal to.
        difference = self._difference(other)
        if difference is NotImplemented:
            return NotImplemented
        return difference <= self.TOLERANCE

    def __gt__(self, other):
        # Requirement 6: Strictly greater than, allowing for tolerance.
        difference = self._difference(other)
        if difference is NotImplemented:
            return NotImplemented
        return difference > self.TOLERANCE

    def __ge__(self, other):
        # Requirement 6: Greater than or approximately equal to.
        difference = self._difference(other)
        if difference is NotImplemented:
            return NotImplemented
        return difference >= -self.TOLERANCE
