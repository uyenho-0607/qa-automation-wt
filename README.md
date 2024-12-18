# QA Automation Testing

## Setting up your project environment
- Ensure that you have Python (3.11 and above) installed on your machine
  - Please refer to https://www.dataquest.io/blog/installing-python-on-mac/ for more information on how to get Python up and running
- Ensure that `pip` or `pip3` is installed alongside Python as well, `pip` would be your main package manager for Python libraries used in running the test cases
- Ensure that you have either Visual Studio Code installed on your machine
  - The IDE (Integrated Development Enviroment) will facilitate your coding of your Python test cases
  - Download Visual Studio Code (v1.85 and above): https://code.visualstudio.com/download
- [For macOS] Ensure that you have `brew` installed on your machine
  **`brew` is a package manager for macOS plugins/libraries that we would have to use to setup your development environment**
  - Refer to https://brew.sh/ for more info on installation
    1. Open Terminal
    2. Run the following command:
      `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    3. Ensure that you follow the commands given after successful installation of `brew`
      ```
        eval "$(homebrew/bin/brew shellenv)"
        brew update --force --quiet
        chmod -R go-w "$(brew --prefix)/share/zsh"
      ```
- Ensure that you have Allure installed on your machine
  **Allure is an automation test report tool that we will be using to generate reports from the test case results**
  - Refer to https://allurereport.org/docs/gettingstarted-installation/ for more info on installation
  - macOS
    - Make sure Homebrew is installed.
    - In a terminal, run this command:
      ```
      brew install allure
      brew install ffmpeg
      ```
  - Windows
    - Make sure Scoop is installed.
    - Make sure Java version 8 or above installed, and its directory is specified in the `JAVA_HOME` environment variable.
    - In a terminal, run this command:
      ```
      scoop install allure
      ```
- Ensure that you have `pytest` installed on your machine
  - `pip` is required for installation of `pytest`
  ```
    pip install pytest
  ```
  - To verify if `pytest` is working
  ```
    # Running this command should print out: pytest 8.x.x
    pytest --version
  ```

## Project structure
- The structure of the folder/files in this project will be further elaborated below:

```
OPTION-B

├── src
│   ├── common
│   │   ├── desktop
│   │   │   ├── login
│   │   │   │   ├── utils.py
│   │   │   ├── Logout
│   │   │   │   ├── utils.py
│   │   ├── mobileweb
│   │   │   ├── login
│   │   │   │   ├── utils.py
│   │   │   ├── Logout
│   │   │   │   ├── utils.py
│   │   ├── main.py
│   ├── constants
│   │   ├── main.py
│   ├── custom_types
│   │   ├── __init__.py
│   ├── enums
│   │   ├── main.py
│   ├── test
│   │   ├── ts_da
│   │   │   ├── test_01.py
│   │   │   ├── test_02.py
│   │   ├── ts_db
│   │   │   ├── test_01.py
│   │   │   ├── test_02.py
│   │   ├── main.py
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── run.sh

from common.desktop.login import login_wt
```

- `src/`
  - Main folder containing all test cases and environment variables
  - `common/`
    - Contains commonly used functions that are shared across test cases
    - Each platform will host its own folder hierarchy
    - Within each platform, it contains folders for specific user actions according to screen (e.g. trade, login, etc.)
      - All functions will be exported by `utils.py` for usage across the project
    - A `helper` library will be initialised which will hold most of the commonly used functions across test cases
  - `constants/`
    - Contains all test IDs of HTML elements being accessed by `selenium` when running the test cases
      - All test IDs will be initialissed within `DataTestID` class in `element_ids.py`
      - e.g. `LOGIN_SUBMIT = 'login-submit'`
  - `test/`
    - Contains all test suites and associated test cases of the test suites
    - Each test suite will have a dedicated folder to contain all test cases within the folder
- `pyproject.toml`
  - This file contains info on the build system details required for running your test cases
  - You do not need to make any changes here, keep this file as it is
- `requirements.txt`
  - This is the main file that defines all the libraries required for `run.sh` script to download and install the relevant libraries required for testing
    - Define the library and version in this format -> `<library>==<version-number>`
    - e.g. `pandas==2.2.0`
- `run.sh`
  - This is the main script file that you will have to execute on your terminal in order to run your test case
  - This script accepts an optional parameter that will allow you to run all test case within a single `.py` file
    - The script command will look like this: `./run.sh <file_name>.py` or `./run.sh <file_folder>`
    - e.g. `./run.sh test/ts_da` will run all test cases with prefix `test_` within the `test/ts_da` test suite e.g. `test_01.py`
    - e.g. `./run.sh test/ts_da/test_01.py` will run the specific test case `test_01.py` within the `test/ts_da` test suite
  - Alternatively, as we are using `pytest` as our main testing library, you could run the test directly using the following command:
    - Assumption: You have already downloaded the libraries required for running test cases through `pytest`
    - e.g. `pytest test/ts_da/test_01.py`

## Writing of test cases
- The test cases will be stored under the `test/` folder
- One test suite (e.g. TS_dA), will have a folder to contain the numerous test cases tied to the test suite
  - e.g.
    ```
      ├── test
      │   ├── ts_da
      │   │   ├── test_01.py
      │   │   ├── test_02.py
      │   ├── ts_db
      │   │   ├── test_01.py
    ```
- For every test case `.py` file, it must be initialised as a class.
  - e.g. 
    ```
      class TC_zA_001():
          @allure.title("TC_zA01 - Sample Test Case")
          def test_sample(self):
            ...
    ```
- `@allure.title` should only be applied onto the individual test case's title.
- For every test case step, it needs to be annotated with `with allure.step("")`
  e.g.
  ```
    from common.desktop.module_login.utils import login_wt
    from common.desktop.trade.utils import place_order
    from constants.helper.driver import shutdown

    class TC_zA_001():
        @allure.title("TC_zA01 - Place a Market Order on WT")
        def test_place_market_order(self):
          # Annotation should be done for every individual step indicated on test case
          with allure.step("Login onto WT"):
            login_wt()

          with allure.step("Place order on WT"):
            place_order()
          
          ...

          shutdown(driver)
  ```
## Generating test report using Allure
- Within the `run.sh` script commands, the results of the test cases/test suites that are being executed are being collected into the `allure_results/` folder.
- To view the test case report locally, run the following command:
  - `allure serve`
- If there are no errors occurring after running the above command, there will be a log in the terminal stating:
  - `Server started at <http://<ip-address>55001/>. Press <Ctrl+C> to exit`
- A webpage will be spawned, which will display your test case report. The URL of the webpage will be something like this:
  - `http://10.0.25.13:55001/index.html`