import pytest

from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, symbol, setup_bulk_test, cancel_bulk_close):
    order_ids = setup_bulk_test(order_type=OrderType.MARKET)
    expected_amount = 0 if len(order_ids) <= 30 else len(order_ids) - 30
    # -------------------

    logger.info(f"Step 1: Bulk close positions")
    web_app.trade_page.asset_tab.bulk_close_positions()

    logger.info(f"Verify bulk close notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti.bulk_close_open_position_banner(order_ids))
    web_app.home_page.notifications.close_noti_banner()

    logger.info(f"Verify asset tab amount is {expected_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, expected_amount)
