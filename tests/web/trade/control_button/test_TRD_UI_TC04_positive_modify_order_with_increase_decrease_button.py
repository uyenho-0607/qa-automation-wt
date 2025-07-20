from src.data.enums import AssetTabs, OrderType
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade

from src.utils.logging_utils import logger


def test(web, symbol, get_asset_tab_amount, ):
    # -------------------

    order_type = OrderType.sample_values()
    tab = AssetTabs.get_tab(order_type)

    trade_object = ObjTrade(order_type=order_type, symbol=symbol)
    tab_amount = get_asset_tab_amount(order_type)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} Order with control button")
    web.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info("Step 2: Modify order with control button")
    web.trade_page.asset_tab.click_edit_button(tab)
    web.trade_page.modals.modify_order_with_control_buttons(trade_object)

    logger.info("Verify order updated notification banner")
    exp_noti = ObjNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.order_updated_banner())

    logger.info("Verify item details in asset tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
