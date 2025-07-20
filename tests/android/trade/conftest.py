import random

import pytest

from src.apis.api_client import APIClient
from src.apis.user_api import UserAPI
from src.core.driver.appium_driver import AppiumDriver
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.android_container import AndroidContainer
from src.data.enums import AssetTabs, Features, OrderType, WatchListTab
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def android():
    logger.info("- Init Android driver")
    DriverManager.get_driver()

    yield AndroidContainer()

    logger.info("- Clean up Android driver")
    DriverManager.quit_driver()

    logger.info("- Stop Appium service")
    AppiumDriver.stop_appium_service()


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(android, symbol):
    logger.info("- Login MemberSite")
    android.login_screen.login()
    android.home_screen.feature_anm_modal.got_it()

    logger.info("- Select watchlist tab ALL")
    android.home_screen.watch_list.select_tab(WatchListTab.CRYPTO)

    logger.info(f"- Select symbol: {symbol!r}")
    android.home_screen.watch_list.select_symbol(symbol)

    # logger.info(f"- Search & select symbol {symbol!r}")
    # android.home_screen.navigate_to(Features.HOME)
    # android.home_screen.search_and_select_symbol(symbol)


@pytest.fixture
def create_order_data(android):
    def _handler(trade_object):

        logger.info(f"- POST {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
        res = APIClient().trade.post_order(trade_object)

        # Loading new created data
        android.trade_screen.navigate_to(Features.HOME)
        android.home_screen.navigate_to(Features.TRADE)
        return res

    return _handler


@pytest.fixture
def enabl_OCT(android):
    logger.info("- Send API to enable OCT")
    APIClient().user.patch_oct()


@pytest.fixture
def disable_OCT(android):
    APIClient().user.patch_oct(enable=False)


@pytest.fixture
def setup_bulk_test(android, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):

        asset_tab = AssetTabs.get_tab(order_type)
        create_amount = random.randint(1, 10)
        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        if not order_ids:
            logger.info(f"- Place {create_amount} {order_type.upper()} orders")
            for _ in range(create_amount):
                APIClient().trade.post_order(ObjTrade(order_type=order_type, symbol=symbol), update_price=False)

        android.trade_screen.navigate_to(Features.HOME)
        android.home_screen.navigate_to(Features.TRADE)
        android.trade_screen.asset_tab.wait_for_tab_amount(asset_tab, expected_amount=create_amount)

        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        return order_ids

    return _handler
