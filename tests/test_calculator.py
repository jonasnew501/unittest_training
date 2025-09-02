import pytest

from calculator import DivisionByZeroError, Calculator


class TestCalculator:
    @staticmethod
    def test_divide_valid_inputs():
        assert Calculator.divide(a=2, b=4) == 2 #two integers, two positive numbers, two even numbers
