import pytest

from src.data.enums import OrderType, SLTPType, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.data.ui_messages import UIMessages
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger

"""
Scenarios: - Modify order
- invalid stop loss
- invalid take profit
- invalid stop_loss and take_profit
- invalid price (order_type != Market)
"""


@pytest.mark.parametrize(
    "invalid_field", (
            "stop_loss",
            "take_profit",
            "stop_loss,take_profit",
    )
)
def test(web, invalid_field, close_edit_confirm_modal, setup_test):

    trade_obj = setup_test
    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step 1: Update placed order with {invalid_field!r}")
    web.trade_page.asset_tab.modify_invalid_order(trade_obj, **invalid_dict, submit=True)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, UIMessages.INVALID_SL_TP_BANNER_DES)



@pytest.fixture(scope="package", autouse=True)
def setup_test(order_data, market_obj, web):
    trade_obj = market_obj()

    logger.info(f"- Place order with: {format_display_dict(trade_obj)}")
    order_data(trade_obj, SLTPType.PRICE, SLTPType.PRICE)
    trade_obj.order_id = web.trade_page.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION)
    yield trade_obj
