import pytest

from unittest_training.user_manager_fixtures import (
    DuplicateUserError,
    InvalidInputError,
    UserManager
)


# user_manager = UserManager()

class TestUserManager:

    @staticmethod
    @pytest.fixture
    def user_manager() -> UserManager:
        """
        Creates a new instance of 'UserManager'

        Returns:
            UserManager: The new instance of UserManager.
        """
        return UserManager()

    @staticmethod
    @pytest.mark.parametrize(
        "username, email, expected_bool",
        [
            ("Jonas Neumayer", "jonas.neumayer@test.de", True),
            ("Test Person", "test.person@test.de", True),
        ],
    )
    def test_addUser_new_user(user_manager:UserManager, username, email, expected_bool):
        # user_manager = UserManager()
        # assert user_manager.addUser(username="Jonas Neumayer", email="jonas.neumayer@test.de") == True
        # assert user_manager.getUserEmail(username="Jonas Neumayer") == "jonas.neumayer@test.de"
        
        assert user_manager.addUser(username=username, email=email) == expected_bool
        assert user_manager.getUserEmail(username=username) == email
    
    @staticmethod
    def test_addUser_duplicate_user(user_manager:UserManager):
        # user_manager = UserManager()
        user_manager.addUser(username="Jonas Neumayer", email="jonas.neumayer@test.de")
        with pytest.raises(DuplicateUserError, match="User already exists."):
            user_manager.addUser(username="Jonas Neumayer", email="another.email@test.de")



