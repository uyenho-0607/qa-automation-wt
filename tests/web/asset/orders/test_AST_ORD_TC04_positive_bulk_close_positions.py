import pytest

from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_bulk_asset_test, cancel_bulk_close):

    tab_amount, order_ids = setup_bulk_asset_test(order_type=OrderType.MARKET)
    expected_amount = 0 if tab_amount <= 30 else tab_amount - 30
    # -------------------
    logger.info(f"Step 1: Bulk Close Positions")
    web.assets_page.asset_tab.bulk_close_positions()

    logger.info("Verify bulk close notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti.bulk_close_open_position_banner(order_ids))

    logger.info(f"Verify asset tab amount is: {expected_amount}")
    web.assets_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, expected_amount)

    logger.info("Verify items displayed in History Tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.HISTORY, order_ids)
