# Test Case Writing Rules

## File Naming Convention

Test case files should follow this naming pattern:
```
test_[MODULE]_TC[XX]_[positive/negative]_[brief_description].py
```

Example:
- `test_LGN_TC01_positive_valid_credentials.py`
- `test_LGN_TC02_negative_invalid_credentials.py`

## Test Case Structure

### 1. Test Function
- Use `test` as the function name
- Include required fixtures in parameters: `pages`, `server`, `account`
```python
def test(pages, server, account):
```

### 2. Test Steps
- Each step should be logged using `logger.info()`
- Steps should be clear and descriptive
- Include verification steps

Example:

```python
def test(pages, server, account):
    # Get test data
    credentials = Config.get_credentials(server, account)

    # Step 1: Action
    logger.info("Step 1: Login with valid userid and password")
    pages.login_page.login(credentials.username, credentials.password, AccountType.DEMO, Language.ENGLISH)

    # Step 2: Verification
    logger.info("Verify trade page URL is correct")
    pages.home_page.verify_page_url(URLPaths.TRADE)

    # Step 3: Additional verification
    logger.info("Verify account selector is displayed")
    pages.home_page.verify_account_tabs_is_displayed()
```

## Best Practices

1. **Test Data Management**
   - Use `Config.get_credentials()` for credentials
   - Use enums for constants (AccountType, Language, URLPaths)
   - Keep test data separate from test logic
   - Use data providers for multiple test scenarios
   - Avoid hardcoding test data in test files

2. **Logging**
   - Log each step clearly
   - Include expected and actual results in logs
   - Use appropriate log levels (info, error, debug)
   - Add context to log messages
   - Log important state changes

3. **Assertions**
   - Use page object verification methods
   - Include clear assertion messages
   - Use soft assertions when appropriate
   - Verify one thing per assertion
   - Include both positive and negative assertions

4. **Test Independence**
   - Each test should be independent
   - Don't rely on the state from other tests
   - Clean up after test execution
   - Use appropriate setup and teardown
   - Handle test data cleanup

5. **Error Handling**
   - Include negative test cases
   - Verify error messages and states
   - Handle expected exceptions
   - Test edge cases and boundary conditions
   - Verify error recovery scenarios

6. **Code Quality**
   - Follow PEP 8 style guide
   - Use meaningful variable names
   - Keep test methods focused and small
   - Use appropriate comments
   - Avoid code duplication

7. **Test Organization**
   - Group related tests together
   - Use descriptive test names
   - Follow consistent naming patterns
   - Use appropriate test markers
   - Organize tests by feature/functionality

8. **Performance Considerations**
   - Minimize unnecessary waits
   - Use appropriate wait strategies
   - Avoid redundant verifications
   - Optimize test data setup
   - Clean up resources properly

9. **Maintainability**
   - Keep tests simple and readable
   - Use helper methods for common operations
   - Document complex test scenarios
   - Update tests when application changes
   - Regular test maintenance

10. **Security**
    - Don't hardcode sensitive data
    - Use secure credential management
    - Handle sensitive data properly
    - Follow security best practices
    - Clean up sensitive data after tests

## Example Test Cases

### Positive Test Case

```python
def test(pages, server, account):
    credentials = Config.get_credentials(server, account)

    logger.info("Step 1: Login with valid userid and password")
    pages.login_page.login(credentials.username, credentials.password, AccountType.DEMO, Language.ENGLISH)

    logger.info("Verify trade page URL is correct")
    pages.home_page.verify_page_url(URLPaths.TRADE)

    logger.info("Verify account selector is displayed")
    pages.home_page.verify_account_tabs_is_displayed()
```

### Negative Test Case
```python
def test(pages, server, account):
    logger.info("Step 1: Login with invalid credentials")
    pages.login_page.login("invalid_user", "invalid_pass", AccountType.DEMO, Language.ENGLISH)

    logger.info("Verify login failed")
    pages.login_page.verify_login_failed()
```

## Code Quality Examples

### Good Test Case

```python
def test(pages, server, account):
    # Arrange
    credentials = Config.get_credentials(server, account)
    expected_url = URLPaths.TRADE

    # Act
    logger.info("Step 1: Login with valid credentials")
    pages.login_page.login(
        username=credentials.username,
        password=credentials.password,
        account_type=AccountType.DEMO,
        language=Language.ENGLISH
    )

    # Assert
    logger.info("Verify successful login")
    pages.home_page.verify_page_url(expected_url)
    pages.home_page.verify_account_tabs_is_displayed()
```

### Bad Test Case (Avoid)
```python
def test(pages, server, account):
    # Bad: Hardcoded credentials
    pages.login_page.login("user123", "pass123", "demo", "en")
    
    # Bad: No logging
    pages.home_page.verify_page_url("/trade")
    
    # Bad: Multiple assertions in one line
    assert pages.home_page.is_account_tab_displayed() and pages.home_page.is_trade_tab_displayed()
```

## Test Case Checklist

Before submitting a test case, ensure:
- [ ] Test name follows naming convention
- [ ] All steps are properly logged
- [ ] Test data is properly managed
- [ ] Assertions are clear and specific
- [ ] Error handling is implemented
- [ ] Code follows style guide
- [ ] Test is independent
- [ ] No hardcoded values
- [ ] Proper cleanup is implemented
- [ ] Documentation is complete 