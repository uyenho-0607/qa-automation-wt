# Web, Mobile, and API Test Automation Framework

A comprehensive test automation framework built with Python, supporting web application testing with Selenium, mobile application testing with Appium, and API testing with RESTful services.

## 🚀 Features

- **Web Application Testing** with Selenium WebDriver
- **Mobile Application Testing** with Appium (Android support)
- **API Testing** with RESTful services
- **Page Object Model (POM)** design pattern for UI testing
- **Allure Reporting** integration with custom enhancements
- **Cross-platform support** (Web, Android)
- **Modular and maintainable** test structure
- **Code quality tools** integration (flake8, isort, black)
- **Parallel test execution** with controlled concurrency
- **Environment-specific configurations** (SIT, UAT, PROD)
- **Multi-client support** (Lirunex, TransactCloud)
- **Multi-server support** (MT4, MT5)
- **Account type testing** (Demo, Live, CRM)
- **Video recording** for mobile tests
- **Screenshot capture** on test failures

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)
- Git
- Allure Command Line Tool (for report generation)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd qa-automation-wt
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Allure Command Line Tool:
```bash
# On macOS
brew install allure

# On Windows (using scoop)
scoop install allure

# On Linux
wget -qO- https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz | tar -xz -C /opt/
sudo ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure
```

## 📁 Framework Structure

```
qa-automation-wt/
├── config/                 # Configuration files
├── docs/                  # Documentation
│   ├── test_case_rules.md
│   ├── test_naming_convention.md
│   └── locator_conventions.md
├── src/                   # Source code
│   ├── apis/             # API testing modules
│   │   ├── api_base.py   # Base API client
│   │   ├── api_client.py # HTTP client wrapper
│   │   ├── auth_api.py   # Authentication API
│   │   ├── trade_api.py  # Trading API
│   │   ├── user_api.py   # User management API
│   │   ├── market_api.py # Market data API
│   │   ├── order_api.py  # Order management API
│   │   ├── statistics_api.py # Statistics API
│   │   └── chart_api.py  # Chart data API
│   │
│   ├── core/             # Core framework functionality
│   │   ├── actions/      # Action implementations
│   │   ├── driver/       # Driver management
│   │   ├── page_container/ # Page container management
│   │   ├── config_manager.py # Configuration management
│   │   └── decorators.py # Custom decorators
│   │
│   ├── data/             # Test data and constants
│   │   ├── enums.py      # Enumerations
│   │   ├── ui_messages.py # UI message constants
│   │   └── project_info.py # Project information
│   │
│   ├── page_object/      # Page Object classes
│   │   ├── web/         # Web page objects
│   │   │   ├── base_page.py
│   │   │   ├── pages/   # Individual page objects
│   │   │   └── components/ # Reusable components
│   │   └── android/     # Android page objects
│   │       ├── base_page.py
│   │       ├── pages/   # Individual page objects
│   │       └── components/ # Reusable components
│   │
│   └── utils/            # Utility functions
│       ├── allure_utils.py
│       ├── assert_utils.py
│       ├── common_utils.py
│       ├── logging_utils.py
│       └── video_utils.py
│
├── tests/                # Test cases
│   ├── web/             # Web test cases
│   ├── android/         # Android test cases
│   ├── api/             # API test cases
│   └── conftest.py      # Test configuration
├── conftest.py          # Main pytest configuration
├── pytest.ini          # Pytest settings
├── requirements.txt     # Project dependencies
├── pyproject.toml       # Project metadata
├── setup.cfg           # Project configuration
├── run_web_tests.sh    # Web test execution script
├── merge_report.sh     # Report merging utility
└── README.md           # Project documentation
```

### Key Components

1. **APIs** (`src/apis/`)
   - RESTful API testing modules
   - Base API client with common functionality
   - Specialized API modules for different services:
     - Authentication
     - Trading operations
     - User management
     - Market data
     - Order management
     - Statistics
     - Chart data

2. **Core** (`src/core/`)
   - Framework's core functionality
   - Actions: Web and mobile action implementations
   - Driver management: Web and mobile driver handling
   - Page container: Page object lifecycle management
   - Configuration management: Environment and test configuration
   - Decorators: Custom decorators for test enhancement

3. **Page Objects** (`src/page_object/`)
   - Page Object Model implementation for web and mobile applications
   - Organized by platform:
     - **Web** (`web/`):
       - `base_page.py`: Base class for all web page objects
       - `pages/`: Individual page objects (login, trade, markets, etc.)
       - `components/`: Reusable web components (settings, modals, notifications, etc.)
     - **Android** (`android/`):
       - `base_page.py`: Base class for all Android page objects
       - `pages/`: Individual mobile page objects
       - `components/`: Reusable mobile components
   - Each page object follows POM best practices:
     - Encapsulates page-specific locators
     - Implements page-specific actions
     - Inherits from respective base page class
     - Supports both web and mobile element interactions

