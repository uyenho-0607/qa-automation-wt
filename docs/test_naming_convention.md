# Test Case Naming Convention

## Feature Prefixes

| Feature    | Prefix  | Description                      |
|--------------|---------|--------------------------------|
| Login        | LGN     | Authentication and user access |
| Market       | MKT     | Market data and analysis       |
| Trade        | TRD     | Trading operations             |
| Asset        | AST     | Asset management               |
| Signals      | SGN     | Trading signals                |
| News         | NWS     | News and announcements         |
| Calendar     | CLD     | Economic calendar              |
| Copy Trade   | CPT     | Copy trading functionality     |
| Education    | EDU     | Educational content            |
| Setting      | SET     | Setting content                |
| Notification | NTF     | Notification content           |


## Test Case Naming Format

```
test_<PREFIX>_TC<ID>_<TYPE>_<DESCRIPTION>
```

Where:

- `<PREFIX>`: Feature prefix from the table above (e.g., LGN, TRD, AST)
- `<ID>`: Sequential test ID (e.g., 01, 02, 03)
- `<TYPE>`: Test type (positive/negative)
- `<DESCRIPTION>`: Brief description of what the test verifies

### Examples:

- `test_LGN_TC01_positive_valid_credentials.py` - Tests successful login with valid credentials
- `test_LGN_TC02_negative_invalid_password.py` - Tests login failure with invalid password
- `test_TRD_TC01_positive_place_market_order.py` - Tests successful market order placement
- `test_AST_TC01_positive_view_portfolio.py` - Tests successful portfolio view

## Test File Organization

- Test files should be organized in directories matching their feature prefix
- Each feature should have its own directory under `tests/web/`
- Common test fixtures should be placed in the feature's `conftest.py`

Example structure:

```
tests/
  web/
    login/
      conftest.py
      test_LGN_TC01_positive_valid_credentials.py
      test_LGN_TC02_negative_invalid_password.py
    trade/
      conftest.py
      test_TRD_TC01_positive_place_market_order.py
    assets/
      conftest.py
      test_AST_TC01_positive_view_portfolio.py
``` 