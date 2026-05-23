class UserCredentialsContainer:
    """
    POJO container class to store dynamic user credentials (username and password)
    generated during the registration process, sharing them with the login steps.
    """
    def __init__(self):
        self._username = None
        self._password = None

    def set_username(self, username: str):
        self._username = username

    def get_username(self) -> str:
        return self._username

    def set_password(self, password: str):
        self._password = password

    def get_password(self) -> str:
        return self._password

# Singleton instance for easy sharing across step definitions
credentials_container = UserCredentialsContainer()
