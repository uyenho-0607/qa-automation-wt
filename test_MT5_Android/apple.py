import unittest
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy


# For Simulator
capabilities_simulator = dict(
    platformName='iOS',
    automationName='XCUITest',
    deviceName='iPhone 15 Pro',
    platformVersion='17.5',
    #appPackage='com.aquariux.wt.release.lirunex',
    appPackage='com.apple.Preferences',
    language='en',
    locale='US'
)

# For Real Device
capabilities_device = dict(
    platformName='iOS',
    automationName='XCUITest',
    deviceName='Nicodemus\'s iPhone',
    udid='00008120-001A79A03AA0C01E',
    #udid='auto',
    platformVersion='17.5.1',
    #app='com.apple.Preferences',
    app='com.aquariux.wt.release.lirunex',
    xcodeOrgId='Nicodemus Chan',
    useNewWDA=False,
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=XCUITestOptions().load_capabilities(capabilities_device))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:
        #el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
        self.driver.implicitly_wait(7)
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Sign in"]')
        el.click()


if __name__ == '__main__':
    unittest.main()
