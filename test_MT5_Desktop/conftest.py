import pytest
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
# from typing import Generator


"""
@pytest.fixture(scope="class")
def chromeDriver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

"""

@pytest.fixture(scope="class")
def chromeDriver() -> WebDriver:
    
    chromedriver_autoinstaller.install() # This will install the correct version of ChromeDriver if not already installed
    
    options = Options()
    options.add_argument("--incognito") # Opens the browser in incognito mode
    options.add_argument("--disable-cache") # Disable caching for fresh content
    options.add_argument("--start-maximized") # Maximize Chrome window
    options.add_argument("--disable-extensions") # Disables all extensions for a faster and cleaner browser environment
    
    # options.add_argument("--auto-open-devtools-for-tabs") # This opens the DevTools automatically
    
    # options.add_argument("--headless") # Headless mode, faster as it does not render UI
    options.add_argument("--disable-popup-blocking") # Disable popup blocking
    options.add_argument("--disable-infobars")

    options.page_load_strategy = 'eager'  # Wait for full page load (Options: 'normal', 'eager', 'none')

    # options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # options.add_experimental_option("detach", True) # allows the Chrome browser to stay open after the script finishes.
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    # driver = webdriver.Remote('http://localhost:4444/wd/hub', options=options)
    return driver





# @pytest.fixture(scope="class")
# def safariDriver() -> Generator[WebDriver, None, None]:
#     # Initialize Safari WebDriver directly
#     driver = webdriver.Safari()

#     yield driver  # This allows the test to use the driver

#     driver.quit() # Cleanup after tests
