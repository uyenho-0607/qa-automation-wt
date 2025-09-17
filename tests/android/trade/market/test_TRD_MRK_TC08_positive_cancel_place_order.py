import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test_cancel_order(android, symbol, get_asset_tab_amount):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} order")
    android.trade_screen.place_order_panel.place_order(trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values())

    logger.info("Step 2: Cancel Place Order")
    android.trade_screen.modals.confirm_trade(confirm=False)

    logger.info(f"Verify Asset Tab amount is not changed: {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)


def test_cancel_bulk_order(android, symbol, get_asset_tab_amount, setup_bulk_test):

    setup_bulk_test(order_type=OrderType.MARKET)
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)
    # -------------------

    logger.info("Step 1: Click on Bulk Close - Cancel action")
    android.trade_screen.asset_tab.bulk_close_positions()

    logger.info(f"Verify Asset Tab amount is not changed: {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)
