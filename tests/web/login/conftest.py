import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.utils.logging_utils import logger


@pytest.fixture(autouse=True)
def web():
    """
    Fixture to initialize and provide page objects for login tests.
    Handles driver setup, page navigation, and cleanup.
    """
    logger.info("- Initializing web driver")
    DriverManager.get_driver()

    yield WebContainer()

    logger.info("- Cleaning up web driver")
    DriverManager.quit_driver()


@pytest.fixture(autouse=True)
def setup_test(web):
    logger.info("- Navigating to login page...")
    web.login_page.goto()