4. **Utils** (`src/utils/`)
   - Allure reporting with custom enhancements
   - Assertion utilities
   - Common utilities
   - Logging utilities
   - Video recording utilities

5. **Tests** (`tests/`)
   - Web tests (`web/`)
   - Android tests (`android/`)
   - API tests (`api/`)

6. **Config** (`config/`)
   - Environment-specific configuration files

7. **Docs** (`docs/`)
   - Test case writing rules
   - Test naming conventions
   - Locator conventions

## 🧪 Running Tests

### Basic Test Execution

To run all tests with Allure reporting:
```bash
pytest --alluredir=./allure-results
```

To generate and view the Allure report:
```bash
allure serve ./allure-results
```

### Test Execution Options

The framework supports various test execution options through command-line arguments:

```bash
# Platform selection
--platform=web|android

# Environment selection
--env=sit|uat|prod

# Client selection
--client=lirunex|transactCloud

# Server selection
--server=mt4|mt5

# Account type
--account=demo|live|crm

# Browser selection (for web tests)
--browser=chrome|firefox|edge

# Headless mode (for web tests)
--headless

# Custom username
--user="username"

# Argo CD mode
--cd

# Test retry on failure
--reruns <number>

# Test markers
-m "smoke|regression|e2e|critical|sanity"
```

### Test Execution Examples

```bash
# Run web tests on SIT environment for Lirunex client with MT4 server using demo account
pytest --platform=web --env=sit --client=lirunex --server=mt4 --account=demo --alluredir=./allure-results

# Run mobile tests on UAT environment with live account
pytest --platform=android --env=uat --account=live --alluredir=./allure-results

# Run API tests
pytest tests/api --alluredir=./allure-results

# Run smoke tests on Chrome browser in headless mode
pytest --platform=web --browser=chrome --headless -m "smoke" --alluredir=./allure-results

# Run critical tests with custom username
pytest -m "critical" --user="testuser123" --alluredir=./allure-results

# Run specific test case
pytest tests/web/login/test_LGN_TC01_positive_valid_credentials.py --platform=web --env=sit --alluredir=./allure-results
```

### Parallel Test Execution

Use the provided shell script for controlled parallel execution:
```bash
# Run web tests in parallel with controlled concurrency
./run_web_tests.sh
```

The script controls the number of parallel test suites to manage memory usage effectively.

## 🏷️ Test Markers

The framework supports various test markers for categorization:

- `smoke`: Smoke test suite
- `sanity`: Sanity test suite
- `critical`: Critical priority tests
- `uat`: Tests for UAT environment only
- `mt4`: Tests for MT4 server only
- `mt5`: Tests for MT5 server only
- `not_demo`: Tests not for demo accounts
- `not_live`: Tests not for live accounts
- `not_crm`: Tests not for CRM accounts

## 🛠️ Development Tools

### Code Quality
- **flake8**: Linting and style checking
- **isort**: Import sorting
- **black**: Code formatting

### Testing Framework
- **pytest**: Test runner and framework
- **pytest-selenium**: Selenium integration
- **allure-pytest**: Test reporting
- **pytest-check**: Additional test features
- **pytest-rerunfailures**: Test retry functionality

### Web & Mobile Testing
- **selenium**: Web browser automation
- **Appium-Python-Client**: Mobile app automation
- **webdriver-manager**: WebDriver management

### Utilities
- **colorama**: Colored terminal output
- **pyyaml**: YAML configuration parsing
- **numpy**: Numerical computing
- **pandas**: Data manipulation
- **cryptography**: Encryption utilities
- **boto3**: AWS SDK for Python

## 📊 Reporting

### Allure Reports
The framework generates comprehensive Allure reports with:
- Test execution results
- Screenshots on failures
- Video recordings for mobile tests
- Environment information
- Custom test steps and logs
- Test categorization by server, account type, and platform

### Report Generation
```bash
# Generate report
allure generate ./allure-results --clean

# Serve report locally
allure serve ./allure-results

# Open existing report
allure open ./allure-report
```

## 🔧 Configuration

### Environment Configuration
The framework supports multiple environments:
- **SIT**: System Integration Testing
- **UAT**: User Acceptance Testing
- **PROD**: Production (use with caution)

### Client Configuration
- **Lirunex**: Default client configuration
- **TransactCloud**: Alternative client configuration

### Server Configuration
- **MT4**: MetaTrader 4 server
- **MT5**: MetaTrader 5 server

### Account Types
- **Demo**: Demo trading accounts
- **Live**: Live trading accounts
- **CRM**: Customer Relationship Management accounts

## 📚 Documentation

Additional documentation is available in the `docs/` directory:
- `test_case_rules.md`: Guidelines for writing test cases
- `test_naming_convention.md`: Test naming conventions
- `locator_conventions.md`: Locator strategy guidelines

## 🤝 Contributing

1. Follow the established coding standards
2. Use the provided code quality tools
3. Write comprehensive test cases
4. Update documentation as needed
5. Follow the test naming conventions

## 📝 License

This project is proprietary and confidential.
