from typing import Union


class DivisionByZeroError(Exception):
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
        if b == 0:
            raise DivisionByZeroError
        else:
            return a/b
