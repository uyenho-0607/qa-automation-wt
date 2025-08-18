import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_app_container import WebAppContainer
from src.utils.logging_utils import logger


@pytest.fixture
def web_app():
    logger.info("- Init Web Driver")
    DriverManager.get_driver()

    yield WebAppContainer()

    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(autouse=True)
def setup_test(web_app):
    logger.info("- Navigating to login page...")
    web_app.login_page.goto()
