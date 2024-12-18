import pytest
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


# from appium import webdriver
# from appium.options.android import UiAutomator2Options


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                DESKTOP
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Desktop Chrome


@pytest.fixture(scope="class")
def chromeDriver() -> WebDriver:
    chromedriver_autoinstaller.install() # This will install the correct version of ChromeDriver if not already installed
    
    # Configure ChromeDriver for mobile emulation
    mobile_emulation = {
        "deviceName": "Pixel 2"  # Use a predefined mobile device
    }

    options = Options()
    options.add_argument("--disable-cache") # Disable caching for fresh content
    options.add_argument("--start-maximized") # Maximize Chrome window
    options.add_argument("--incognito") # Opens the browser in incognito mode
    options.add_argument("--disable-extensions") # Disables all extensions for a faster and cleaner browser environment
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    # CHROME >= 115, using mac-arm64 as architecture identifier

    options.page_load_strategy = 'eager'  # Wait for full page load

    # enablePerformanceLogging= True, # analyze what's slowing things down, you can enable performance logging:
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    # driver = webdriver.Remote('http://localhost:4444/wd/hub', options=options)
    return driver


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ANDROID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# # Android Chrome

# @pytest.fixture(scope="class")
# def chromeDriver(appium_server_url="http://localhost:4723/wd/hub"):

# # def chromeDriver(appium_server_url="http://localhost:4723"):

#     # This will install the correct version of ChromeDriver if not already installed
#     chromedriver_path = chromedriver_autoinstaller.install()
#     # chromedriver_path = ChromeDriverManager().install()
    
#     capabilities = dict(
#         platformName='Android',
#         automationName = 'UiAutomator2',  # Make sure to use UiAutomator2
#         deviceName='RF8NC185FLY', # RFCTC0L5L0D / RF8NC185FLY
#         browserName='Chrome',
#         chromedriverExecutable=chromedriver_path,
#         unicodeKeyboard = True,
#         resetKeyboard = True,
#         pageLoadStrategy= "eager",
#         appium={'chromeOptions': {'w3c': False}}  # Add the Chrome options to disable W3C protocol
    
#         # enablePerformanceLogging= True, # analyze what's slowing things down, you can enable performance logging:
#     )
    
#     capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
    
#     # Create a new Appium driver instance
#     driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)
    
#     return driver

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                iOS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# iOS version
# @pytest.fixture(scope="class")
# def chromeDriver(appium_server_url="http://localhost:4723/wd/hub"):
    
#     capabilities = {
#         'platformName': 'iOS',
#         'browserName': 'Safari',
#         'deviceName': 'iPhone XS Max',
#         'automationName': 'XCUITest',
#         'udid': '00008020-0006308E260B002E',
#         'platformVersion': '18.1'
#     }

#     capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
#     driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

#     return driver

