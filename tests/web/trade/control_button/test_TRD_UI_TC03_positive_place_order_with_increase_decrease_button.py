import random

import pytest

from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "order_type", (
            OrderType.MARKET,
            random.choice([OrderType.LIMIT, OrderType.STOP]),
            OrderType.STOP_LIMIT,
    )
)
def test(web, symbol, get_asset_tab_amount, order_type):
    # -------------------

    tab = AssetTabs.get_tab(order_type)

    trade_object = ObjTrade(order_type=order_type, symbol=symbol)
    tab_amount = get_asset_tab_amount(order_type)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} Order with control button")
    web.trade_page.place_order_panel.place_order_by_control_button(trade_object, input_value=random.randint(0, 1))

    logger.info(f"Verify trade confirmation")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 2: Confirm place order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
