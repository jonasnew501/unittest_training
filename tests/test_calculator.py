import pytest

# from ...unittest_training.src.calculator import DivisionByZeroError, Calculator
from calculator import DivisionByZeroError, Calculator


class TestCalculator:
    @staticmethod
    def test_divide_valid_inputs():
        assert Calculator.divide(a=2, b=4) == 0.5 #two integers, two positive numbers, two even numbers
