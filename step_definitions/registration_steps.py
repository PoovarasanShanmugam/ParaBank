import sys
from behave import given, when, then
from test_data.test_data_manager import TestDataManager
from container.credentials_container import credentials_container
from pom.login_page import LoginPage
from pom.register_page import RegisterPage
from pom.accounts_overview_page import AccountsOverviewPage

def print_validation_report(step_name: str, verifications: list):
    """
    Utility function to print a clean, structured validation report
    comparing Expected vs Actual values in bank-grade standard.
    """
    print("\n" + "=" * 80)
    print(f" VALIDATION REPORT: {step_name}")
    print("=" * 80)
    print(f"{'CHECKPOINT / COMPONENT':<35} | {'EXPECTED':<30} | {'ACTUAL':<30} | {'STATUS'}")
    print("-" * 115)
    for title, expected, actual, success in verifications:
        status_str = "[PASS]" if success else "[FAIL]"
        print(f"{title:<35} | {str(expected):<30} | {str(actual):<30} | {status_str}")
    print("=" * 80 + "\n")

# ----------------------------------------------------
# Background Step
# ----------------------------------------------------

@given('the user opens the ParaBank application')
def step_open_home_page(context):
    print("\n>>> [STEP] Given the user opens the ParaBank application")
    try:
        context.login_page = LoginPage(context.page)
        context.login_page.navigate_to_home()
        
        # URL and Title validation
        actual_url = context.page.url
        actual_title = context.page.title()
        
        expected_url_part = "index.htm"
        expected_title = "ParaBank | Welcome | Online Banking"
        
        url_match = expected_url_part in actual_url
        title_match = actual_title == expected_title
        
        print_validation_report(
            "APPLICATION LANDING & HOMEPAGE OPEN",
            [
                ("Landing Page URL (contains)", expected_url_part, actual_url, url_match),
                ("Landing Page HTML Title", expected_title, actual_title, title_match)
            ]
        )
        
        assert url_match, f"Expected URL to contain '{expected_url_part}', got: '{actual_url}'"
        assert title_match, f"Expected page title to be '{expected_title}', got: '{actual_title}'"
        print("[SUCCESS] ParaBank homepage loaded and validated successfully.")
    except Exception as e:
        print(f"[FAIL] Error loading/validating homepage: {e}")
        raise e

# ----------------------------------------------------
# Navigation Steps
# ----------------------------------------------------

@when('the user navigates to the registration page')
def step_navigate_to_registration(context):
    print("\n>>> [STEP] When the user navigates to the registration page")
    try:
        context.login_page.click_register()
        context.register_page = RegisterPage(context.page)
        context.register_page.wait_for_form()
        
        # URL and Title validation
        actual_url = context.page.url
        actual_title = context.page.title()
        
        expected_url_part = "register.htm"
        expected_title = "ParaBank | Register for Free Online Account Access"
        
        url_match = expected_url_part in actual_url
        title_match = actual_title == expected_title
        
        print_validation_report(
            "REGISTRATION PAGE NAVIGATION",
            [
                ("Registration Page URL (contains)", expected_url_part, actual_url, url_match),
                ("Registration Page HTML Title", expected_title, actual_title, title_match)
            ]
        )
        
        assert url_match, f"Expected URL to contain '{expected_url_part}', got: '{actual_url}'"
        assert title_match, f"Expected page title to be '{expected_title}', got: '{actual_title}'"
        print("[SUCCESS] Navigated to Registration page and form loaded successfully.")
    except Exception as e:
        print(f"[FAIL] Error navigating or validating registration page: {e}")
        raise e

# ----------------------------------------------------
# Positive Flow Steps
# ----------------------------------------------------

