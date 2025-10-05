import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, Features, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(login_wt_app, android):

    logger.info("[Setup] Select any symbol from watch list", setup=True)
    android.home_screen.watch_list.select_last_symbol()

    logger.info("[Setup] Check if OCT mode is enabled/disabled in Admin Config", setup=True)
    is_enable = android.trade_screen.place_order_panel.is_oct_enable()

    if is_enable:
        logger.info("[Setup] OCT mode is enabled in Admin config - Disable OCT", setup=True)
        android.trade_screen.place_order_panel.toggle_oct(enable=False, confirm=True)

    else:
        logger.info("[Setup] OCT mode already disabled in Admin Config", setup=True)

@pytest.fixture
def setup_bulk_asset_test(android, symbol):
    def _handler(order_type: OrderType = OrderType.MARKET):
        asset_tab = AssetTabs.get_tab(order_type)

        create_amount = random.randint(1, 5)

        tab_amount = APIClient().order.get_counts(order_type=order_type)

        trade_object = ObjTrade(order_type=order_type, symbol=symbol)
        logger.info(f"- Place {create_amount} {trade_object.trade_type.upper()} {trade_object.order_type.upper()}")
        for _ in range(create_amount):
            APIClient().trade.post_order(trade_object, update_price=False)

        logger.info("- Navigate to Asset Page")
        android.trade_screen.navigate_to(Features.ASSETS)

        logger.info("- Navigate to View all Transaction page")
        android.assets_screen.click_view_all_transaction()

        order_ids = APIClient().order.get_order_id_list(symbol, order_type)

        return tab_amount, order_ids

    return _handler
