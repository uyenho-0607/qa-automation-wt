import pytest

from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import AssetTabs, OrderType
from src.data.enums import Features
from src.data.objects.trade_object import ObjectTrade
from src.utils import DotDict
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


@pytest.fixture(scope="package", autouse=True)
def disable_OCT(disable_OCT):
    pass


@pytest.fixture
def setup_close_position_test(web, get_asset_tab_amount, symbol):
    tab_amount = get_asset_tab_amount(OrderType.MARKET)
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info("- Get Min volume value")
    min_vol = web.trade_page.place_order_panel.get_min_volume()

    if not tab_amount:
        logger.info("- Place new order")
        web.trade_page.place_order_panel.place_order(trade_object, submit=True)
        web.home_page.notifications.close_noti_banner()

        logger.info("- Wait for asset tab amount increase")
        web.trade_page.asset_tab.wait_for_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    web.trade_page.asset_tab.get_item_data(trade_object=trade_object)
    max_vol = trade_object.get("volume", 0)
    order_id = trade_object.get("order_id", 0)

    yield DotDict(
        tab_amount=tab_amount or 1,
        min_vol=min_vol,
        max_vol=max_vol,
        order_id=order_id
    )
