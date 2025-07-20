import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, symbol, get_asset_tab_amount, close_confirm_modal):
    trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} order")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values())

    logger.info("Step 2: Cancel Place Order")
    web.trade_page.modals.close_trade_confirm_modal()

    logger.info(f"Verify Asset Tab amount is not changed: {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)
