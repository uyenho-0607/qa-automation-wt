# Web and Mobile Test Automation Framework

A robust test automation framework built with Python, supporting both web and mobile application testing using Selenium and Appium.

## 🚀 Features

- Web application testing with Selenium
- Mobile application testing with Appium
- Page Object Model (POM) design pattern
- Allure reporting integration
- Cross-platform support
- Modular and maintainable test structure
- Code quality tools integration (flake8, isort, black)

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)
- Git

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd qa-automation-wt-demo
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

## 📁 Framework Structure

```
uyn-auto-wt/
├── config/                 # Configuration files
├── docs/                  # Documentation
│   ├── test_case_rules.md
│   └── page_object_rules.md
├── src/                   # Source code
│   ├── core/            # Core framework functionality
│   │   ├── actions/     # Action implementations
│   │   ├── driver/      # Driver management
│   │   └── config_manager.py
│   │
│   ├── data/            # Test data and constants
│   │   ├── enums.py
│   │   └── ui_messages.py
│   │
│   ├── page_object/     # Page Object classes
│   │   ├── web/        # Web page objects
│   │   └── mobile/     # Mobile page objects
│   │
│   └── utils/           # Utility functions
│       ├── allure_utils.py
│       ├── assert_utils.py
│       ├── common_utils.py
│       ├── logging_utils.py
│       └── video_utils.py
│
├── tests/               # Test cases
│   ├── web/            # Web test cases
│   └── mobile/         # Mobile test cases
├── conftest.py         # Pytest configurations
├── pytest.ini          # Pytest settings
├── requirements.txt    # Project dependencies
├── pyproject.toml      # Project metadata and build system
├── setup.cfg          # Project configuration
└── README.md          # Project documentation
```

### Key Components

1. **Core** (`src/core/`)
   - Framework's core functionality
   - Actions:
     - Web actions
     - Mobile actions
   - Driver management:
     - Web driver
     - Mobile driver
   - Configuration management

2. **Page Objects** (`src/page_object/`)
   - Page Object Model implementation for both web and mobile applications
   - Organized by platform:
     - Web (`web/`):
       - `base_page.py`: Base class for all web page objects
       - `pages/`: Individual page objects (e.g., login, trade, markets, ...)
       - `components/`: Reusable web components can be used in multiple pages (e.g., settings, modals, notifiations, ... )
     - Android (`android/`) (using the same structure as Web):
       - `base_page.py`: Base class for all Android page objects
       - `pages/`: Individual mobile page objects
       - `components/`: Reusable mobile components
   - Each page object follows POM best practices:
     - Encapsulates page-specific locators
     - Implements page-specific actions
     - Inherits from respective base page class
     - Supports both web and mobile element interactions

3. **Utils** (`src/utils/`)
   - Allure reporting
   - Assertions
   - Common utilities
   - Logging
   - Video recording

4. **Tests** (`tests/`)
   - Web tests
   - Mobile tests

5. **Config** (`config/`)
   - Environment configurations files

6. **Docs** (`docs/`)
   - Rules to note for using the framework

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
--platform=web|mobile

# Environment selection
--env=sit|uat|prod

# Client selection
--client=lirunex|other

# Server selection
--server=mt4|mt5

# Account type
--account=demo,live

# Browser selection (for web tests)
--browser=chrome|firefox|edge

# Headless mode (for web tests)
--headless

# Test retry on failure
--reruns <number>

# Test markers
-m "smoke|regression|e2e"
```

### Test Execution Examples

```bash
# Run web tests on SIT environment for Lirunex client with MT4 server using demo and live account
pytest --platform=web --env=sit --client=lirunex --server=mt4 --account=demo,live --alluredir=./allure-results

# Run mobile tests on UAT environment with live account and retry failed tests
pytest --platform=mobile --env=uat --account=live --reruns 3 --alluredir=./allure-results

# Run smoke tests on Chrome browser in headless mode
pytest --platform=web --browser=chrome --headless -m "smoke" --alluredir=./allure-results

# Run all login tests
pytest tests/web/login --platform=web --env=sit --alluredir=./allure-results

# Run specific test case
pytest .\tests\web\login\test_LGN_TC01_positive_valid_credentials.py --platform=web --env=sit --alluredir=./allure-results
```

## 🛠️ Development Tools

- **Code Quality**:
  - flake8: Linting
  - isort: Import sorting
  - black: Code formatting

- **Testing**:
  - pytest: Test runner
  - pytest-selenium: Selenium integration
  - allure-pytest: Test reporting
  - pytest-check: Additional test features
