# ParaBank Test Case Specifications

This document outlines the test case specifications designed for the automated testing of the ParaBank Account Registration and Sign-In flows. Each test case is mapped directly to a Test Case ID and can be executed via features or the python unit test suite.

---

## Test Suite Matrix Summary

| Test Case ID | Module | Test Case Title | Test Type | Priority | Execution Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_PB_01** | Registration & Login | Successful User Registration, Sign-In, and Balance Retrieval | Positive | High | `PASSED` |
| **TC_PB_02** | Registration | Failed Registration - Password Mismatch validation | Negative | Medium | `PASSED` |
| **TC_PB_03** | Registration | Failed Registration - Missing Required Fields validation | Negative | High | `PASSED` |
| **TC_PB_04** | Login Panel | Failed Sign-In - Invalid username and password credentials | Negative | High | `PASSED` |

---

## Test Cases Detailed Specifications

### TC_PB_01: Successful User Registration, Sign-In, and Balance Retrieval

* **Module**: Registration & Login
* **Test Type**: Functional / Positive
* **Priority**: High
* **Execution Tag**: `@TC_PB_01` (BDD Scenarios) / `test_TC_PB_01` (Python Unit Test)

#### Objective
Verify that a new user can successfully complete the account registration process with dynamically generated valid inputs, log out, log back in using the newly created credentials, view their Accounts Overview dashboard, and retrieve their balance.

#### Preconditions
1. The ParaBank web application is accessible.
2. The user session is cleared (not logged in).
3. The username generated is unique to avoid database constraint violations.

#### Test Steps (BDD Gherkin Style)
```gherkin
Given the user opens the ParaBank application
When the user navigates to the registration page
And the user registers a new account with dynamic valid credentials
Then the registration confirmation message should contain "Your account was created successfully. You are now logged in."
When the user logs out of the application
And the user logs in with the newly registered credentials
Then the user should see their accounts overview dashboard
And the user logs the account balance displayed on the page
```

#### Dynamic Test Data (POJO Model)
* **First Name**: Random alphabet string (e.g., `John`)
* **Last Name**: Random alphabet string (e.g., `Doe`)
* **Address**: Dynamic address string
* **City**: Dynamic city string
* **State**: Dynamic state string
* **Zip Code**: Random 5-digit number
* **Phone**: Random 10-digit number
* **SSN**: Random 9-digit SSN format (`###-##-####`)
* **Username**: Programmatically unique string (e.g., `pb_171649234`)
* **Password**: Secure dynamic password

#### Expected Results
1. The registration confirmation banner displays: `"Your account was created successfully. You are now logged in."`
2. Logout succeeds, redirecting the user back to the homepage login sidebar.
3. Sign-in with the dynamic username and password succeeds and navigates to the Accounts Overview page.
4. The dashboard lists the user's primary checking account with a non-empty balance.
5. The account balance is successfully scraped, displayed, and printed to the console output/logs.

---

### TC_PB_02: Failed Registration - Password Mismatch validation

* **Module**: Registration
* **Test Type**: Functional / Negative
* **Priority**: Medium
* **Execution Tag**: `@TC_PB_02` (BDD Scenarios) / `test_TC_PB_02` (Python Unit Test)

#### Objective
Verify that the account registration form validation prevents users from registering when the "Password" and "Confirm Password" input values do not match.

#### Preconditions
1. The ParaBank registration page is accessible.

#### Test Steps (BDD Gherkin Style)
```gherkin
Given the user opens the ParaBank application
When the user navigates to the registration page
And the user attempts registration with mismatched passwords
Then registration fails showing error "Passwords did not match."
```

#### Test Data
* **Standard Fields**: Valid dynamic text
* **Password**: `SecurePass123!`
* **Confirm Password**: `MismatchedPass999`

#### Expected Results
1. The registration form submission is rejected.
2. A red validation error message stating `"Passwords did not match."` is displayed directly below or beside the "Confirm" password field.
3. No account is created in the database.

---

### TC_PB_03: Failed Registration - Missing Required Fields validation

* **Module**: Registration
* **Test Type**: Functional / Negative
* **Priority**: High
* **Execution Tag**: `@TC_PB_03` (BDD Scenarios) / `test_TC_PB_03` (Python Unit Test)

#### Objective
Verify that the account registration form validation blocks registration when mandatory fields (such as First Name or Username) are left completely blank.

#### Preconditions
1. The ParaBank registration page is accessible.

#### Test Steps (BDD Gherkin Style)
```gherkin
Given the user opens the ParaBank application
When the user navigates to the registration page
And the user attempts registration with missing first name and username fields
Then registration fails showing field warning "First name is required." or "Username is required."
```

#### Test Data
* **First Name**: *Left Blank*
* **Username**: *Left Blank*
* **Other Fields**: Populated with standard dynamic data

#### Expected Results
1. The form submission is rejected.
2. In-line validation text appears next to the missing fields indicating:
   * `"First name is required."`
   * `"Username is required."`
3. No account is created in the database.

---

### TC_PB_04: Failed Sign-In - Invalid username and password credentials

* **Module**: Login Panel
* **Test Type**: Functional / Negative
* **Priority**: High
* **Execution Tag**: `@TC_PB_04` (BDD Scenarios) / `test_TC_PB_04` (Python Unit Test)

#### Objective
Verify that the login mechanism blocks sign-in requests that provide credentials that do not exist or are incorrect, ensuring application security.

#### Preconditions
1. The ParaBank homepage is accessible and the user login sidebar is displayed.

#### Test Steps (BDD Gherkin Style)
```gherkin
Given the user opens the ParaBank application
When the user attempts login with invalid credentials "nonexistent_test_user" and "WrongPassword99!"
Then login fails showing error "The username and password could not be verified."
```

#### Test Data
* **Username**: `nonexistent_test_user` (Not registered in ParaBank)
* **Password**: `WrongPassword99!`

#### Expected Results
1. The user authentication fails.
2. The user remains unauthenticated.
3. An error message banner appears displaying: `"The username and password could not be verified."`
4. The user is not granted access to the Accounts Overview dashboard.

---

## Formats & Deliverables Map

The test cases are available and synchronized across the following three proper formats:
1. **Interactive BDD Feature Specification**: [features/registration.feature](file:///Users/myfolder/ParaBank/features/registration.feature) (Executable tag-filtered Gherkin Gherkins)
2. **Beautiful Excel Spreadsheet Matrix**: [test_cases.xlsx](file:///Users/myfolder/ParaBank/test_cases.xlsx) (Fully styled Excel sheets for managers, featuring dark navy headers, soft gray row strips, Segoe UI fonts, and auto-fit column sizes)
3. **Executable Python Unit Test Suite**: [tests/test_suite.py](file:///Users/myfolder/ParaBank/tests/test_suite.py) (Native Python `unittest` class for CLI or CI/CD pipelines)
