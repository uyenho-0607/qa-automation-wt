import builtins
import subprocess

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from selenium.common import WebDriverException

from src.core.config_manager import Config
from src.data.project_info import DriverList
from src.utils.common_utils import get_connected_device
from src.utils.logging_utils import logger


class AppiumDriver:
    _appium_service = None

    @classmethod
    def start_appium_service(cls, host="localhost", port=4723):

        kill_command = f"lsof -ti :{port} | xargs kill -9"
        subprocess.run(kill_command, shell=True, check=True)

        cls._appium_service = AppiumService()
        args = [
            "-pa", "/wd/hub",
            "--address", host,
            "--port", str(port),
        ]

        logger.debug("- Starting appium service...")
        cls._appium_service.start(args=args, timeout_ms=30000)
        logger.info("- Appium service started !")

    @classmethod
    def init_android_driver(cls, host="http://localhost", port=4723) -> webdriver.Remote:

        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.udid = Config.mobile().device_udid or get_connected_device()
        options.app_package = Config.mobile().app_id
        options.app_activity = ".MainActivity"
        options.app_wait_activity = ".MainActivity"
        options.auto_grant_permissions = True
        options.no_reset = False
        options.full_reset = False
        options.new_command_timeout = 30000
        options.set_capability("appium:dontStopAppOnReset", False)
        options.set_capability("appium:shouldTerminateApp", True)

        if not cls._appium_service:
            cls.start_appium_service()

        try:
            logger.debug("- Init android driver...")
            driver = webdriver.Remote(f"{host}:{port}/wd/hub", options=options)
            setattr(builtins, "android_driver", driver)

            DriverList.all_drivers["android"] = driver
            logger.info("- Android driver init !")
            return driver

        except WebDriverException as error:
            raise WebDriverException(f"Failed to init resources driver with error: {error!r}")

    @classmethod
    def init_ios_driver(cls, host="http://localhost", port=4723) -> webdriver.Remote:
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.udid = Config.mobile().device_udid or get_connected_device()
        options.bundle_id = Config.mobile().app_id
        options.auto_accept_alerts = True
        options.no_reset = False
        options.full_reset = False
        options.use_prebuilt_wda = True
        options.new_command_timeout = 30000
        options.set_capability("appium:dontStopAppOnReset", False)
        options.set_capability("appium:shouldTerminateApp", True)
        options.set_capability("wdaStartupRetries", 2)
        options.set_capability("wdaStartupRetryInterval", 20000)

        if not cls._appium_service:
            cls.start_appium_service()

        try:
            logger.debug("- Init iOS driver...")
            driver = webdriver.Remote(f"{host}:{port}/wd/hub", options=options)
            setattr(builtins, "ios_driver", driver)

            DriverList.all_drivers["ios"] = driver
            logger.info("- iOS driver init !")
            return driver

        except WebDriverException as error:
            raise WebDriverException(f"Failed to init iOS driver with error: {error!r}")

    @classmethod
    def quit_mobile_driver(cls, platform):
        if DriverList.all_drivers.get(platform):
            DriverList.all_drivers[platform].quit()
            DriverList.all_drivers[platform] = None

    @classmethod
    def stop_appium_service(cls):
        if cls._appium_service:
            cls._appium_service.stop()
            cls._appium_service = None