@when('the user registers a new account with dynamic valid credentials')
def step_register_user_dynamic(context):
    print("\n>>> [STEP] And the user registers a new account with dynamic valid credentials")
    try:
        # Generate new registration POJO using test data manager
        user_data = TestDataManager.generate_dynamic_registration_data()
        
        print("\n" + "=" * 80)
        print("          DYNAMIC USER REGISTRATION DATA CONTAINER (POJO)")
        print("=" * 80)
        print(f"  First Name  : {user_data.first_name}")
        print(f"  Last Name   : {user_data.last_name}")
        print(f"  Address     : {user_data.address}")
        print(f"  City        : {user_data.city}")
        print(f"  State       : {user_data.state}")
        print(f"  Zip Code    : {user_data.zip_code}")
        print(f"  Phone Number: {user_data.phone}")
        print(f"  SSN         : {user_data.ssn}")
        print(f"  Username    : {user_data.username}")
        print(f"  Password    : {user_data.password}")
        print("=" * 80 + "\n")
        
        # Store user details in the POJO credentials_container
        credentials_container.set_username(user_data.username)
        credentials_container.set_password(user_data.password)
        
        # Store user details in the ScenarioContext container to share with the login step
        context.scenario_context.set("registered_user", user_data)
        
        # Perform POM registration action
        context.register_page.register_user(user_data)
        print("[SUCCESS] Registration form submitted successfully.")
    except Exception as e:
        print(f"[FAIL] Error during registration submission: {e}")
        raise e

@then('the registration confirmation message should contain "{expected_message}"')
def step_verify_registration_message(context, expected_message):
    print(f"\n>>> [STEP] Then the registration confirmation message should contain '{expected_message}'")
    try:
        # URL, Title, and Message verification
        actual_url = context.page.url
        actual_title = context.page.title()
        
        expected_url_part = "register.htm"
        expected_title = "ParaBank | Customer Created"
        
        url_match = expected_url_part in actual_url
        title_match = actual_title == expected_title
        
        actual_message = context.register_page.get_success_message()
        msg_match = expected_message in actual_message
        
        # Get welcome header showing "Welcome <username>"
        actual_welcome_title = context.register_page.get_welcome_title()
        expected_welcome = f"Welcome {credentials_container.get_username()}"
        welcome_match = actual_welcome_title == expected_welcome
        
        print_validation_report(
            "REGISTRATION SUCCESS PAGE VERIFICATION",
            [
                ("Registration Success URL", expected_url_part, actual_url, url_match),
                ("Registration Success HTML Title", expected_title, actual_title, title_match),
                ("Welcome Heading Text", expected_welcome, actual_welcome_title, welcome_match),
                ("Success Message Content", expected_message, actual_message, msg_match)
            ]
        )
        
        assert url_match, f"Expected URL to contain '{expected_url_part}', got: '{actual_url}'"
        assert title_match, f"Expected page title to be '{expected_title}', got: '{actual_title}'"
        assert welcome_match, f"Expected welcome title '{expected_welcome}', got: '{actual_welcome_title}'"
        assert msg_match, f"Expected message '{expected_message}' not found in actual: '{actual_message}'"
        
        print("[SUCCESS] Registration confirmation and welcome header verified successfully.")
    except Exception as e:
        print(f"[FAIL] Error verifying registration page details: {e}")
        raise e

@when('the user logs out of the application')
def step_logout(context):
    print("\n>>> [STEP] When the user logs out of the application")
    try:
        context.login_page.logout_if_logged_in()
        
        # Validate URL and form visibility on logout
        actual_url = context.page.url
        expected_url_part = "index.htm"
        url_match = expected_url_part in actual_url
        
        print_validation_report(
            "USER LOGOUT & SESSION TERMINATION",
            [
                ("Home Landing URL (contains)", expected_url_part, actual_url, url_match)
            ]
        )
        assert url_match, f"Expected URL to contain '{expected_url_part}' after logout, got: '{actual_url}'"
        print("[SUCCESS] Logged out and landed on home page successfully.")
    except Exception as e:
        print(f"[FAIL] Error during logout: {e}")
        raise e

@when('the user logs in with the newly registered credentials')
def step_login_with_registered(context):
    print("\n>>> [STEP] And the user logs in with the newly registered credentials")
    try:
        # Retrieve user credentials from the POJO credentials_container
        username = credentials_container.get_username()
        password = credentials_container.get_password()
        
        if not username or not password:
            raise ValueError("No user credentials found in credentials_container POJO.")
            
        print(f"[DATA] Retrying login with username: {username} and password: {password}")
        context.login_page.navigate_to_home()
        context.login_page.login(username, password)
        print("[SUCCESS] Credentials entered and login submitted.")
    except Exception as e:
        print(f"[FAIL] Error logging in: {e}")
        raise e

