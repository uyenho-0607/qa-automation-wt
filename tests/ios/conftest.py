from contextlib import suppress

import pytest
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.ios_container import iOSContainer
from src.data.consts import FAILED_ICON_COLOR
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def ios():
    logger.info("- Init ios driver")
    DriverManager.get_driver()

    yield iOSContainer()

    logger.info("- Clean up ios driver")
    DriverManager.quit_driver()

    logger.info("- Stop Appium service")
    AppiumDriver.stop_appium_service()


@pytest.fixture(scope="package")
def login_wt_app(ios):
    return

    if not RuntimeConfig.argo_cd:
        # currently, cannot reset login state of app -> temporarily check if app is logged in -> perform logout
        if ios.home_screen.on_home_screen():
            logger.info("- App is logged in, logout first", setup=True)
            ios.home_screen.settings.logout()

    # handle login with max attempts = 3
    max_retries = 3

    logger.info("- Login to WT app", setup=True)
    ios.login_screen.login(wait=True)

    logger.info("- Skip feature ann modal if any", setup=True)
    ios.home_screen.feature_anm_modal.got_it()

    logger.info("- Wait for home screen loaded", setup=True)


    for attempt in range(max_retries + 1):
        if not ios.home_screen.on_home_screen():
            with suppress(Exception):
                logger.info("- Perform login again", setup=True)
                ios.login_screen.login(wait=True)
                ios.home_screen.feature_anm_modal.got_it()

        else:
            break

        if attempt == max_retries - 1 and not ios.home_screen.on_home_screen():
            # login one more time to catch the screenshot
            ios.login_screen.login()
            raise RuntimeError(f"Setup test failed ! Unable to Login to WT {FAILED_ICON_COLOR}")


@pytest.fixture(scope="package")
def disable_OCT(ios):
    """disable OCT from place order panel"""
    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = ios.trade_screen.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] OCT mode is enabled in Admin config - Disable OCT", setup=True)
        ios.trade_screen.place_order_panel.toggle_oct(enable=False, submit=True)

    else:
        logger.info("[Setup] OCT mode already disabled in Admin Config", setup=True)


@pytest.fixture(scope="package")
def enable_OCT(ios):
    """enable OCT from place order panel"""
    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = ios.trade_screen.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] OCT mode is enabled in Admin config - Enable OCT", setup=True)
        ios.trade_screen.place_order_panel.toggle_oct(enable=True, submit=True)

    else:
        pytest.skip("OCT mode is disabled in Admin Config - SKIP this test ")
