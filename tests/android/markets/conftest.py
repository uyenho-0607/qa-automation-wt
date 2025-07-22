import pytest

from src.utils.logging_utils import logger


#
#
# @pytest.fixture(scope="package")
# def android():
#
#     logger.info("- Init Android driver")
#     DriverManager.get_driver()
#     actions = MobileActions()
#
#     yield AndroidContainer(actions)
#
#     logger.info("- Clean up Android driver")
#     DriverManager.quit_driver()
#
#     logger.info("- Stop Appium service")
#     AppiumDriver.stop_appium_service()
#
#
@pytest.fixture(scope="package", autouse=True)
def setup_login(android):

    logger.info(f"- Login to MemberSite")
    android.login_screen.login(wait=True)
    android.home_screen.feature_anm_modal.got_it()
