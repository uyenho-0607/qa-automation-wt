from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade

from src.utils.logging_utils import logger


def test(web, symbol, get_asset_tab_amount, ):

    order_type = OrderType.sample_values()
    tab = AssetTabs.get_tab(order_type)

    trade_object = ObjectTrade(order_type=order_type, symbol=symbol)
    tab_amount = get_asset_tab_amount(order_type)
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type.upper()} Order with swap_to_units")
    web.trade_page.place_order_panel.place_order(
        trade_object, sl_type=SLTPType.sample_values(), tp_type=SLTPType.sample_values(), swap_to_units=True
    )

    logger.info("Verify trade confirmation modal information is correct")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 2: Confirm Place Order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    exp_noti = ObjectNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.order_submitted_banner())

    logger.info(f"Verify Asset Tab amount {tab.title()} is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(tab, tab_amount + 1)

    logger.info(f"Verify {tab.title()} item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
