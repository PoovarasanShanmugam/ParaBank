from pom.base_page import BasePage
from test_data.pojo_models import UserRegistrationData

class RegisterPage(BasePage):
    """
    Page Object class for the user registration form.
    """
    FORM_CONTAINERS = [
        "form[id='customerForm']",
        "form#customerForm",
        "#customerForm"
    ]
    
    FIRST_NAME_INPUTS = [
        "form#customerForm input[id='customer.firstName']",
        "input[name='customer.firstName']",
        "#customer\\.firstName"
    ]
    LAST_NAME_INPUTS = [
        "form#customerForm input[id='customer.lastName']",
        "input[name='customer.lastName']",
        "#customer\\.lastName"
    ]
    STREET_INPUTS = [
        "form#customerForm input[id='customer.address.street']",
        "input[name='customer.address.street']",
        "input[id='customer.address.street']"
    ]
    CITY_INPUTS = [
        "form#customerForm input[id='customer.address.city']",
        "input[name='customer.address.city']",
        "input[id='customer.address.city']"
    ]
    STATE_INPUTS = [
        "form#customerForm input[id='customer.address.state']",
        "input[name='customer.address.state']",
        "input[id='customer.address.state']"
    ]
    ZIP_INPUTS = [
        "form#customerForm input[id='customer.address.zipCode']",
        "input[name='customer.address.zipCode']",
        "input[id='customer.address.zipCode']"
    ]
    PHONE_INPUTS = [
        "form#customerForm input[id='customer.phoneNumber']",
        "input[name='customer.phoneNumber']",
        "input[id='customer.phoneNumber']"
    ]
    SSN_INPUTS = [
        "form#customerForm input[id='customer.ssn']",
        "input[name='customer.ssn']",
        "input[id='customer.ssn']"
    ]
    USERNAME_INPUTS = [
        "form#customerForm input[id='customer.username']",
        "input[name='customer.username']",
        "input[id='customer.username']"
    ]
    PASSWORD_INPUTS = [
        "form#customerForm input[id='customer.password']",
        "input[name='customer.password']",
        "input[id='customer.password']"
    ]
    CONFIRM_PASSWORD_INPUTS = [
        "form#customerForm input[id='repeatedPassword']",
        "input[name='repeatedPassword']",
        "input[id='repeatedPassword']"
    ]
    REGISTER_BUTTONS = [
        "form#customerForm input[value='Register']",
        "input[type='submit'][value='Register']",
        "input.button[value='Register']"
    ]
    
    # Using :has-text prevents reading the registration form instructions pre-submission
    CONFIRMATION_TEXTS = [
        "div[id='rightPanel'] p:has-text('Your account was created successfully')",
        "div#rightPanel p:has-text('Your account was created successfully')",
        "#rightPanel p:has-text('Your account was created successfully')",
        "div[id='rightPanel'] p"
    ]
    
    ERROR_TEXTS = [
        "span.error",
        "td span.error",
        "//span[@class='error']"
    ]

    def wait_for_form(self):
        """Waits for the registration form container to load completely."""
        print("[REGISTER PAGE] Waiting for registration form to load...")
        self.wait_for_selector_with_fallback(self.FORM_CONTAINERS)

    def register_user(self, user_data: UserRegistrationData, password_to_confirm: str = None):
        """
        Fills out the registration form details and submits the form.
        Uses Enter key press on the confirm password field to avoid double-submit bugs,
        falling back to a direct click if needed.
        """
        self.wait_for_form()
        print(f"[REGISTER PAGE] Registering user username: {user_data.username}")
        
        self.fill_with_fallback(self.FIRST_NAME_INPUTS, user_data.first_name)
        self.fill_with_fallback(self.LAST_NAME_INPUTS, user_data.last_name)
        self.fill_with_fallback(self.STREET_INPUTS, user_data.address)
        self.fill_with_fallback(self.CITY_INPUTS, user_data.city)
        self.fill_with_fallback(self.STATE_INPUTS, user_data.state)
        self.fill_with_fallback(self.ZIP_INPUTS, user_data.zip_code)
        self.fill_with_fallback(self.PHONE_INPUTS, user_data.phone)
        self.fill_with_fallback(self.SSN_INPUTS, user_data.ssn)
        self.fill_with_fallback(self.USERNAME_INPUTS, user_data.username)
        
        # Fill password
        self.fill_with_fallback(self.PASSWORD_INPUTS, user_data.password)
        
        # Confirm password can be different for negative tests
        confirm_pass = password_to_confirm if password_to_confirm is not None else user_data.password
        self.fill_with_fallback(self.CONFIRM_PASSWORD_INPUTS, confirm_pass)
        
        # Submit the form using Enter keypress to prevent Playwright button click double-submits
        try:
            confirm_locator = self.page.locator(self.CONFIRM_PASSWORD_INPUTS[0]).first
            confirm_locator.press("Enter")
            print("[REGISTER PAGE] Submitted registration form via Enter keypress successfully.")
        except Exception as e:
            print(f"[REGISTER PAGE] Enter keypress failed: {e}. Falling back to click...")
            self.click_with_fallback(self.REGISTER_BUTTONS)

    def get_success_message(self) -> str:
        """Retrieves confirmation message text after registering."""
        return self.get_text_with_fallback(self.CONFIRMATION_TEXTS)

    def get_first_validation_error(self) -> str:
        """Retrieves the first visible form validation error text."""
        return self.get_text_with_fallback(self.ERROR_TEXTS)

    def get_welcome_title(self) -> str:
        """Retrieves the welcome title text displayed after registration."""
        selectors = [
            "div#rightPanel h1.title",
            "#rightPanel h1.title",
            "h1.title",
            "//h1[@class='title']"
        ]
        return self.get_text_with_fallback(selectors)

