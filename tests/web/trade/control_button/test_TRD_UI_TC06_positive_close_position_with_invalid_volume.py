import pytest

from src.data.enums import AssetTabs
from src.utils import random_utils
from src.utils.logging_utils import logger


@pytest.mark.parametrize("volume", (
        random_utils.random_number_by_length(),
        -123,
        random_utils.random_username(),
))
def test(web, setup_close_position_test, volume):
    order_id = setup_close_position_test.order_id
    tab_amount = setup_close_position_test.tab_amount

    logger.info(f"Step 1: Attempt partial close with invalid volume input: {volume!r}")
    web.trade_page.asset_tab.partial_close_position(order_id, volume=volume, confirm=False)

    logger.info("Step 2: Confirm close order with force option due to invalid volume")
    web.trade_page.modals.confirm_close_order(force=True)

    logger.info(f"Verify asset tab amount decreased to {tab_amount - 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount - 1)

    logger.info("Verify position is no longer displayed in the table")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, order_id, is_display=False)
