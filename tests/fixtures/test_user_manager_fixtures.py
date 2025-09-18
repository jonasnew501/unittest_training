import pytest

from unittest_training.fixtures.user_manager_fixtures import (
    DuplicateUserError,
    InvalidInputError,
    MissingUserError,
    UserManager,
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
        "username, email",
        [
            ("Jonas Neumayer", 3.5),  # valid username, invalid email
            (384, "jonas.neumayer@test.de"),  # invalid username, valid email
            (3249, 294.32),  # invalid username, invalid email
        ],
    )
    def test_addUser_invalid_inputs(user_manager: UserManager, username, email):
        with pytest.raises(
            InvalidInputError,
            match="Both 'username' and 'email' need to be of type 'str'.",
        ):
            user_manager.addUser(username=username, email=email)

    @staticmethod
    def test_addUser_duplicate_user(user_manager: UserManager):
        # user_manager = UserManager()
        user_manager.addUser(username="Jonas Neumayer", email="jonas.neumayer@test.de")
        with pytest.raises(DuplicateUserError, match="User already exists."):
            user_manager.addUser(
                username="Jonas Neumayer", email="another.email@test.de"
            )

    @staticmethod
    @pytest.mark.parametrize(
        "username, email, expected_bool",
        [
            ("Jonas Neumayer", "jonas.neumayer@test.de", True),
            ("Test Person", "test.person@test.de", True),
        ],
    )
    def test_addUser_getUserEmail_valid_inputs(
        user_manager: UserManager, username, email, expected_bool
    ):
        # user_manager = UserManager()
        # assert user_manager.addUser(username="Jonas Neumayer", email="jonas.neumayer@test.de") == True
        # assert user_manager.getUserEmail(username="Jonas Neumayer") == "jonas.neumayer@test.de"

        assert user_manager.addUser(username=username, email=email) == expected_bool
        assert user_manager.getUserEmail(username=username) == email

    @staticmethod
    def test_getUserEmail_invalid_input(user_manager: UserManager):
        user_manager.addUser(username="Jonas Neumayer", email="jonas.neumayer@test.de")
        with pytest.raises(
            InvalidInputError, match="'username' needs to be of type 'str'."
        ):
            user_manager.getUserEmail(username=254.2418)

    @staticmethod
    def test_getUserEmail_missing_user(user_manager: UserManager):
        user_manager.addUser(username="Jonas Neumayer", email="jonas.neumayer@test.de")
        with pytest.raises(
            MissingUserError,
            match="The user you look for is not contained in the database.",
        ):
            user_manager.getUserEmail(username="Another User")
