# TODODev Test Cases
```
Test Case ID: TC001
Feature: User Login
Scenario: Valid login credentials
Preconditions: User account exists (username: testuser, password: Test123!)

Steps:
  1. Navigate to login page
  2. Enter username: testuser
  3. Enter password: Test123!
  4. Click login button

Expected Result: User is redirected to dashboard
Actual Result: User is redirected to dashboard
Status: Pass
```
``` 
Test Case ID: TC002
Feature: User Login
Scenario: Invalid login credentials
Preconditions: User account doesn't exists (username: testuser1, password: Test123!)

Steps:
  1. Navigate to login page
  2. Enter username: testuser1
  3. Enter password: Test123!
  4. Click login button

Expected Result: User is redirected to login page with error message
Actual Result: User is redirected to login page with error message
Status: Pass
```
```
Test Case ID: TC003
Feature: User Login
Scenario: Invalid login credentials
Preconditions: User account exists (username: testuser, password: Test123)

Steps:
  1. Navigate to login page
  2. Enter username: testuser
  3. Enter password: Test123
  4. Click login button

Expected Result: User is redirected to login page with error message
Actual Result: User is redirected to login page with error message
Status: Pass
```
```
Test Case ID: TC004
Feature: Category Creation
Scenario: Max length of category name
Preconditions: User must be in the create a task view

Steps:
  1. Create a new task
  2. Click the + button next to category dropdown
  3. Enter category name with a minimum of 50 characters
  4. Click + Add Category button

Expected Result: Category name should be truncated to 50 characters
Actual Result: Category name is not truncated and max length is not enforced
Status: Fail
```