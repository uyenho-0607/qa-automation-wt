from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


def test(web_app, symbol, setup_bulk_test, cancel_bulk_delete):
    order_ids = setup_bulk_test(order_type=OrderType.STOP)
    expected_amount = 0 if len(order_ids) <= 30 else 30 - len(order_ids)
    # -------------------

    logger.info(f"Step 1: Bulk delete orders")
    web_app.trade_page.asset_tab.bulk_delete_orders()

    logger.info(f"Verify bulk delete notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti.bulk_delete_order_banner(order_ids))
    web_app.home_page.notifications.close_noti_banner()

    logger.info(f"Verify asset tab amount is {expected_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, expected_amount)
