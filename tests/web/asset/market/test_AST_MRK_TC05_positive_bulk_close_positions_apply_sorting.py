from src.data.enums import AssetTabs, SortOptions
from src.data.objects.notification_object import ObjectNoti
from src.utils.logging_utils import logger


def test(web, setup_bulk_asset_test, cancel_bulk_delete):
    # -------------------
    tab_amount, order_ids = setup_bulk_asset_test()
    expected_amount = 0 if len(order_ids) <= 30 else len(order_ids) - 30
    # -------------------
    logger.info("Step 1: Apply sorting option")
    web.trade_page.asset_tab.apply_sorting(SortOptions.OPEN_DATE)

    logger.info("Step 2: Bulk Close Positions")
    web.assets_page.asset_tab.bulk_close_positions()

    logger.info("Verify bulk close notification banner")
    exp_noti = ObjectNoti.bulk_close_open_position_banner(order_ids)
    web.home_page.notifications.verify_notification_banner(*exp_noti)

    logger.info(f"Verify asset tab amount is: {expected_amount}")
    web.assets_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, expected_amount)

    logger.info("Verify items displayed in History Tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.HISTORY, order_ids)
