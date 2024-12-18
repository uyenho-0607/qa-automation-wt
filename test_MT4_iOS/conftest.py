import pytest

from appium import webdriver
from appium.options.ios import XCUITestOptions



@pytest.fixture(scope="class")
def init_driver(appium_server_url="http://localhost:4723/wd/hub"):

    capabilities = dict(
        platformName='iOS',
        automationName='XCUITest',
        deviceName='Nicodemus\'s iPhone',
        udid='00008120-001A79A03AA0C01E',
        #udid='auto',
        platformVersion='17.5.1',
        #app='com.apple.Preferences',
        app='com.aquariux.wt.release.lirunex',
        xcodeOrgId='Nicodemus Chan',
        useNewWDA=False, # driver to auto install 
        language='en',
        locale='US'
    )

    capabilities_options = XCUITestOptions().load_capabilities(capabilities)
    driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
    
    
    # driver = webdriver.Remote(appium_server_url, options=XCUITestOptions().load_capabilities(capabilities))

    return driver