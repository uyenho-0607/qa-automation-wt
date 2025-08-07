from src.data.enums import AssetTabs
from src.data.ui_messages import UIMessages
from src.utils.logging_utils import logger


def test(web, setup_close_position_test):
    _, min_vol, max_vol, order_id = setup_close_position_test.values()

    logger.info("Step 2: Test increase and decrease buttons")
    web.trade_page.asset_tab.click_close_button()
    web.trade_page.asset_tab.adjust_close_volume_by_control_button(inc_step=True, dec_step=True)

    logger.info("Step 3: Set volume to minimum")
    web.trade_page.asset_tab.adjust_close_volume_by_control_button(min_volume=True)

    logger.info("Verify min and decrease buttons are disabled")
    web.trade_page.asset_tab.verify_volume_btn_disabled(min_button=True, dec_button=True)

    logger.info("Verify minimum volume value")
    web.trade_page.asset_tab.verify_min_max_value(min_value=min_vol)

    logger.info("Step 4: Set volume to maximum")
    web.trade_page.asset_tab.adjust_close_volume_by_control_button(max_volume=True)

    logger.info("Verify max and increase buttons are disabled")
    web.trade_page.asset_tab.verify_volume_btn_disabled(max_button=True, inc_button=True)

    logger.info("Verify maximum volume value")
    web.trade_page.asset_tab.verify_min_max_value(max_value=max_vol)

    logger.info("Step 5: Confirm close order")
    web.trade_page.modals.confirm_close_order()

    logger.info("Verify close order notification banner")
    web.home_page.notifications.verify_notification_banner(UIMessages.CLOSE_ORDER_BANNER_TITLE)

    logger.info("Verify order is closed")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, order_id, is_display=False)
