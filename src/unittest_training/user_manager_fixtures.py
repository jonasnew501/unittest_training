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


class UserManager:
    """
    Manages a collection of users.

    For every user, their full name and accompanying email-address are stored.
    """

    def __init__(self):
        self.users = {}

    def addUser(self, username: str, email: str) -> bool:
        if not isinstance(username, str) and not isinstance(email, str):
            raise InvalidInputError("Both 'username' and 'email' need to be of type 'str'.")

        if username in self.users:
            raise DuplicateUserError("User already exists.")
        
        self.users[username] = email
        return True

    def getUser(self, username) -> dict:
        if username in self.users:
            self.users.get(key=username)
