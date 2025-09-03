import builtins
import os
import subprocess

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from selenium.common import WebDriverException

from src.core.config_manager import Config
from src.data.project_info import DriverList, RuntimeConfig
from src.utils.common_utils import get_connected_device
from src.utils.logging_utils import logger

DEVICEFARM_DEVICE_NAME = os.getenv("DEVICEFARM_DEVICE_NAME")
DEVICEFARM_DEVICE_PLATFORM_NAME = os.getenv("DEVICEFARM_DEVICE_PLATFORM_NAME")
DEVICEFARM_APP_PATH = os.getenv("DEVICEFARM_APP_PATH")
IOS_DEVICEFARM_UDID = os.getenv("DEVICEFARM_DEVICE_UDID_FOR_APPIUM")
ANDROID_DEVICEFARM_UDID = os.getenv("DEVICEFARM_DEVICE_UDID")

class AppiumDriver:
    _appium_service = None

    @classmethod
    def start_appium_service(cls, host="localhost", port=4723):
        # Kill any existing process on the port (with error handling)
        kill_command = f"lsof -ti :{port} | xargs kill -9"
        try:
            subprocess.run(kill_command, shell=True, check=True)
            logger.debug(f"- Killed existing process on port {port}")
        except subprocess.CalledProcessError:
            # No process running on the port, which is fine
            logger.debug(f"- No existing process found on port {port}")

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

        cd = RuntimeConfig.argo_cd
        options = UiAutomator2Options()
        options.platform_name = DEVICEFARM_DEVICE_PLATFORM_NAME if cd else "Android"
        options.device_name = DEVICEFARM_DEVICE_NAME if cd else ""
        options.udid = ANDROID_DEVICEFARM_UDID if cd else Config.mobile().device_udid or get_connected_device()

        if not cd:
            options.app_package = Config.mobile().app_id
            options.app_activity = ".MainActivity"
            options.app_wait_activity = ".MainActivity"
            options.no_reset = False

        options.auto_grant_permissions = True
        options.full_reset = True if cd else False
        options.new_command_timeout = 30000
        options.set_capability("appium:dontStopAppOnReset", False)
        options.set_capability("appium:shouldTerminateApp", True)

        if cd:
            options.app = DEVICEFARM_APP_PATH

        if not cls._appium_service and not cd:
            cls.start_appium_service()

        try:
            logger.debug("- Init android driver...")
            driver = webdriver.Remote(f"{host}:{port}/wd/hub", options=options)
            setattr(builtins, "android_driver", driver)

            DriverList.all_drivers["android"] = driver
            logger.info("- Android driver init !")
            return driver

        except WebDriverException as error:
            logger.error(f"Failed to init android driver: {error}")
            raise WebDriverException(f"Failed to init android driver with error: {error!r}")


    @classmethod
    def init_ios_driver(cls, host="http://localhost", port=4723) -> webdriver.Remote:
        options = XCUITestOptions()

        if RuntimeConfig.argo_cd:
            options.device_name = DEVICEFARM_DEVICE_NAME
            options.platform_name = DEVICEFARM_DEVICE_PLATFORM_NAME
            options.udid = IOS_DEVICEFARM_UDID
            options.app = DEVICEFARM_APP_PATH
            options.full_reset = True

        else:
            options.platform_name = "iOS"
            options.udid = Config.mobile().device_udid or get_connected_device()
            options.bundle_id = Config.mobile().app_id
            options.full_reset = False

        options.auto_accept_alerts = True
        options.no_reset = False
        options.use_prebuilt_wda = True
        options.new_command_timeout = 30000
        options.set_capability("appium:dontStopAppOnReset", False)
        options.set_capability("appium:shouldTerminateApp", True)
        options.set_capability("wdaStartupRetries", 2)
        options.set_capability("wdaStartupRetryInterval", 20000)

        if not cls._appium_service and not RuntimeConfig.argo_cd:
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