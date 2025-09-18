import random

import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, symbol, close_confirm_modal):

    trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol)

    logger.info("Step 1: Get current tab amount of Pending Orders")
    tab_amount = web.trade_page.asset_tab.get_tab_amount(AssetTabs.PENDING_ORDER)

    logger.info(f"Step 2: Place {trade_object.trade_type} order (tab amount:{tab_amount})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values())

    logger.info("Step 3: Cancel Place Order")
    web.trade_page.modals.close_trade_confirm_modal()

    logger.info(f"Verify Asset Tab amount is not changed: {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)
