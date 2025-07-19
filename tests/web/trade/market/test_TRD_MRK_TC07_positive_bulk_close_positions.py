import pytest

from src.data.consts import LONG_WAIT
from src.data.enums import AssetTabs, BulkCloseOpts, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("close_option", (BulkCloseOpts.ALL, ))
def test(web, setup_bulk_test, cancel_bulk_close, close_option, get_order_id_list):
    order_ids = setup_bulk_test(order_type=OrderType.MARKET)
    expected_amount = 0 if len(order_ids) <= 30 else len(order_ids) - 30
    # -------------------

    logger.info(f"Step 1: Bulk close positions")
    web.trade_page.asset_tab.bulk_close_positions(close_option)

    logger.info("Verify bulk close notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti.bulk_close_open_position_banner(order_ids), timeout=LONG_WAIT)

    logger.info(f"Verify asset tab amount is: {expected_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, expected_amount)
