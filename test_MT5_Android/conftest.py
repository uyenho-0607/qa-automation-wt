import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options



# adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp' run to know the current app

@pytest.fixture(scope="class")
def init_driver(appium_server_url="http://localhost:4723/wd/hub"):

    capabilities = dict(
        platformName = 'Android',
        automationName = 'UiAutomator2',  # Make sure to use UiAutomator2
        deviceName = 'RF8NC185FLY',
        appPackage = "com.aquariux.wt.release.transactcloudmt5",
        appActivity = "com.aquariux.wt.release.transactcloudmt5.MainActivity",
        noReset = True,
        # unicodeKeyboard = True,
        # resetKeyboard = True,
    )

    capabilities_options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)
    return driver