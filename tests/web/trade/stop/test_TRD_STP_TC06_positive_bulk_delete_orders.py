import pytest

from src.data.consts import LONG_WAIT
from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


# @pytest.mark.critical
def test(web, setup_bulk_test, cancel_bulk_delete):
    order_ids = setup_bulk_test(order_type=OrderType.STOP)
    expected_amount = 0 if len(order_ids) <= 30 else len(order_ids) - 30

    logger.info("Step 1: Bulk delete pending orders")
    web.trade_page.asset_tab.bulk_delete_orders()

    logger.info("Verify bulk delete notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti.bulk_delete_order_banner(order_ids), timeout=LONG_WAIT)

    logger.info(f"Verify asset tab amount is: {expected_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, expected_amount)
