import pytest

from src.data.enums import AssetTabs, SLTPType
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, market_obj, cancel_all):
    trade_object = market_obj()

    logger.info("Step 1: Get asset tab amount")
    tab_amount = web_app.trade_page.asset_tab.get_tab_amount(AssetTabs.OPEN_POSITION)

    logger.info(f"Step 2: Place {trade_object.trade_type} order")
    web_app.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values())

    logger.info("Step 3: Cancel Place Order")
    web_app.trade_page.modals.confirm_trade(confirm=False)

    logger.info(f"Verify Asset Tab amount is not changed: {tab_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)
