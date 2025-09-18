import pytest

from unittest_training.calculator_mocking import(
    InvalidInputError,
    CalculatorMocking,
)

class TestCalculatorMocking:
    @staticmethod
    @pytest.mark.parametrize(
        "a, b",
        [
            (4.387, "Hello"), #a is valid, b is invalid
            ("Hello", 7), #a is invalid, b is valid
            ("Hello", "Bye"), #a is invalid, b is invalid
        ]
    )
    def test_multiply_invalid_inputs(a, b):
        with pytest.raises(InvalidInputError, match="Operands must be int or float."):
            CalculatorMocking.multiply(a=a, b=b)
    
    @staticmethod
    def test_multiply_valid_inputs_with_mock(mocker):
        fake_add = mocker.patch("unittest_training.calculator_mocking.CalculatorMocking.add", return_value=10)

        result = CalculatorMocking.multiply(3, 4)

        assert result == 10

        # Did multiply call add() at all?
        assert fake_add.called

        # Did multiply call add exactly 4 times?
        assert fake_add.call_count == 4

        # Did multiply ever call add(0, 3)?
        fake_add.assert_any_call(0, 3)

        # second call should have been add(10, 3) (because first returned 10)
        fake_add.assert_any_call(10, 3)

        #'assert_called_with' checks only for the last-call of the patched object
        fake_add.assert_called_with(10, 3)

        #for inspecting the whole call-history of the patched object
        print(fake_add.call_args_list)

        #------------
        #with 'side_effect's, the mocked function can be made to behave differently
        #each time it is called (when an iterable is assigned as the side_effect)
        fake_add.side_effect = [1, 2, 3]

        result = CalculatorMocking.multiply(3, 3)

        assert result == 3 #3, because the first call of 'add' returns 1, the second call returns 2,
                           #and the third call returns 3
        
        #-----

        #with 'side_effect's, the mocked function can also be made to return an
        #Exception. This is how failures in dependencies (here: the 'add'-function)
        #can be simulated.
        fake_add.side_effect = ValueError("Error!")
        try:
            CalculatorMocking.multiply(3, 3)
        except:
            pass
        #------------

        #Using 'mocker.Mock()' directly
        fake_add = mocker.Mock(return_value=42)

        assert fake_add(1, 2, 3) == 42
        fake_add.assert_called_once_with(1, 2, 3)

        