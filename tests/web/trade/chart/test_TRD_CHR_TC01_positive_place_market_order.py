import pytest

from src.data.enums import TradeType, OrderType, AssetTabs
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("trade_type", [TradeType.BUY, TradeType.SELL])
def test(web, symbol, get_asset_tab_amount, trade_type, sl_type, tp_type, disable_OCT):
    trade_object = ObjectTrade(trade_type, OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(OrderType.MARKET)

    logger.info("Step 1: Enter Chart fullscreen and open trade tab")
    web.trade_page.chart.toggle_chart()
    web.trade_page.chart.open_trade_tab()

    logger.info(f"Step 2: Place {trade_type.upper()} order, sl: {sl_type!r}, tp: {tp_type!r}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type, is_chart=True)

    logger.info("Verify trade confirmation modal information is correct")
    web.trade_page.modals.verify_trade_confirmation(trade_object)

    logger.info("Step 3: Confirm Place Order")
    web.trade_page.modals.confirm_trade()

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Step 4: Exit Chart fullscreen")
    web.trade_page.chart.close_trade_tab()
    web.trade_page.chart.toggle_chart(fullscreen=False)

    logger.info(f"Verify amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f"Verify notification in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjectNoti(trade_object).open_position_details(trade_object.order_id))
