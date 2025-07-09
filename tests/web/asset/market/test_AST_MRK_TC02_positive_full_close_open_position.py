import pytest

from src.data.enums import OrderType, SLTPType, Features, AssetTabs
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
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, submit=True)
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Get item order_id from notification")
    web.trade_page.asset_tab.get_last_item_data(trade_object=trade_object)  # reload new data

    logger.info("Step 3: Navigate to Asset Page and close Position")
    web.home_page.navigate_to(Features.ASSETS)
    web.assets_page.asset_tab.full_close_position(trade_object.order_id)

    logger.info("Verify Close order notification banner")
    exp_noti = ObjectNoti(trade_object)
    web.home_page.notifications.verify_notification_banner(*exp_noti.close_order_success_banner())

    logger.info("Verify Close Position noti in notification box")
    web.home_page.notifications.verify_notification_result(exp_noti.position_closed_details(), check_contains=True)

    logger.info(f"Verify item is no longer displayed in Open Positions tab")
    web.assets_page.asset_tab.verify_item_displayed(AssetTabs.OPEN_POSITION, trade_object.order_id, is_display=False)

    logger.info("Verify history order item details")
    web.assets_page.asset_tab.verify_item_data(trade_object, AssetTabs.HISTORY)
