import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, market_obj, cancel_close_order):
    trade_object = market_obj()

    logger.info("Step 1: Get tab amount")
    tab_amount = web.assets_page.asset_tab.get_tab_amount(AssetTabs.OPEN_POSITION)

    logger.info(f"Step 2: Place {trade_object.trade_type.value.upper()} Order (tab:{tab_amount!r})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.PRICE, tp_type=SLTPType.PRICE, submit=True)
    web.home_page.notifications.close_noti_banner()

    logger.info(f"Verify order placed successfully, tab = {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Step 3: Close Position")
    web.trade_page.asset_tab.full_close_position(trade_object)

    logger.info("Verify Close order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_object).position_closed_details())

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info(f"Verify asset tab amount = {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount)

    logger.info("Step 4: Select History Tab")
    web.trade_page.asset_tab.select_tab(AssetTabs.HISTORY)

    logger.info("Verify history order details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)


@pytest.fixture(autouse=True)
def teardown(web):
    yield
    web.trade_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
