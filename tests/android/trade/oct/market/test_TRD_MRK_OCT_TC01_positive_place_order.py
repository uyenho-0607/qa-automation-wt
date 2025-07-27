import pytest

from src.data.enums import AssetTabs, OrderType, Features, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "sl_type, tp_type", (
            [None, None],
            [SLTPType.PRICE, SLTPType.PRICE],
            [SLTPType.POINTS, SLTPType.POINTS],
            SLTPType.sample_values(amount=2),
    )
)
def test(android, symbol, get_asset_tab_amount, sl_type, tp_type, ):
    # -------------------
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab = AssetTabs.OPEN_POSITION
    tab_amount = get_asset_tab_amount(trade_object.order_type)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with sl_type: {sl_type!r}, tp_type: {tp_type!r}")
    android.trade_screen.place_order_panel.open_pre_trade_details()
    android.trade_screen.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=sl_type)

    logger.info("Verify notification banner displays correct input trade information")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(tab, tab_amount + 1)
    android.trade_screen.asset_tab.get_last_order_id(trade_object)

    logger.info("Verify Open Position noti in Notification Box")
    android.home_screen.navigate_to(Features.HOME)
    android.home_screen.notifications.verify_notification_result(
        ObjNoti(trade_object).open_position_details(trade_object.order_id), go_back=False
    )

    logger.info("Verify noti item details")
    android.home_screen.notifications.verify_notification_details(trade_object)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    android.home_screen.navigate_to(Features.TRADE)
    android.trade_screen.asset_tab.verify_item_data(trade_object)
