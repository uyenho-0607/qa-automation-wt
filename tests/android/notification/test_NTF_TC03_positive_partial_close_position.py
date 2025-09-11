import pytest

from src.apis.api_client import APIClient
from src.data.enums import AssetTabs, OrderType, Features, NotificationTab
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


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

    # Store original volume and units before partial close
    original_volume = trade_object.volume
    original_units = trade_object.units

    # Object for new created open position
    new_object = ObjTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})
    print("new open position", new_object)

    logger.info("Step 5: Partial close position")
    android.trade_screen.asset_tab.partial_close_position(new_object, trade_object.order_id, confirm=True)

    # Calculate remaining volume and units after partial close
    # The close_volume and close_units represent the amount that was closed
    remaining_volume = original_volume - new_object.close_volume
    remaining_units = original_units - new_object.close_units

    # Update trade object with remaining position
    trade_object.volume = remaining_volume
    trade_object.units = remaining_units

    print(f"Original volume/units: {original_volume}/{original_units}")
    print(f"Closed volume/units: {new_object.close_volume}/{new_object.close_units}")
    print(f"Remaining volume/units: {remaining_volume}/{remaining_units}")

    logger.info(f"Verify close order notification banner")
    exp_noti = ObjNoti(trade_object)
    android.home_screen.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info(f"Step 6: Get updated order_id")
    android.trade_screen.asset_tab.get_last_order_id(trade_object)
    logger.info(f"Got updated order_id = {trade_object.order_id!r}")

    logger.info("Step 7: Navigate to Home screen")
    android.trade_screen.navigate_to(Features.HOME)

    logger.info(f"Verify notification tab amount increased to {noti_tab_amount + 2}")
    android.home_screen.notifications.verify_tab_amount(NotificationTab.ORDER, noti_tab_amount + 2)

    logger.info(f"Verify position closed noti in notification box")
    android.home_screen.notifications.verify_notification_result(exp_noti.position_closed_details())

    logger.info("Verify Open Position noti in Notification Box")
    android.home_screen.notifications.verify_notification_result(
        ObjNoti(trade_object).open_position_details(trade_object.order_id), go_back=False)