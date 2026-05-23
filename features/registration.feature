Feature: ParaBank Account Registration, Sign-In, and Security Validation

  As a prospective bank customer
  I want to register an account and manage my sign-in session
  So that my banking data is secure and accessible

  Background:
    Given the user opens the ParaBank application

  @TC_PB_01 @positive @registration @login
  Scenario: Successful User Registration, Sign-In, and Balance Retrieval
    When the user navigates to the registration page
    And the user registers a new account with dynamic valid credentials
    Then the registration confirmation message should contain "Your account was created successfully. You are now logged in."
    When the user logs out of the application
    And the user logs in with the newly registered credentials
    Then the user should see their accounts overview dashboard
    And the user logs the account balance displayed on the page

  @TC_PB_02 @negative @registration
  Scenario: Failed Registration - Password Mismatch validation
    When the user navigates to the registration page
    And the user attempts registration with mismatched passwords
    Then registration fails showing error "Passwords did not match."

  @TC_PB_03 @negative @registration
  Scenario: Failed Registration - Missing Required Fields validation
    When the user navigates to the registration page
    And the user attempts registration with missing first name and username fields
    Then registration fails showing field warning "First name is required." or "Username is required."

  @TC_PB_04 @negative @login
  Scenario: Failed Sign-In - Invalid username and password credentials
    When the user attempts login with invalid credentials "nonexistent_test_user" and "WrongPassword99!"
    Then login fails showing error "The username and password could not be verified."

