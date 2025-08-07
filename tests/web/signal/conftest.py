import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import SignalTab, Features
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site, web):
    logger.info("- Navigate to Signal Page")
    web.home_page.navigate_to(Features.SIGNAL)


@pytest.fixture
def get_current_symbol(web):
    def _handler(tab: SignalTab = SignalTab.SIGNAL_LIST):
        symbols = web.signal_page.get_current_symbols(tab)
        return symbols

    return _handler
