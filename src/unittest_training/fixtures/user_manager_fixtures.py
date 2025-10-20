class DuplicateUserError(Exception):
    """
    A custom domain-specific exception for the case of a duplicate user.
    """

    pass


class InvalidInputError(Exception):
    """
    A custom domain-specific Exception
    for providing invalid inputs to functions.
    """

    pass


class MissingUserError(Exception):
    """
    A custom domain-specific Exception
    for when a requested user is not contained in the database.
    """

    pass


class UserManager:
    """
    Manages a collection of users.

    For every user, their full name and accompanying email-address are stored.
    """

    def __init__(self):
        self.users = {}

    def addUser(self, username: str, email: str) -> bool:
        if not isinstance(username, str) or not isinstance(email, str):
            raise InvalidInputError(
                "Both 'username' and 'email' need to be of type 'str'."
            )

        if username in self.users:
            raise DuplicateUserError("User already exists.")

        self.users[username] = email
        return True

    def getUserEmail(self, username) -> str:
        if not isinstance(username, str):
            raise InvalidInputError("'username' needs to be of type 'str'.")

        if username not in self.users:
            raise MissingUserError(
                "The user you look for is not contained in the database."
            )

        return self.users.get(username)


user_manager = UserManager()
user_manager.addUser(username="Max Mustermann", email="max.mustermann@test.de")
print(user_manager.users)
print(user_manager.getUserEmail(username="Max Mustermann"))
print(user_manager.users)
