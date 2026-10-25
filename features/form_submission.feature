Feature: Login and registration forms
  As a visitor to QA Practice Hub
  I want the login, password recovery, and registration forms to behave correctly
  So that I can verify common form interactions and validation

  Background:
    Given the Forms page is open

  Scenario: The Forms page shows the login and registration forms
    Then I should see the "Login Form" and "Registration Form" sections

  Scenario Outline: Login reports the result for submitted credentials
    When I fill the "login" form with
      | field    | value       |
      | username | <username>  |
      | password | <password>  |
    And I submit the "login" form
    Then the "login" form feedback should contain "<feedback>"

    Examples:
      | username | password    | feedback            |
      | tester   | password123 | Login successful!   |
      | wrong    | invalid     | Invalid credentials |

  Scenario: Login rejects an empty username
    When I fill the "login" form with
      | field    | value       |
      | username |             |
      | password | password123 |
    And I submit the "login" form
    Then the "username" field on the "login" form should be invalid

  Scenario: Login rejects an empty password
    When I fill the "login" form with
      | field    | value  |
      | username | tester |
      | password |        |
    And I submit the "login" form
    Then the "password" field on the "login" form should be invalid

  Scenario: The login password can be shown and hidden
    When I fill the "login" form with
      | field    | value       |
      | password | password123 |
    And I toggle visibility of the "password" field on the "login" form
    Then the "password" field on the "login" form should be "visible"
    When I toggle visibility of the "password" field on the "login" form
    Then the "password" field on the "login" form should be "hidden"

  Scenario: Password recovery reports a missing username
    When I open the "password recovery" form
    And I fill the "password recovery" form with
      | field    | value |
      | username |       |
    And I submit the "password recovery" form
    Then the "password recovery" form feedback should contain "Please enter your username."

  Scenario: Password recovery returns the practice account password
    When I open the "password recovery" form
    And I fill the "password recovery" form with
      | field    | value  |
      | username | tester |
    And I submit the "password recovery" form
    Then the "password recovery" form feedback should contain "Password: password123"

  Scenario: Registration requires all fields
    When I submit the "registration" form
    Then the "registration" form feedback should contain "Please fill in all required fields."

  Scenario: Registration rejects an invalid email address
    When I fill the "registration" form with
      | field      | value        |
      | first name | Taylor       |
      | last name  | Tester       |
      | email      | not-an-email |
      | country    | India        |
    Then the "email" field on the "registration" form should be invalid

  Scenario: Registration requires a country selection
    When I fill the "registration" form with
      | field      | value              |
      | first name | Taylor             |
      | last name  | Tester             |
      | email      | taylor@example.com |
      | country    |                    |
    Then the "country" field on the "registration" form should be invalid

  Scenario: Registration succeeds with valid details
    When I fill the "registration" form with
      | field      | value              |
      | first name | Taylor             |
      | last name  | Tester             |
      | email      | taylor@example.com |
      | country    | India              |
    And I submit the "registration" form
    Then the "registration" form feedback should contain "Registration successful for Taylor Tester!"

  Scenario: Clear resets the registration form
    When I fill the "registration" form with
      | field      | value        |
      | first name | Taylor       |
      | last name  | Tester       |
      | email      | not-an-email |
      | country    | India        |
    And I clear the "registration" form
    Then all fields on the "registration" form should be empty or unselected
