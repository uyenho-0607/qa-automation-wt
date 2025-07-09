from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.utils.logging_utils import logger


def test(web, symbol, setup_bulk_asset_test, cancel_bulk_delete):
    # -------------------
    tab_amount, order_ids = setup_bulk_asset_test(OrderType.STOP)
    # -------------------
    logger.info("Step 1: Bulk delete pending orders")
    web.trade_page.asset_tab.bulk_delete_orders()

    logger.info("Verify bulk delete notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti.bulk_delete_order_banner(order_ids))

    logger.info(f"Verify asset tab amount is: {tab_amount - len(order_ids)}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount - len(order_ids))
