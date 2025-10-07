import pytest

from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web_app, symbol, get_asset_tab_amount, cancel_all, create_order_data):
    trade_object = ObjTrade(order_type=OrderType.STOP_LIMIT, symbol=symbol)
    tab = AssetTabs.PENDING_ORDER
    # ------------------- #

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    logger.info(f"Step 3: Select Pending Orders tab")
    web_app.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify order placed successfully, order_id: {trade_object.order_id!r}")
    web_app.trade_page.asset_tab.verify_item_displayed(tab, trade_object.order_id)

    logger.info(f"Step 4: Delete pending order (order_id:{trade_object.order_id})")
    web_app.trade_page.asset_tab.delete_order(trade_object=trade_object, confirm=False)

    logger.info("Verify Delete Order Notification banner")
    web_app.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify {tab.title()} amount = {tab_amount}")
    web_app.trade_page.asset_tab.verify_tab_amount(tab, tab_amount)

    logger.info("Verify item is no longer displayed in Pending Orders tab")
    web_app.trade_page.asset_tab.verify_item_displayed(tab, trade_object.order_id, is_display=False)
