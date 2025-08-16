import random

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, get_asset_tab_amount, cancel_delete_order):
    trade_object = ObjTrade(order_type=random.choice(OrderType.pending()), symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=False)

    logger.info(f"Verify Asset Tab amount: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 2: Select Pending Order tab")
    web.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info("Step 3: Delete pending order")
    web.trade_page.asset_tab.delete_order(trade_object, confirm=False)

    logger.info("Verify delete order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).delete_order_banner())

    logger.info(f"Verify Asset Tab amount = {tab_amount}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount)

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
