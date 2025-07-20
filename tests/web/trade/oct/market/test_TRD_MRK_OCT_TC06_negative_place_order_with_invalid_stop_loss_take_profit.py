import pytest

from src.data.enums import OrderType
from src.data.objects.trade_object import ObjectTrade
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

"""
Scenarios: - Place new order
- invalid stop loss
- invalid take profit
"""


@pytest.mark.parametrize(
    "invalid_field", (
            "stop_loss",
            "take_profit",
            "stop_loss,take_profit",
    )
)
def test(web, invalid_field):
    order_type = OrderType.MARKET
    trade_object = ObjectTrade(order_type=order_type)

    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step: Place order with invalid: {invalid_field}")
    web.trade_page.place_order_panel.place_invalid_order(trade_object, **invalid_dict)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, UIMessages.INVALID_SL_TP_BANNER_DES)
