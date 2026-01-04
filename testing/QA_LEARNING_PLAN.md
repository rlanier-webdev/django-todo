# QA Learning Plan: Django-Todo Project

## Overview
This is your hands-on QA learning journey using the django-todo project. You'll progress from manual testing to automated testing, learning core QA concepts and tools along the way.

---

## Phase 1: Understanding the Application (Week 1)

### Goals
- Understand what the application does
- Identify all features and user flows
- Set up your testing environment

### Tasks
- [X] Set up the project locally and run it
- [X] Create a user account and explore all features
- [X] Map out all user flows (signup → login → create task → edit → delete, etc.)
- [ ] Document the application structure

### Features to Explore
1. **Authentication**
   - User signup
   - User login
   - User logout
   - Timezone preferences

2. **Task Management**
   - Create task
   - View tasks (dashboard, calendar)
   - Edit task
   - Delete task
   - Toggle task completion
   - Filter/search tasks
   - Task priorities (low, medium, high, urgent)
   - Task statuses (pending, in progress, completed)

3. **Categories**
   - Create category
   - Assign category to task
   - View tasks by category

### Deliverables
- Feature map document
- User flow diagrams (can be simple text)

---

## Phase 2: Manual Testing & Test Case Design (Weeks 2-3)

### Goals
- Learn to write effective test cases
- Perform exploratory testing
- Understand different test types

### Tasks

#### 2.1 Exploratory Testing
- [X] Spend 30 minutes just "playing around" with the app
- [X] Try to break things (weird inputs, edge cases)
- [X] Document any bugs you find

#### 2.2 Write Test Cases
Create test cases for each feature. Use this format:

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
Actual Result: [Fill during testing]
Status: [Pass/Fail]
```

#### Test Areas to Cover
- [ ] User signup (valid/invalid data)
- [X] User login (valid/invalid credentials)
- [X] Task creation (all field combinations)
- [X] Task editing
- [X] Task deletion
- [X] Task filtering
- [X] Category management
- [ ] Timezone settings

#### 2.3 Test Design Techniques
Learn and apply these techniques:

**Equivalence Partitioning**
Example: Testing task title length
- Valid partition: 1-100 characters
- Invalid partition: 0 characters (empty)
- Invalid partition: 101+ characters

**Boundary Value Analysis**
Test the edges:
- Title: 0, 1, 99, 100, 101 characters
- Priority: low, medium, high, urgent (valid), "invalid_priority" (invalid)
- Dates: past dates, today, future dates, invalid formats

**Decision Tables**
Create a table for task creation with different field combinations

### Deliverables
- Test case document (at least 30 test cases)
- Bug report (if you find any)
- Test execution results

---

## Phase 3: Automated Testing - Unit Tests (Weeks 4-5)

### Goals
- Learn pytest and Django testing framework
- Write unit tests for models
- Achieve code coverage

### Setup
```bash
pip install pytest pytest-django pytest-cov
```

### Tasks

#### 3.1 Model Tests
Test the business logic in `core/todo/models.py`

Learn to test:
- [ ] Category model
  - Slug auto-generation
  - String representation
  - Unique name constraint
- [ ] Task model
  - Status/is_completed synchronization
  - Default values
  - Foreign key relationships
  - String representation
- [ ] TaskActivity model
  - Activity logging
  - Timestamp creation

**Example Test Structure:**
```python
# core/todo/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task, Category

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_task_creation(self):
        """Test that a task can be created with valid data."""
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            priority='high'
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.priority, 'high')
        self.assertFalse(task.is_completed)
