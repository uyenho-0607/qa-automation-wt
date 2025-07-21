import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import SignalTab, Features
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
    logger.info("- Navigate  & Login to MemberSite")
    web.home_page.goto()
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()

    logger.info("- Navigate to Signal Page")
    web.home_page.navigate_to(Features.SIGNAL)


@pytest.fixture
def get_current_symbol(web):
    def _handler(tab: SignalTab = SignalTab.SIGNAL_LIST):
        symbols = web.signal_page.get_current_symbols(tab)
        return symbols

    return _handler
