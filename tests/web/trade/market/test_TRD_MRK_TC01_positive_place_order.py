import allure
import pytest

from src.data.enums import AssetTabs, SLTPType, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@allure.issue("https://aquariux.atlassian.net/browse/WT-8757", "WT-8757")
@pytest.mark.critical
@pytest.mark.parametrize(
    "sl_type, tp_type",
    [
        (None, None),
        (SLTPType.random_values(), None),
        (None, SLTPType.random_values()),
        (SLTPType.POINTS, SLTPType.POINTS),
        (SLTPType.PRICE, SLTPType.PRICE),
        SLTPType.sample_values(amount=2)
    ]
)
def test(web, symbol, get_asset_tab_amount, sl_type, tp_type, update_entry_price, close_confirm_modal):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} order with sl_type: {sl_type!r}, tp_type: {tp_type!r}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify trade confirmation modal information is correct")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 2: Confirm Place Order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Verify Asset Tab amount: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify order details in Asset Tab")
    update_entry_price(trade_object)
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info("Verify Open Position noti in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjectNoti(trade_object).open_position_details(trade_object.order_id))
