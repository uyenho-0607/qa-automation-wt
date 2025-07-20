import pytest

from src.data.enums import SLTPType, TradeType, OrderType, AssetTabs, Expiry
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade
from src.utils.logging_utils import logger


@pytest.mark.parametrize(
    "trade_type, order_type, expiry, sl_type, tp_type",
    [
        (TradeType.sample_values(), OrderType.random_values(except_val=[OrderType.MARKET]), Expiry.GOOD_TILL_DAY, *SLTPType.sample_values(amount=2)),
        (TradeType.sample_values(), OrderType.random_values(except_val=[OrderType.MARKET]), Expiry.GOOD_TILL_CANCELLED, *SLTPType.sample_values(amount=2)),
    ]
)
def test(web, symbol, get_asset_tab_amount, trade_type, order_type, sl_type, tp_type, expiry, disable_OCT):
    trade_object = ObjectTrade(trade_type, order_type, symbol, expiry=expiry)
    tab_amount = get_asset_tab_amount(order_type)

    logger.info("Step 1: Enter Chart fullscreen and open trade tab")
    web.trade_page.chart.toggle_chart()
    web.trade_page.chart.open_trade_tab()

    logger.info(f"Step 2: Place order")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

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
    web.trade_page.asset_tab.verify_tab_amount(AssetTabs.PENDING_ORDER, tab_amount + 1)

    logger.info(f"Verify item details in Asset Tab")
    web.trade_page.asset_tab.verify_item_data(trade_object)
