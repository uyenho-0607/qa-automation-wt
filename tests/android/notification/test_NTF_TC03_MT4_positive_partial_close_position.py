import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features, NotificationTab
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.format_utils import remove_comma
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.mt4]


def test(android, symbol, get_notification_tab_amount):
    trade_object = ObjTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    APIClient().trade.post_order(trade_object, update_price=True)

    logger.info("Step 2: Get Notification tab amount")
    noti_tab_amount = get_notification_tab_amount()

    logger.info(f"Step 3: Select tab {AssetTabs.OPEN_POSITION.value!r}")
    android.trade_screen.asset_tab.select_tab(AssetTabs.OPEN_POSITION)

    logger.info(f"Verify order placed successfully, order_id = {trade_object.order_id!r}")
    android.trade_screen.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id)

    logger.info("Step 5: Partial close position")
    # Object for new created open position
    new_object = ObjTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})
    android.trade_screen.asset_tab.partial_close_position(new_object, trade_object.order_id)

    # Normalize all numeric values
    orig_volume = int(trade_object.volume)
    orig_units = int(remove_comma(trade_object.units))

    logger.info(f"Partial close completed. Closed volume={int(new_object.close_volume)}, units={int(remove_comma(new_object.close_units))}")

    # Build object for closed position with ALL required fields
    close_trade = ObjTrade(**dict(trade_object))
    close_trade.volume = int(new_object.close_volume)
    close_trade.units = int(remove_comma(new_object.close_units))

    logger.info(f"Verify close order notification banner (vol={close_trade.volume}, units={close_trade.units})")
    exp_noti = ObjNoti(close_trade)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    # After verifying the close notification, calculate the remaining position and update trade_object accordingly
    trade_object.volume = orig_volume - close_trade.volume
    trade_object.units = orig_units - close_trade.units
    logger.info(f"Expected remaining after partial close: vol={trade_object.volume}, units={trade_object.units}")

    logger.info(f"Step 6: Get latest order_id")
    trade_object.order_id = android.trade_screen.asset_tab.get_last_order_id(AssetTabs.OPEN_POSITION)
    logger.info(f"Got updated order_id = {trade_object.order_id!r}")

    logger.info("Step 7: Navigate to Home screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify notification tab amount increased to {noti_tab_amount + 2}")
    android.home_screen.notifications.verify_tab_amount(NotificationTab.ORDER, noti_tab_amount + 2)

    logger.info(f"Verify position closed noti in notification box")
    # Use the close_trade object that has all required fields
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info("Verify Open Position noti in Notification Box")
    android.home_screen.notifications.verify_notification_result(
        ObjNoti(trade_object).open_position_details(trade_object.order_id))
