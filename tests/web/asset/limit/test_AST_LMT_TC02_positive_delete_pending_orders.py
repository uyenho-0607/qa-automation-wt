import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType, Features
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (None, None),
        (SLTPType.sample_values(), None),
        (None, SLTPType.sample_values()),
        SLTPType.sample_values(amount=2),
    ]
)
def test(web, symbol, sl_type, tp_type, search_symbol):
    trade_object = ObjectTrade(order_type=OrderType.LIMIT, symbol=symbol)
    tab = AssetTabs.PENDING_ORDER
    # -------------------

    logger.info(f"Step 1: Place {trade_object.trade_type} Order with SL: {sl_type!r}, TP: {tp_type!r}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, submit=True)
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 2: Get order_id")
    web.assets_page.asset_tab.get_last_order_id(trade_object)

    logger.info("Step 3: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Step 4: Delete pending order")
    web.assets_page.asset_tab.delete_pending_order(order_id=trade_object.order_id)

    logger.info(f"Verify {tab.title()} notification banner deleted message")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).delete_order_banner())

    logger.info("Verify item is no longer displayed")
    web.trade_page.asset_tab.verify_item_displayed(AssetTabs.PENDING_ORDER, trade_object.order_id, is_display=False)
