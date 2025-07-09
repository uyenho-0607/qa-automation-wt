from src.data.enums import OrderType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade

from src.utils.logging_utils import logger


def test(web, symbol, update_entry_price):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with swap_to_volume")
    web.trade_page.place_order_panel.place_order(trade_object, swap_to_volume=True, submit=True)

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify order details in Asset Tab")
    update_entry_price(trade_object)
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjectNoti(trade_object).open_position_details(trade_object.order_id))
