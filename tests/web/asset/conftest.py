import random

import pytest

from src.apis.api_client import APIClient
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_container import WebContainer
from src.data.enums import AssetTabs, OrderType, Features
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web():
    logger.info("- Init Web Driver")
    DriverManager.get_driver()

    yield WebContainer()

    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package", autouse=True)
def setup_asset_test(web):
    logger.info("- Navigate to Login Page")
    web.home_page.goto()

    logger.info(f"- Login MemberSite")
    web.login_page.login()
    web.home_page.feature_announcement_modal.got_it()


@pytest.fixture
def search_symbol(web, symbol):
    logger.info(f"- Search and select symbol: {symbol}")
    web.home_page.search_symbol(symbol)
    web.home_page.select_item_from_search_result(symbol)
    yield


@pytest.fixture
def setup_bulk_asset_test(web, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):

        asset_tab = AssetTabs.get_tab(order_type)
        create_amount = random.randint(1, 5)

        logger.info("- Get asset tab amount")
        tab_amount = APIClient().order.get_counts(order_type=order_type)

        if not tab_amount:

            trade_object = ObjectTrade(order_type=order_type, symbol=symbol)
            logger.info(f"- Place {create_amount} {trade_object.trade_type.upper()} {trade_object.order_type.upper()}")
            for _ in range(create_amount):
                APIClient().trade.post_order(trade_object)

        logger.info("- Navigate to Asset Page")
        web.home_page.navigate_to(Features.ASSETS, wait=False)

        order_ids = web.trade_page.asset_tab.get_order_id_list(asset_tab)
        logger.debug(f"- Current order_ids: {order_ids}")

        return tab_amount or create_amount, order_ids

    return _handler
