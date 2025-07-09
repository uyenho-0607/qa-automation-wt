import pytest

from src.data.enums import OrderType, AssetTabs, TradeType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize("trade_type", TradeType.list_values())
def test(web, symbol, get_asset_tab_amount, trade_type, enable_OCT):

    trade_object = ObjectTrade(trade_type, OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(OrderType.MARKET)

    logger.info("Step 1: Enter Chart fullscreen")
    web.trade_page.chart.toggle_chart()

    logger.info(f"Step 2: Place {trade_type.upper()} order")
    web.trade_page.place_order_panel.place_oct_order(trade_object)

    logger.info("Verify notification banner displays correct input trade information")
    web.home_page.notifications.verify_notification_banner(*ObjectNoti(trade_object).order_submitted_banner())

    logger.info(f"Step 3: Exit Chart fullscreen")
    web.trade_page.chart.toggle_chart(fullscreen=False)

    logger.info(f"Verify amount is: {tab_amount + 1}")
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.OPEN_POSITION, tab_amount + 1)

    logger.info(f"Verify item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)

    logger.info(f"Verify notification in Notification Box")
    web.home_page.notifications.verify_notification_result(ObjectNoti(trade_object).open_position_details(trade_object.order_id))
