from typing import Union

class InvalidInputError(Exception):
    """
    A custom domain-specific Exception
    for providing invalid inputs to functions.
    """

    pass


class CalculatorMocking:
    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise InvalidInputError("Operands must be int or float.")
        
        return a + b

    @staticmethod
    def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise InvalidInputError("Operands must be int or float.")
        
        result = 0
        for i in range(1, b+1):
            result = CalculatorMocking.add(result, a)
            print(f"Multiply-iteration: {i}")
        
        return result


# print(multiply(3, 4))


