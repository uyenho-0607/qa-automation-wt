import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from common.mobileapp.helper.element import find_element_by, populate_element_with_wait


def init_driver(appium_server_url="http://localhost:4723/wd/hub"):

    capabilities = dict(
        platformName='Android',
        automationName='UiAutomator2',  # Make sure to use UiAutomator2
        deviceName='RF8NC185FLY',
        appPackage="com.aquariux.wt.release.lirunex",
        appActivity="com.aquariux.wt.release.lirunex.MainActivity"
    )

    capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
    return driver


# Example usage
driver = init_driver()

time.sleep(30)
# Find an element by id and click it (replace with actual element locators)
element = find_element_by(driver, AppiumBy.XPATH, "//android.view.ViewGroup[3]/android.widget.EditText")
populate_element_with_wait(driver, element=element, text="test")


# ... Perform other actions on the app ...

# No need to call launch_app here, app launches during session creation
