import pytest

# from ...unittest_training.src.calculator import DivisionByZeroError, Calculator
from calculator import DivisionError, Calculator


class TestCalculator:
    @staticmethod
    def test_divide_valid_inputs():
        assert Calculator.divide(a=2, b=4) == 0.5 #two positive numbers
        assert Calculator.divide(a=2, b=-5) == -0.4 #one positive and one negative number
        assert Calculator.divide(a=-2.5, b=-5) == 0.5 #two negative numbers
        assert Calculator.divide(a=0, b=0.01) == 0 #numerator is zero
