import random

import pytest

from src.data.enums import AssetTabs, OrderType, Features, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type", random.choices([
        [SLTPType.PRICE, SLTPType.PRICE],
        [SLTPType.POINTS, SLTPType.POINTS],
        SLTPType.sample_values(amount=2),
    ])
)
def test(android, symbol, get_asset_tab_amount, sl_type, tp_type):

    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab = AssetTabs.OPEN_POSITION

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} Order (sl_type:{sl_type!r}, tp_type:{tp_type!r}, tab:{tab_amount})")
    android.trade_screen.place_order_panel.open_pre_trade_details()
    android.trade_screen.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=sl_type)

    logger.info("Verify Order Submitted notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Step 3: Get placed orderID")
    android.trade_screen.asset_tab.get_last_order_id(trade_object)

    logger.info("Step 4: Navigate to Home screen")
    android.home_screen.navigate_to(Features.HOME)

    logger.info("Verify Open Position noti in Notification Box")
    android.home_screen.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id), go_back=False)

    # logger.info("Verify noti item details")
    # android.home_screen.notifications.verify_notification_details(trade_object)
    #
    logger.info("Step 5: Navigate to Trade screen")
    android.home_screen.navigate_to(Features.TRADE)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    android.trade_screen.asset_tab.verify_item_data(trade_object)
