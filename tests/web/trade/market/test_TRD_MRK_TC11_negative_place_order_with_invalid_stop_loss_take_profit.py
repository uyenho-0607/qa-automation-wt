import pytest

from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger

"""
Scenarios: - Place new order & modify order
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
def test(web, invalid_field, market_obj):
    trade_object = market_obj()

    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step 1: Place order with invalid: {invalid_field}")
    web.trade_page.place_order_panel.place_invalid_order(trade_object, **invalid_dict, submit=True)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, UIMessages.INVALID_SL_TP_BANNER_DES)
