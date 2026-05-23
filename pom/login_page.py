from pom.base_page import BasePage
from config.global_config import Config

class LoginPage(BasePage):
    """
    Page Object class for the login panel elements and user actions.
    """
    # Multi-locator fallbacks for elements
    USERNAME_INPUTS = [
        "input[name='username']",
        "form[name='login'] input[name='username']",
        "//input[@name='username']"
    ]
    PASSWORD_INPUTS = [
        "input[name='password']",
        "form[name='login'] input[name='password']",
        "//input[@name='password']"
    ]
    LOGIN_BUTTONS = [
        "input[value='Log In']",
        "form[name='login'] input[type='submit']",
        "//input[@value='Log In']"
    ]
    REGISTER_LINKS = [
        "a:has-text('Register')",
        "a[href*='register.htm']",
        "//a[text()='Register']"
    ]
    LOGOUT_LINKS = [
        "a:has-text('Log Out')",
        "a[href*='logout.htm']",
        "//a[text()='Log Out']"
    ]
    ERROR_MESSAGES = [
        "div#rightPanel p.error",
        "div#rightPanel p.error:visible",
        "#rightPanel p.error",
        "//div[@id='rightPanel']//p[@class='error']"
    ]

    def navigate_to_home(self):
        """Navigates to the home page URL matching active configuration."""
        self.navigate(Config.get_base_url())

    def click_register(self):
        """Navigates to the registration form by clicking the Register link."""
        print("[LOGIN PAGE] Clicking Register Link...")
        self.click_with_fallback(self.REGISTER_LINKS)

    def login(self, username, password):
        """Logs in using username and password credentials."""
        print(f"[LOGIN PAGE] Performing login for user: {username}")
        self.fill_with_fallback(self.USERNAME_INPUTS, username)
        self.fill_with_fallback(self.PASSWORD_INPUTS, password)
        self.click_with_fallback(self.LOGIN_BUTTONS)

    def logout_if_logged_in(self):
        """Safely logs out of the portal if active session is visible."""
        print("[LOGIN PAGE] Checking active session for logout...")
        if self.is_visible_with_fallback(self.LOGOUT_LINKS, timeout=3000):
            print("[LOGIN PAGE] Active session found. Logging out...")
            self.click_with_fallback(self.LOGOUT_LINKS)
        else:
            print("[LOGIN PAGE] No active session found.")

    def get_error_message(self) -> str:
        """
        Retrieves the login error message text.
        Waits for the error element to be present in the DOM (attached),
        then reads its text content directly - handles hidden error elements.
        """
        selectors = [
            "div#rightPanel p.error",
            "#rightPanel p.error",
            "p.error",
            "//p[@class='error']"
        ]
        last_error = None
        for selector in selectors:
            try:
                is_xpath = selector.startswith("//")
                if is_xpath:
                    locator = self.page.locator(f"xpath={selector}").first
                else:
                    locator = self.page.locator(selector).first
                # Wait for element to be in the DOM (attached), not necessarily visible
                locator.wait_for(state="attached", timeout=10000)
                # Read text directly via JavaScript to bypass visibility restriction
                text = locator.evaluate("el => el.innerText").strip()
                if text:
                    print(f"[LOGIN PAGE] Error message retrieved: '{text}'")
                    return text
            except Exception as e:
                print(f"[LOGIN PAGE] Selector failed: '{selector}' | {e}")
                last_error = e
        raise Exception(f"Could not retrieve error message using any selector. Last error: {last_error}")
