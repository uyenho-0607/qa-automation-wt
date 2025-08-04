import pytest

from src.core.page_container.web_app_container import WebAppContainer
from src.core.driver.driver_manager import DriverManager
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web_app():
    logger.info("- Init Web Driver")
    DriverManager.get_driver()

    yield WebAppContainer()

    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package")
def login_member_site(web_app):
    logger.info("- Navigate to WT Member Site")
    web_app.login_page.goto()

    logger.info("- Login to Member Site")
    web_app.login_page.login(wait=True)
    web_app.home_page.feature_anm_modal.got_it()
