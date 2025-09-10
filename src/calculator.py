from typing import Union


class DivisionError(Exception):
    '''
    A custom domain-specific Exception.
    '''
    pass


class Calculator:
    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        '''
        Divides 'a' by 'b'.

        Params:
        - a: The numerator
        - b: The denominator

        Returns:
        - The result of the division, if b != 0
        - A custom 'DivisionByZeroError' if b == 0.
        '''
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise DivisionError
        if b == 0:
            raise DivisionError
        else:
            return a/b


print(Calculator.divide(2,0))
