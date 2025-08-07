from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


def test(android, symbol, setup_bulk_test, cancel_bulk_delete):
    order_ids = setup_bulk_test(order_type=OrderType.STOP_LIMIT)
    expected_amount = 0 if len(order_ids) <= 30 else 30 - len(order_ids)
    # -------------------

    logger.info(f"Step 1: Bulk delete orders")
    android.trade_screen.asset_tab.bulk_delete_orders()

    logger.info(f"Verify bulk delete notification banner")
    android.home_screen.notifications.verify_notification_banner(*ObjNoti.bulk_delete_order_banner(order_ids))
    android.home_screen.notifications.close_noti_banner()

    logger.info(f"Verify asset tab amount is {expected_amount}")
    android.trade_screen.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, expected_amount)
