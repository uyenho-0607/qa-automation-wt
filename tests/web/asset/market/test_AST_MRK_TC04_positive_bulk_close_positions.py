import pytest

from src.data.enums import AssetTabs, BulkCloseOpts
from src.data.objects.notification_object import ObjectNoti
from src.utils.logging_utils import logger


@pytest.mark.parametrize("close_option", (BulkCloseOpts.ALL, BulkCloseOpts.LOSS,))
def test(web, setup_bulk_asset_test, close_option, cancel_bulk_close):
    # -------------------
    tab_amount, order_ids = setup_bulk_asset_test()
    # -------------------
    logger.info(f"Step 1: Bulk Close Positions with option: {close_option.upper()!r}")
    web.assets_page.asset_tab.bulk_close_positions(close_option)

    logger.info("Verify bulk close notification banner")
    exp_noti = ObjectNoti.bulk_close_open_position_banner(order_ids)
    web.home_page.notifications.verify_notification_banner(*exp_noti)

    logger.info(f"Verify asset tab amount is: {tab_amount - len(order_ids)}")
    web.assets_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount - len(order_ids))

    logger.info("Verify items displayed in History Tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.HISTORY, order_ids)
