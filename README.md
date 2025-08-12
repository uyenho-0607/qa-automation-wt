# Chart Data API Testing Framework

A focused test automation framework for validating MetaTrader chart data through API testing. This framework compares chart data from MetaTrader CSV exports with API responses to ensure data accuracy across different timeframes and symbols.

## 🚀 Features

- **Chart Data API Testing** with comprehensive validation
- **MetaTrader Integration** (MT4 and MT5 support)
- **Multi-timeframe Testing** (1min, 5min, 15min, 30min, 1h, 4h, 1d, 1w, 1M)
- **Allure Reporting** with detailed comparison summaries
- **Environment-specific configurations** (SIT, UAT, Release-SIT)
- **Multi-client support** (Lirunex, TransactCloud)
- **Data tolerance validation** with configurable thresholds
- **Automated report generation and deployment**

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)
- Git
- Allure Command Line Tool (for report generation)
- MetaTrader 4/5 with CSV export capability

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

## 📁 Framework Structure

```
qa-automation-wt/
├── config/                 # Environment configuration files
│   ├── sit.yaml            # SIT environment settings
│   ├── uat.yaml            # UAT environment settings
│   ├── prod.yaml           # Production environment settings
│   └── release_sit.yaml    # Release SIT environment settings
├── src/                    # Source code
│   ├── apis/              # API testing modules
│   │   ├── api_base.py    # Base API client
│   │   ├── api_client.py  # Main API client
│   │   ├── auth_api.py    # Authentication API
│   │   └── chart_api.py   # Chart data API
│   ├── core/              # Core framework functionality
│   │   ├── config_manager.py # Configuration management
│   │   └── decorators.py  # API request decorators
│   ├── data/              # Test data and constants
│   │   ├── enums.py       # Enumerations (consolidated)
│   │   ├── consts.py      # Constants and paths
│   │   └── project_info.py # Runtime configuration
│   └── utils/             # Utility functions
│       ├── metatrader_utils.py # MetaTrader data processing
│       ├── assert_utils.py     # Assertion utilities
│       ├── allure_utils.py     # Allure reporting
│       ├── logging_utils.py    # Logging utilities
│       ├── format_utils.py     # Request formatting
│       └── encrypt_utils.py    # Password encryption
├── tests/                 # Test cases
│   └── api/
│       └── metatrader/
│           └── test_chart_data.py # Chart data validation tests
├── chart_data.sh         # Test execution and deployment script
├── conftest.py           # Pytest configuration
├── pytest.ini           # Pytest settings
└── requirements.txt      # Project dependencies
```

## 🧪 Running Tests

### Quick Start with Script

The easiest way to run tests and generate reports:

```bash
./chart_data.sh
```

This script will:
1. Run all chart data tests
2. Generate Allure report
3. Deploy report to Netlify (if configured)

### Manual Test Execution

Run chart data tests with Allure reporting:
```bash
pytest tests/api/metatrader --alluredir=allure-results
```

Generate and view the Allure report:
```bash
allure serve allure-results
allure serve -h  192.168.0.100 -p 8080 a
```

### Test Execution Options

```bash
# Environment selection
--env=sit|uat|release_sit

# Client selection  
--client=lirunex|transactCloud

# Server selection
--server=mt4|mt5

# Account type
--account=demo|live

# Custom credentials
--user="username" --password="password"
```

### Test Execution Examples

```bash
# Run tests for Lirunex MT4 demo account on SIT
pytest tests/api/ --env=sit --client=lirunex --server=mt4 --account=demo --alluredir=allure-results

# Run tests for TransactCloud MT5 live account on UAT
pytest tests/api/ --env=uat --client=transactCloud --server=mt5 --account=live --alluredir=allure-results

# Run tests with custom credentials
pytest tests/api/ --user="12345678" --password="mypassword" --alluredir=allure-results
```

## 📊 Chart Data Testing

### What It Tests

The framework validates:

1. **Dataset Amount**: Ensures API returns the same number of data points as MetaTrader
2. **Data Accuracy**: Compares OHLC (Open, High, Low, Close) values with configurable tolerance
3. **Missing Data Points**: Identifies data present in MetaTrader but missing in API
4. **Redundant Data Points**: Identifies extra data in API not present in MetaTrader  
5. **Timestamp Intervals**: Validates that data points follow correct timeframe intervals

### Supported Timeframes

- 1 minute (`1min`)
- 5 minutes (`5min`) 
- 15 minutes (`15min`)
- 30 minutes (`30min`)
- 1 hour (`1h`)
- 4 hours (`4h`)
- 1 day (`1d`)
- 1 week (`1w`)
- 1 month (`1M`)

### MetaTrader CSV Setup

The framework expects CSV files exported from MetaTrader to be available at:

- **MT5**: `~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Files/`
- **MT4**: `~/Library/Application Support/net.metaquotes.wine.metatrader4/drive_c/Program Files (x86)/MetaTrader 4/MQL4/Files/`

CSV files should be named: `{SYMBOL}_{TIMEFRAME}.csv`

Example: `BTCUSD.std_M1.csv`, `BAKE.USD_H1.csv`

## 📈 Allure Reports

The framework generates comprehensive Allure reports with:

- **Test execution summary** with pass/fail status
- **Detailed comparison tables** for each symbol-timeframe combination
- **Error details** with timestamps and data differences
- **Tolerance information** for numerical comparisons
- **Environment information** and test configuration

## 🔧 Configuration

### Environment Files

Configuration files in `config/` directory contain:

- **API URLs** for different environments
- **Encrypted passwords** for security
- **User credentials** for different account types
- **Client-specific settings**

### Data Tolerance

Default tolerance for OHLC comparisons is 0.1% (configurable in `src/data/consts.py`)

## 🛠️ Development

### Key Components

1. **APIs** (`src/apis/`): HTTP client and authentication
2. **Core** (`src/core/`): Configuration and request handling  
3. **Utils** (`src/utils/`): Data processing and validation utilities
4. **Tests** (`src/tests/`): Chart data validation test cases

### Adding New Symbols

1. Add symbol to `SYMBOL_LIST` in `test_chart_data.py`
2. Ensure CSV files are available in MetaTrader export directory
3. Update configuration files if needed

## 🚀 Deployment

The `chart_data.sh` script automatically deploys reports to Netlify. Configure your Netlify site by:

1. Install Netlify CLI: `npm install -g netlify-cli`
2. Login: `netlify login`  
3. Link site: `netlify link`
4. Update `DEPLOY_URL` in `chart_data.sh`
