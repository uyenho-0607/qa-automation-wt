import random

from src.data.enums import OrderType, AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(web, symbol, get_asset_tab_amount, disable_OCT):

    trade_object = ObjTrade(order_type=random.choice(OrderType.pending()))
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info("Step 1: Open Chart fullscreen")
    web.trade_page.chart.toggle_chart()

    logger.info("Step 2: Open Trade Tab from Chart")
    web.trade_page.chart.open_trade_tab()

    logger.info(f"Step 3: Place Pending order")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=SLTPType.random_values(), tp_type=SLTPType.random_values())

    logger.info(f"Verify trade confirmation")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm place order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Step 5: Close Trade tab & Exit Chart fullscreen")
    web.trade_page.chart.close_trade_tab()
    web.trade_page.chart.toggle_chart(fullscreen=False)

    logger.info(f"Verify amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info("Step 6: Select Pending tab")
    web.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info(f"Verify item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
