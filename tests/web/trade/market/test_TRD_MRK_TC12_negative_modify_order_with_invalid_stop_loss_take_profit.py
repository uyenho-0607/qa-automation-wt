import pytest

from src.data.enums import OrderType
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
    "invalid_field", (
            "stop_loss",
            "take_profit",
            "stop_loss,take_profit",
    )
)
def test(web, invalid_field, close_edit_confirm_modal, setup_test):

    trade_obj = setup_test
    invalid_dict = {key: True for key in invalid_field.split(",")}

    logger.info(f"Step 1: Modify order with {invalid_field!r}")
    web.trade_page.asset_tab.modify_invalid_order(trade_obj, **invalid_dict, submit=True)

    logger.info("Verify invalid notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.INVALID_ORDER_BANNER_TITLE, UIMessages.INVALID_SL_TP_BANNER_DES)



@pytest.fixture(scope="package", autouse=True)
def setup_test(create_order_data, symbol):
    trade_obj = ObjTrade(stop_loss=0, take_profit=0, symbol=symbol, order_type=OrderType.MARKET)

    logger.info(f"- Place {trade_obj.trade_type} Order")
    create_order_data(trade_obj)
    yield trade_obj
