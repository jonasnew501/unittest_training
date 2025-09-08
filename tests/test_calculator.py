import pytest

from calculator import DivisionByZeroError, InvalidInputError, Calculator


class TestCalculator:
    # @staticmethod
    # #The version of this function without pytests parameterization
    # def test_divide_valid_inputs():
    #     assert Calculator.divide(a=2, b=4) == 0.5 #two positive numbers
    #     assert Calculator.divide(a=2, b=-5) == -0.4 #one positive and one negative number
    #     assert Calculator.divide(a=-2.5, b=-5) == 0.5 #two negative numbers (one is float)
    #     assert Calculator.divide(a=0, b=0.01) == 0 #numerator is zero (denominator is float)
    
    @staticmethod
    #The version of this function with pytests parameterization
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 4, 0.5), #two positive numbers
            (2, -5, -0.4), #one positive and one negative number
            (-2.5, -5, 0.5), #two negative numbers (one is float)
            (0, 0.01, 0), #numerator is zero (denominator is float)
        ]
    )
    def test_divide_valid_inputs_correct_result(a, b, expected):
        assert Calculator.divide(a, b) == expected
    
    
    @staticmethod
    #The version of this function with pytests parameterization
    @pytest.mark.parametrize(
        "a, b",
        [
            (2, 4), #two positive numbers
            (2, -5), #one positive and one negative number
            (-2.5, -5), #two negative numbers (one is float)
            (0, 0.01), #numerator is zero (denominator is float)
        ]
    )
    def test_divide_valid_inputs_correct_datatype(a, b):
        assert isinstance(Calculator.divide(a, b), float)

    
    @staticmethod
    def test_divide_denominator_zero():
        with pytest.raises(DivisionByZeroError):
            Calculator.divide(a=2.4, b=0) #numerator positive, denominator zero

        with pytest.raises(DivisionByZeroError):
            Calculator.divide(a=-2.4, b=0) #numerator negative, denominator zero

        with pytest.raises(DivisionByZeroError):
            Calculator.divide(a=0, b=0) #numerator zero, denominator zero
        
        with pytest.raises(DivisionByZeroError):
            Calculator.divide(a=0, b=-0) #numerator zero, denominator negative zero
    
    @staticmethod
    def test_divide_invalid_input_types():
        with pytest.raises(InvalidInputError):
            Calculator.divide(a=2.4, b="Hello") #one valid input, one invalid input
        
        with pytest.raises(InvalidInputError):
            Calculator.divide(a="Hello", b="Hello") #two valid inputs