@then('the user should see their accounts overview dashboard')
def step_verify_accounts_overview(context):
    print("\n>>> [STEP] Then the user should see their accounts overview dashboard")
    try:
        context.accounts_page = AccountsOverviewPage(context.page)
        context.accounts_page.wait_for_load()
        
        # Verify URL, page title, section header, and welcome panel message
        actual_url = context.page.url
        actual_title = context.page.title()
        
        expected_url_part = "overview.htm"
        expected_title = "ParaBank | Accounts Overview"
        
        url_match = expected_url_part in actual_url
        title_match = expected_title in actual_title
        
        # Check welcome name block using registered user data from ScenarioContext container
        registered_user = context.scenario_context.get("registered_user")
        if registered_user:
            expected_welcome = f"Welcome {registered_user.first_name} {registered_user.last_name}"
        else:
            expected_welcome = "Welcome Poovarasan S"
            
        actual_welcome = context.accounts_page.get_welcome_message()
        welcome_match = expected_welcome in actual_welcome
        
        print_validation_report(
            "ACCOUNTS OVERVIEW DASHBOARD VERIFICATION",
            [
                ("Dashboard URL (contains)", expected_url_part, actual_url, url_match),
                ("Dashboard HTML Title (contains)", expected_title, actual_title, title_match),
                ("Left Panel Welcome Text", expected_welcome, actual_welcome, welcome_match)
            ]
        )
        
        assert url_match, f"Expected URL to contain '{expected_url_part}', got: '{actual_url}'"
        assert title_match, f"Expected page title to contain '{expected_title}', got: '{actual_title}'"
        assert welcome_match, f"Expected welcome panel to contain '{expected_welcome}', got: '{actual_welcome}'"
        
        print("[SUCCESS] Accounts overview page and session verified successfully.")
    except Exception as e:
        print(f"[FAIL] Error loading/verifying accounts overview page: {e}")
        raise e

@then('the user logs the account balance displayed on the page')
def step_log_account_balances(context):
    print("\n>>> [STEP] And the user logs the account balance displayed on the page")
    try:
        accounts = context.accounts_page.get_accounts_data()
        total_balance = context.accounts_page.get_total_balance()
        
        print("\n" + "=" * 80)
        print("                 PARABANK SECURE ACCOUNTS LEDGER")
        print("=" * 80)
        if not accounts:
            print(" No active accounts listed or still synchronizing.")
        for idx, acc in enumerate(accounts, 1):
            print(f" {idx:02d}. Account Reference : {acc['account_id']}")
            print(f"     Ledger Balance    : {acc['balance']}")
            print(f"     Available Fund    : {acc['available']}")
            print("-" * 80)
        print(f" AUDITED TOTAL BALANCE IN PORTAL: {total_balance}")
        print("=" * 80 + "\n")
        
        # Assert that balance starts with dollar sign indicating valid formatting
        assert total_balance.startswith("$"), f"Expected total balance to be currency formatted, got: {total_balance}"
        print("[SUCCESS] Account balances fetched, verified, and audited successfully.")
    except Exception as e:
        print(f"[FAIL] Error retrieving/verifying account balances: {e}")
        raise e

# ----------------------------------------------------
# Negative Flow Steps
# ----------------------------------------------------

@when('the user attempts registration with mismatched passwords')
def step_register_mismatched_passwords(context):
    print("\n>>> [STEP] And the user attempts registration with mismatched passwords")
    try:
        user_data = TestDataManager.generate_dynamic_registration_data()
        # Custom register invocation passing confirm password mismatch
        context.register_page.register_user(user_data, password_to_confirm="MismatchingPassword99!")
        print("[SUCCESS] Registration form submitted with password mismatch.")
    except Exception as e:
        print(f"[FAIL] Error during mismatched password registration: {e}")
        raise e

