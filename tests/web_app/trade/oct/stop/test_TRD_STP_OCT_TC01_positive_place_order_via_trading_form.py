import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.format_utils import format_display_dict
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("sl_type, tp_type", [(SLTPType.PRICE, SLTPType.PRICE)])
def test(web_app, stop_obj, get_asset_tab_amount, sl_type, tp_type):
    trade_object = stop_obj()
    tab = AssetTabs.PENDING_ORDER

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 2: Open pre-trade details form")
    web_app.trade_page.place_order_panel.open_pre_trade_details()

    logger.info(f"Step 3: Place order: {format_display_dict(trade_object)} (sl_type:{sl_type.value.title()}, tp_type:{tp_type.value.title()}, tab:{tab_amount})")
    web_app.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify Order Submitted Notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    web_app.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info("Step 4: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    web_app.trade_page.asset_tab.verify_item_data(trade_object)
