import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
@pytest.mark.parametrize("sltp_type", [SLTPType.PRICE, SLTPType.POINTS])
def test(web, symbol, get_asset_tab_amount, cancel_close_order, sltp_type, create_order_data):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol, indicate=sltp_type)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    create_order_data(trade_object)

    # Object for new created open position
    new_object = ObjectTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})

    logger.info("Step 2: Close Position")
    web.trade_page.asset_tab.partial_close_position(trade_object=new_object)

    # update new volume, units after partial close
    trade_object.volume, trade_object.units = new_object.close_volume, new_object.close_units

    logger.info("Verify Close order notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).close_order_success_banner())

    logger.info(f"Verify new open position created, asset tab amount = {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(ObjectNoti(trade_object).position_closed_details(), check_contains=True)

    logger.info("Verify Open Position details in asset tab")
    web.trade_page.asset_tab.verify_item_data(new_object)

    logger.info("Verify history order details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
