from src.data.objects.notification_obj import ObjNoti

from src.utils.logging_utils import logger


def test(web, market_obj, update_entry_price):
    trade_obj = market_obj()

    logger.info(f"Step 1: Place {trade_obj.trade_type} Order with swap_to_units")
    web.trade_page.place_order_panel.place_order(trade_obj, swap_to_units=True, swap_to_volume=False)

    logger.info(f"Verify trade confirmation")
    web.trade_page.modals.verify_trade_confirmation(trade_obj)

    logger.info("Step 2: Confirm place order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_obj).order_submitted_banner())

    logger.info(f"Verify order details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_obj)

    logger.info("Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_obj).open_position_details(trade_obj.order_id))
