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

        assert result == 10