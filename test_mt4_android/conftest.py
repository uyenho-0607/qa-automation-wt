import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
# def android_driver(appium_server_url="http://localhost:4723/wd/hub"):
def android_driver(appium_server_url="http://localhost:4723"):
    # Set up desired capabilities using UiAutomator2Options
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'RFCTC0L5L0D'  # ROX - Device ID for your Android device
    # options.device_name = 'RF8NC185FLY'  # Device ID for your Android device
    
    # Release SIT
    # options.app_package = "com.aquariux.wt.release.lirunex"
    # options.app_activity = "com.aquariux.wt.release.lirunex.MainActivity"
    
    # SIT 
    # options.app_package = "com.aquariux.wt.sit.lirunex"
    # options.app_activity = "com.aquariux.wt.sit.lirunex.MainActivity"
    
    # UAT
    options.app_package = "com.aquariux.lirunex.uat"
    options.app_activity = "com.aquariux.lirunex.uat.MainActivity"
    
    options.no_reset = True  # Do not reset app state
    # options.full_reset = False
    options.new_command_timeout = 300  # Timeout for app initialization
    options.set_capability("unicodeKeyboard", True)
    options.set_capability("resetKeyboard", True)
    options.set_capability("appium:clearSystemFiles", True) # Add clearSystemFiles
    # options.set_capability("appium:autoGrantPermissions", True)
    # options.set_capability("appium:resetOnSessionStartOnly", True)
    options.set_capability("appium:dontStopAppOnReset", False)
    options.set_capability("appium:shouldTerminateApp", True)
    # options.set_capability("appium:autoLaunch", True)
    # options.set_capability("appium:enableWebviewDetailsCollection", True) # Add clearSystemFiles
    # options.set_capability("setWebContentsDebuggingEnabled", True)

    # Initialize the Appium driver
    driver = webdriver.Remote(command_executor=appium_server_url, options=options)

    # yield driver
    return driver