import pytest

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

    logger.info(f"Step 1: Modify order with {invalid_field!r}")
    web.trade_page.modals.modify_invalid_order(trade_object, **invalid_dict, submit=True)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, expected_message)


@pytest.fixture(scope="package", autouse=True)
def setup_test(create_order_data, limit_obj):
    trade_object = limit_obj(stop_loss=0, take_profit=0)

    logger.info(f"- Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    yield trade_object
