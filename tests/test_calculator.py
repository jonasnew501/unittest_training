import pytest

from calculator import DivisionByZeroError, InvalidInputError, Calculator


class TestCalculator:
    @staticmethod
    def test_divide_valid_inputs():
        assert Calculator.divide(a=2, b=4) == 0.5 #two positive numbers
        assert Calculator.divide(a=2, b=-5) == -0.4 #one positive and one negative number
        assert Calculator.divide(a=-2.5, b=-5) == 0.5 #two negative numbers (one is float)
        assert Calculator.divide(a=0, b=0.01) == 0 #numerator is zero (one is float)
    
    @staticmethod
    def test_divide_denominator_zero():
        with pytest.raises(DivisionByZeroError):
            Calculator.divide(a=2.4, b=0)
    
    @staticmethod
    def test_divide_invalid_input_types():
        with pytest.raises(InvalidInputError):
            Calculator.divide(a=2.4, b="Hello") #one valid input, one invalid input
        
        with pytest.raises(InvalidInputError):
            Calculator.divide(a="Hello", b="Hello") #two valid inputs