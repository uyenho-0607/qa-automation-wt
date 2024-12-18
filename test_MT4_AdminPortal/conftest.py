import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


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
    options.add_argument("--disable-cache") # Disable caching for fresh content
    options.add_argument("--start-maximized") # Maximize Chrome window
    options.add_argument("--incognito") # Opens the browser in incognito mode
    options.add_argument("--disable-extensions") # Disables all extensions for a faster and cleaner browser environment
    options.page_load_strategy = 'eager'  # Wait for full page load

    # options.add_experimental_option("detach", True)
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver
