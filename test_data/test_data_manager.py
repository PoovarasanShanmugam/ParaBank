import uuid
import random
from test_data.pojo_models import UserRegistrationData

class TestDataManager:
    """
    Manages static and dynamic test data for positive and negative scenarios.
    """
    # Static invalid login credentials
    INVALID_USERNAMES = ["nonexistent_test_user", "wrong_pb_user", "invalid_admin"]
    INVALID_PASSWORD = "WrongPassword123!"
    
    # Template static details for registration data
    FIRST_NAME = "Poovarasan"
    LAST_NAME = "S"
    ADDRESS = "105,Aarthi Apartment, T Nagar"
    CITY = "Chennai"
    STATE = "Tamil Nadu"
    ZIP_CODE = "600017"

    @classmethod
    def generate_dynamic_registration_data(cls) -> UserRegistrationData:
        """
        Generates a new instance of UserRegistrationData with fully dynamic
        and unique credentials (username, password, phone, and SSN).
        """
        unique_id = uuid.uuid4().hex[:10]
        unique_username = f"pb_{unique_id}"
        dynamic_password = f"Pass_{uuid.uuid4().hex[:8]}"
        
        # Generate random unique phone and SSN numbers
        dynamic_phone = "9" + "".join(random.choices("0123456789", k=9))
        dynamic_ssn = f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
        
        return UserRegistrationData(
            first_name=cls.FIRST_NAME,
            last_name=cls.LAST_NAME,
            address=cls.ADDRESS,
            city=cls.CITY,
            state=cls.STATE,
            zip_code=cls.ZIP_CODE,
            phone=dynamic_phone,
            ssn=dynamic_ssn,
            username=unique_username,
            password=dynamic_password
        )
