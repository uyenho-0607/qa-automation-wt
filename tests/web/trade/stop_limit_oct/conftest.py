import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import Features
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web():
    DriverManager.get_driver()
    yield WebContainer()
    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(web, symbol):
    logger.info("- Login to MemberSite")
    web.home_page.goto()
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()

    logger.info("- Select Trade Page")
    web.home_page.navigate_to(Features.TRADE)

    logger.info(f"- Search and select symbol: {symbol}")
    web.home_page.search_symbol(symbol)
    web.home_page.select_item_from_search_result(symbol)


@pytest.fixture(autouse=True, scope="package")
def enable_OCT(enable_OCT):
    pass
