import pytest

from src.data.enums import OrderType
from src.data.objects.trade_obj import ObjTrade
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

"""
Scenarios: - Place new order
- invalid stop loss
- invalid take profit
- invalid price
"""


@pytest.mark.parametrize(
    "invalid_field, expected_message", [
        ("entry_price", UIMessages.INVALID_PRICE_BANNER_DES),
        ("stop_loss", UIMessages.INVALID_SL_TP_BANNER_DES),
        ("take_profit", UIMessages.INVALID_SL_TP_BANNER_DES),
        ("stop_loss,take_profit", UIMessages.INVALID_SL_TP_BANNER_DES),
    ]
)
def test(web, invalid_field, expected_message):
    order_type = OrderType.STOP_LIMIT
    trade_object = ObjTrade(order_type=order_type)

    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step 1: Place order with invalid: {invalid_field}")
    web.trade_page.place_order_panel.place_invalid_order(trade_object, **invalid_dict, submit=True)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, expected_message)


@pytest.fixture(autouse=True)
def cleanup(web):
    yield
    web.home_page.notifications.close_noti_banner()