import allure
import pytest

from src.data.enums import AssetTabs, SLTPType
from src.data.objects.notification_obj import ObjNoti
from src.utils.logging_utils import logger


@allure.issue("https://aquariux.atlassian.net/browse/WT-8757", "[Multi OMS][MT5] - WT-8757")
@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (None, None),
        (SLTPType.random_values(), None),
        (None, SLTPType.random_values()),
        SLTPType.random_values(amount=2)
    ]
)
def test(web, market_obj, sl_type, tp_type, ):
    trade_object = market_obj()

    logger.info("Step 1: Get tab amount")
    tab_amount = web.trade_page.asset_tab.get_tab_amount(AssetTabs.OPEN_POSITION)

    logger.info(f"Step 2: Place {trade_object.trade_type} order for {trade_object.symbol!r} (SL:{sl_type}, TP:{tp_type}, tab:{tab_amount})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, submit=False)

    logger.info("Step 3: Get current server/ device time")
    web.home_page.get_server_device_time(trade_object)

    logger.info(f"Verify order submitted notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify order details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f"Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id))
