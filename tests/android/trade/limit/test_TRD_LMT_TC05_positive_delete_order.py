from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade

from src.utils.logging_utils import logger


def test(android, symbol, get_asset_tab_amount, cancel_delete_order, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.LIMIT, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)
    # ------------------- #

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info(f"Verify asset tab amount: {tab_amount + 1}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 2: Delete pending order")
    android.trade_screen.asset_tab.delete_pending_order(trade_object=trade_object)

    logger.info("Verify Delete order notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify asset tab amount: {tab_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)

    logger.info("Verify item is no longer displayed")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
