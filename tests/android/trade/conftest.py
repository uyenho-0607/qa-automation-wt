import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, Features, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup_trade_test(login_wt_app, android, symbol):

    logger.info(f"[Setup] Search and select symbol: {symbol!r}", setup=True)
    android.home_screen.search_and_select_symbol(symbol)


@pytest.fixture
def create_order_data(android):
    def _handler(trade_object):
        tab = AssetTabs.get_tab(trade_object.order_type)
        current_amount = android.trade_screen.asset_tab.get_tab_amount(tab)

        logger.info(f"- POST {trade_object.trade_type.upper()} {trade_object.order_type.upper()} order")
        res = APIClient().trade.post_order(trade_object)

        # Loading new created data
        android.trade_screen.asset_tab.wait_for_tab_amount(tab, expected_amount=current_amount + 1)

        return res, current_amount + 1

    return _handler


@pytest.fixture(scope="package")
def enable_OCT(enable_OCT):
    pass


@pytest.fixture(scope="package")
def disable_OCT(disable_OCT):
    pass


@pytest.fixture(scope="package")
def swap_to_volume():
    logger.info("[Setup] Send API to use volume")
    APIClient().user.patch_swap_volume_units()


@pytest.fixture(scope="package")
def swap_to_units():
    logger.info("[Setup] Send API to use units")
    APIClient().user.patch_swap_volume_units(use_volume=False)


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


@pytest.fixture
def close_edit_confirmation(android):
    yield
    android.trade_screen.modals.close_edit_confirm_modal()