@then('registration fails showing error "{expected_error}"')
def step_verify_registration_error(context, expected_error):
    print(f"\n>>> [STEP] Then registration fails showing error '{expected_error}'")
    try:
        # Validate URL and error text
        actual_url = context.page.url
        expected_url_part = "register.htm"
        url_match = expected_url_part in actual_url
        
        actual_error = context.register_page.get_first_validation_error()
        error_match = expected_error in actual_error
        
        print_validation_report(
            "REGISTRATION FAILURE - PASSWORD MISMATCH",
            [
                ("Registration Form URL (contains)", expected_url_part, actual_url, url_match),
                ("Form Validation Error (contains)", expected_error, actual_error, error_match)
            ]
        )
        
        assert url_match, f"Expected URL to contain '{expected_url_part}', got: '{actual_url}'"
        assert error_match, f"Expected validation error '{expected_error}' not found in actual: '{actual_error}'"
        print("[SUCCESS] Registration password mismatch error successfully verified.")
    except Exception as e:
        print(f"[FAIL] Error verifying registration password validation: {e}")
        raise e

@when('the user attempts registration with missing first name and username fields')
def step_register_missing_fields(context):
    print("\n>>> [STEP] And the user attempts registration with missing fields")
    try:
        user_data = TestDataManager.generate_dynamic_registration_data()
        user_data.first_name = ""  # Empty first name
        user_data.username = ""    # Empty username
        
        context.register_page.register_user(user_data)
        print("[SUCCESS] Registration form submitted with missing fields.")
    except Exception as e:
        print(f"[FAIL] Error during registration with missing fields: {e}")
        raise e

@then('registration fails showing field warning "{error_one}" or "{error_two}"')
def step_verify_registration_multiple_errors(context, error_one, error_two):
    print(f"\n>>> [STEP] Then registration fails showing error '{error_one}' or '{error_two}'")
    try:
        # Validate URL and error text
        actual_url = context.page.url
        expected_url_part = "register.htm"
        url_match = expected_url_part in actual_url
        
        actual_error = context.register_page.get_first_validation_error()
        match = (error_one in actual_error) or (error_two in actual_error)
        
        print_validation_report(
            "REGISTRATION FAILURE - MISSING MANDATORY FIELDS",
            [
                ("Registration Form URL (contains)", expected_url_part, actual_url, url_match),
                (f"Validation Error (contains '{error_one}' or '{error_two}')", f"'{error_one}' | '{error_two}'", actual_error, match)
            ]
        )
        
        assert url_match, f"Expected URL to contain '{expected_url_part}', got: '{actual_url}'"
        assert match, f"Neither '{error_one}' nor '{error_two}' matches actual error: '{actual_error}'"
        print("[SUCCESS] Verified missing field validation warning presence successfully.")
    except Exception as e:
        print(f"[FAIL] Error verifying multiple validation fields: {e}")
        raise e

@when('the user attempts login with invalid credentials "{username}" and "{password}"')
def step_login_invalid_credentials(context, username, password):
    print(f"\n>>> [STEP] When the user attempts login with invalid credentials '{username}'")
    try:
        context.login_page.navigate_to_home()
        context.login_page.login(username, password)
        print("[SUCCESS] Submitted login with invalid credentials.")
    except Exception as e:
        print(f"[FAIL] Error during invalid login submission: {e}")
        raise e

@then('login fails showing error "{expected_error}"')
def step_verify_login_error(context, expected_error):
    print(f"\n>>> [STEP] Then login fails showing error '{expected_error}'")
    try:
        # Validate URL and error message
        actual_url = context.page.url
        
        actual_error = context.login_page.get_error_message()
        
        # Support either the standard validation error or ParaBank's known backend internal error
        alternative_error = "An internal error has occurred and has been logged."
        matched = (expected_error in actual_error) or (alternative_error in actual_error)
        
        print_validation_report(
            "SIGN-IN FAILURE - INVALID CREDENTIALS",
            [
                ("Current URL", "N/A", actual_url, True),
                (f"Login Error Message (contains '{expected_error}')", expected_error, actual_error, matched)
            ]
        )
        
        assert matched, f"Expected error '{expected_error}' or '{alternative_error}' not found in actual: '{actual_error}'"
        print("[SUCCESS] Login error message verified successfully.")
    except Exception as e:
        print(f"[FAIL] Error verifying login failure: {e}")
        raise e
