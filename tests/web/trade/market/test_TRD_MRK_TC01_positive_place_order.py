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
def test(web, market_obj, get_asset_tab_amount, sl_type, tp_type, close_confirm_modal):
    trade_object = market_obj()

    logger.info("Step 1: Get tab amount")
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 2: Place {trade_object.trade_type} order for {trade_object.symbol!r} (SL:{sl_type}, TP:{tp_type}, tab:{tab_amount})")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info(f"Verify trade confirmation")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Get current server/ device time")
    web.home_page.get_server_device_time(trade_object)

    logger.info("Step 4: Confirm place order")
    web.trade_page.modals.confirm_trade()

    logger.info(f"Verify order submitted notification banner")
    web.home_page.notifications.verify_notification_banner(*ObjNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount increased to {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify order details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f"Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjNoti(trade_object).open_position_details(trade_object.order_id))
