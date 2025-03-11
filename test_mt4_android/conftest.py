import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def android_driver(appium_server_url="http://localhost:4723/wd/hub"):
    # Set up desired capabilities using UiAutomator2Options
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'RFCTC0L5L0D'  # ROX - Device ID for your Android device
    # options.device_name = 'RF8NC185FLY'  # Device ID for your Android device
    # options.app_package = "com.aquariux.wt.release.lirunex"
    # options.app_activity = "com.aquariux.wt.release.lirunex.MainActivity"
    # options.app_package = "com.aquariux.wt.sit.lirunex"
    # options.app_activity = "com.aquariux.wt.sit.lirunex.MainActivity"
    options.app_package = "com.aquariux.lirunex.uat"
    options.app_activity = "com.aquariux.lirunex.uat.MainActivity"
    options.no_reset = True  # Keep app data between test sessions
    options.unicode_keyboard = True
    options.reset_keyboard = True
    options.new_command_timeout = 300  # Timeout for app initialization
    
    # Initialize the Appium driver
    driver = webdriver.Remote(command_executor=appium_server_url, options=options)
    
    return driver