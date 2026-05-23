from dataclasses import dataclass

@dataclass
class UserRegistrationData:
    """
    Dataclass for user registration data.
    """
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone: str
    ssn: str
    username: str
    password: str
