import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import WatchListTab
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web():
    logger.info("- Init Web Driver")
    DriverManager.get_driver()

    yield WebContainer()

    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package", autouse=True)
def setup_home_tests(web, symbol):
    logger.info("- Navigate to Login Page")
    web.home_page.goto()

    logger.info(f"- Login MemberSite")
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()


@pytest.fixture
def get_current_symbol(web):
    def _handler(tab: WatchListTab = WatchListTab.ALL):
        symbols = web.trade_page.watch_list.get_current_symbols(tab)
        return symbols

    return _handler
