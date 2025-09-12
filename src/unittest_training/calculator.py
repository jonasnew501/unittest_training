from typing import Union


class DivisionByZeroError(Exception):
    """
    A custom domain-specific Exception
    for dividing by zero.
    """

    pass


class InvalidInputError(Exception):
    """
    A custom domain-specific Exception
    for providing invalid inputs to functions.
    """




    pass





class Calculator:
    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Divide 'a' by 'b'.

        Args:
            a (int | float): Numerator.
            b (int | float): Denominator.

        Returns:
            float: The result of the division.

        Raises:
            DivisionByZeroError: If denominator is zero.
            InvalidInputError: If a and/or b are not int/float.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise InvalidInputError("Operands must be int or float.")

        if b == 0:
            raise DivisionByZeroError("Denominator cannot be zero.")

        # #New feature: Integer division (return an int when both arguments are of type int)
        # if isinstance(a, int) and isinstance(b, int):
        #     return a // b #returns an int

        return a / b


# print(Calculator.divide(4,2))
# print(type(Calculator.divide(4,2)))
