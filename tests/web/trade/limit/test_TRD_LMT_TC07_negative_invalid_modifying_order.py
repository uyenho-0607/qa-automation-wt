import pytest

from src.data.enums import OrderType, AssetTabs
from src.data.objects.trade_obj import ObjTrade
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

"""
Scenarios: - Modify order
- invalid stop loss
- invalid take profit
- invalid stop_loss and take_profit
- invalid price (order_type != Market)
"""


@pytest.mark.parametrize(
    "invalid_field, expected_message", [
        ("entry_price", UIMessages.INVALID_PRICE_BANNER_DES),
        ("stop_loss", UIMessages.INVALID_SL_TP_BANNER_DES),
        ("take_profit", UIMessages.INVALID_SL_TP_BANNER_DES),
        ("stop_loss,take_profit", UIMessages.INVALID_SL_TP_BANNER_DES),
    ]
)
def test(web, invalid_field, expected_message, close_edit_confirm_modal, setup_test):

    trade_object = setup_test
    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step 1: Update placed order with {invalid_field!r}")
    web.trade_page.asset_tab.modify_invalid_order(trade_object, **invalid_dict, submit=True)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, expected_message)


@pytest.fixture(scope="package", autouse=True)
def setup_test(order_data, symbol, web):
    trade_object = ObjTrade(symbol=symbol, order_type=OrderType.LIMIT, stop_loss=0, take_profit=0)

    logger.info(f"- Place order for setup")
    order_data(trade_object, None, None)
    trade_object.order_id = web.trade_page.asset_tab.get_last_order_id(AssetTabs.PENDING_ORDER)

    yield trade_object
