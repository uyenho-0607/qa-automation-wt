from src.data.enums import Features, OrderType
from src.data.objects.notification_object import ObjectNoti
from src.data.objects.trade_object import ObjectTrade

from src.utils.logging_utils import logger


def test(web, symbol, disable_OCT):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)

    logger.info(f"Step 1: Search and select symbol: {symbol!r}")
    web.home_page.search_symbol(symbol)
    web.home_page.select_item_from_search_result(symbol)
    web.home_page.wait_for_spin_loader()

    logger.info(f"Step 2: Place new order with {symbol!r}")
    web.trade_page.place_order_panel.place_order(trade_object, submit=True)

    logger.info("Verify order summited")
    web.home_page.notifications.verify_notification_banner(ObjectNoti(trade_object).order_submitted_banner()[0])
    web.home_page.notifications.close_noti_banner()

    logger.info("Step 3: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info(f"Verify {symbol} displayed in my trade")
    web.markets_page.verify_my_trade_last_item(symbol, trade_object.trade_type)
