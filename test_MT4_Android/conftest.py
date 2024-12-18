import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options



@pytest.fixture(scope="class")
def init_driver(appium_server_url="http://localhost:4723/wd/hub"):

    capabilities = dict(
        platformName = 'Android',
        automationName = 'UiAutomator2',  # Make sure to use UiAutomator2
        # deviceName = 'RF8NC185FLY',
        deviceName = 'RFCTC0L5L0D', # Rox
        appPackage = "com.aquariux.wt.release.lirunex",
        appActivity = "com.aquariux.wt.release.lirunex.MainActivity",
        noReset = True,
        unicodeKeyboard = True,
        resetKeyboard = True,
        pageLoadStrategy= "eager",
        # enablePerformanceLogging= True, # analyze what's slowing things down, you can enable performance logging:
    )

    capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
    return driver