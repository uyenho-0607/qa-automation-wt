import pytest

from src.data.enums import OrderType
from src.data.objects.trade_object import ObjectTrade
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger
from tests.web.trade.conftest import create_order_data

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
def test(web, setup_test, invalid_field, close_edit_confirm_modal):
    trade_object = setup_test
    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step 1: Update item with {invalid_field!r}")
    web.trade_page.modals.modify_invalid_order(trade_object, **invalid_dict)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, UIMessages.INVALID_SL_TP_BANNER_DES)


@pytest.fixture(scope="package", autouse=True)
def setup_test(create_order_data, symbol):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol, stop_loss=0, take_profit=0)

    logger.info(f"- Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    yield trade_object
