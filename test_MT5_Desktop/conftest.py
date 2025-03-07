import pytest
import chromedriver_autoinstaller

import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


"""
@pytest.fixture(scope="class")
def chromeDriver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

"""


# Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)



@pytest.fixture(scope="class")
def chromeDriver() -> WebDriver:
    # This will install the correct version of ChromeDriver if not already installed
    # To be commented out if using the remote
    chromedriver_autoinstaller.install()
    
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

    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # options.add_experimental_option("detach", True) # allows the Chrome browser to stay open after the script finishes.
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    # driver = webdriver.Remote('http://aqdev:aq123@selenium-grid.aquariux.dev/wd/hub', options=options)

    return driver