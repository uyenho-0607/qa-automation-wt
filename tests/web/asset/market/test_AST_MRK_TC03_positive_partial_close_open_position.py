import pytest

from src.data.enums import AssetTabs, OrderType, SLTPType, Features
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "sl_type, tp_type", [
        (SLTPType.PRICE, SLTPType.PRICE),
        (SLTPType.POINTS, SLTPType.POINTS),
        SLTPType.sample_values(amount=2),
    ]
)
def test(web, symbol, sl_type, tp_type, search_symbol):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, submit=True)
    web.home_page.notifications.close_noti_banner()

    # Object for new created open position
    new_object = ObjectTrade(**{k: v for k, v in trade_object.items() if k != "order_id"})

    logger.info("Step 2: Get item order_id from notification")
    web.home_page.notifications.get_open_position_order_id(trade_object)

    logger.info("Step 3: Get item data from asset tab")
    web.trade_page.asset_tab.get_item_data(order_id=trade_object.order_id, trade_object=trade_object)

    logger.info("Step 4: Navigate to Asset Page and close Position")
    web.home_page.navigate_to(Features.ASSETS)
    web.assets_page.asset_tab.partial_close_position(trade_object.order_id, trade_object=new_object)

    # update new volume, units after partial close
    trade_object.volume, trade_object.units = new_object.close_volume, new_object.close_units

    logger.info("Verify Close order notification banner")
    exp_noti = ObjectNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details(), check_contains=True)

    logger.info("Verify Open Position details in asset tab")
    web.trade_page.asset_tab.verify_item_data(new_object)

    logger.info("Verify history order item details")
    web.trade_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