```

#### 3.2 Form Tests
Test form validation in `core/todo/forms.py`

- [ ] Test valid form data
- [ ] Test invalid form data
- [ ] Test required fields
- [ ] Test field constraints

#### 3.3 Coverage Goals
- [ ] Achieve 80%+ coverage on models
- [ ] Learn to read coverage reports
```bash
pytest --cov=core/todo --cov-report=html
```

### Deliverables
- Comprehensive unit tests
- Coverage report
- Documentation of what you learned

---

## Phase 4: Automated Testing - Integration Tests (Weeks 6-7)

### Goals
- Learn to test views and user interactions
- Test authentication flows
- Test AJAX endpoints

### Tasks

#### 4.1 View Tests
Test all views in `core/todo/views.py` and `core/accounts/views.py`

**Authentication Tests**
- [ ] Test signup with valid data
- [ ] Test signup with invalid data (duplicate username, weak password)
- [ ] Test login with valid credentials
- [ ] Test login with invalid credentials
- [ ] Test logout
- [ ] Test protected views require login

**Task CRUD Tests**
- [ ] Test dashboard view loads correctly
- [ ] Test task creation via POST
- [ ] Test task editing via POST
- [ ] Test task deletion
- [ ] Test users can only access their own tasks

**AJAX Endpoint Tests**
- [ ] Test toggle_completed endpoint
- [ ] Test add_category endpoint
- [ ] Test set_timezone endpoint

**Example:**
```python
class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_dashboard_requires_login(self):
        """Test that dashboard redirects if not logged in."""
        self.client.logout()
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_create_task(self):
        """Test task creation through the view."""
        response = self.client.post('/task/create/', {
            'title': 'New Task',
            'description': 'Description',
            'priority': 'high',
            'status': 'pending'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Task.objects.filter(title='New Task').exists())
```

#### 4.2 Test Data Management
- [ ] Learn to use fixtures
- [ ] Learn to use factory patterns (factory_boy)
- [ ] Create reusable test data

### Deliverables
- Integration test suite
- Test data factories
- Updated coverage report

---

## Phase 5: Advanced Testing Topics (Weeks 8-9)

### Goals
- Learn about different testing types
- Implement CI/CD
- Explore performance and security testing

### Tasks

#### 5.1 Functional/End-to-End Testing with Selenium
- [ ] Install Selenium: `pip install selenium`
- [ ] Write a test that simulates complete user journey
  - Sign up → Login → Create task → Edit task → Mark complete → Logout

**Example E2E Test:**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

class E2ETests(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_complete_user_flow(self):
        # Navigate to signup
        self.driver.get('http://localhost:8000/signup/')
        # Fill form and submit
        # ... complete the flow
```

#### 5.2 API Testing
If you add Django REST framework later, test the APIs:
- [ ] Test GET endpoints
- [ ] Test POST/PUT/DELETE
- [ ] Test authentication/permissions
- [ ] Test error responses

#### 5.3 Performance Testing
- [ ] Use Django Debug Toolbar to identify slow queries
- [ ] Test with large datasets (1000+ tasks)
- [ ] Measure page load times

#### 5.4 Security Testing
- [ ] Test for SQL injection (try malicious inputs)
- [ ] Test for XSS (try script tags in task titles)
- [ ] Test authentication bypass attempts
- [ ] Test CSRF protection
- [ ] Verify users can't access other users' tasks

**Security Test Examples:**
```python
def test_user_cannot_edit_other_users_task(self):
    """Test that users can't edit tasks they don't own."""
    other_user = User.objects.create_user(
        username='otheruser',
        password='pass123'
    )
    other_task = Task.objects.create(
        user=other_user,
        title='Other User Task'
    )

    # Try to edit other user's task
    response = self.client.post(f'/task/{other_task.id}/edit/', {
        'title': 'Hacked!',
    })

    # Should get 404 (task not found for this user)
    self.assertEqual(response.status_code, 404)
```

#### 5.5 CI/CD Setup
- [ ] Set up GitHub Actions workflow
- [ ] Run tests on every commit
- [ ] Generate coverage reports
- [ ] Enforce minimum coverage threshold

**Example GitHub Actions Workflow:**
```yaml
name: Django Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=core --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### Deliverables
- E2E test suite
- Security test results
- CI/CD pipeline
- Performance test report

---

## Phase 6: Test Documentation & Best Practices (Week 10)

### Goals
- Learn to document testing processes
- Create testing guidelines
- Review and refactor tests

### Tasks
- [ ] Create a testing style guide
- [ ] Document how to run tests
- [ ] Create test data setup guide
- [ ] Refactor duplicate test code
- [ ] Add docstrings to all tests

### Deliverables
- TESTING.md document
- Refactored test suite
- Team testing guidelines

---

## Learning Resources

### Books
- "Test-Driven Development with Python" by Harry Percival
- "Django for Professionals" by William Vincent

### Documentation
- Django Testing Documentation: https://docs.djangoproject.com/en/stable/topics/testing/
- pytest Documentation: https://docs.pytest.org/
- pytest-django: https://pytest-django.readthedocs.io/

### Tools to Learn
1. **pytest** - Testing framework
2. **pytest-django** - Django integration
3. **pytest-cov** - Code coverage
4. **factory_boy** - Test data factories
5. **Selenium** - Browser automation
6. **Django Debug Toolbar** - Performance analysis
7. **Coverage.py** - Coverage measurement

### Key Concepts to Master
- Test-driven development (TDD)
- Test fixtures and factories
- Mocking and patching
- Test isolation
- Code coverage vs test quality
- Continuous integration
- Regression testing

---

## Weekly Milestones

**Week 1:** Application exploration complete, feature map created
**Week 2-3:** 50+ manual test cases written and executed
**Week 4-5:** Model and form tests complete, 80%+ coverage
**Week 6-7:** View tests complete, integration tests passing
**Week 8-9:** E2E tests, security tests, CI/CD pipeline running
**Week 10:** Documentation complete, test suite refactored

---

## Success Criteria

By the end of this plan, you should be able to:
- Write effective test cases manually
- Implement comprehensive automated test suites
- Achieve 85%+ code coverage
- Identify and report bugs systematically
- Understand security testing basics
- Set up CI/CD pipelines
- Make informed decisions about test strategies

---

## Next Steps

Start with Phase 1 - let me know when you're ready to begin!

I can help you with:
1. Setting up the testing environment
2. Writing your first tests
3. Understanding Django testing concepts
4. Debugging test failures
5. Improving test coverage

Let's build your QA skills step by step!
