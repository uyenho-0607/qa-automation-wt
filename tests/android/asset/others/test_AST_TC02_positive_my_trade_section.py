import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.symbol_obj import ObjSymbol
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(android, setup_test):

    symbols = setup_test

    logger.info("Step 1: Navigate to Asset Screen")
    android.home_screen.navigate_to(Features.ASSETS, wait=True)

    logger.info(f"Verify My Trade list: {', '.join(symbols)} (result from test setup)")
    android.assets_screen.verify_my_trade_list(symbols)

    logger.info(f"Step 2: Select latest symbol from My Trade ({symbols[0]!r})")
    android.assets_screen.watch_list.select_last_symbol(tab=None)
    trade_obj = ObjTrade(symbol=symbols[0], order_type=random.choice(OrderType.pending()))

    logger.info(f"Step 3: Place {trade_obj.order_type.upper()!r} Order")
    android.trade_screen.place_order_panel.place_order(trade_obj, submit=True, sl_type=None, tp_type=None)

    logger.info("Verify Order Submitted Notification banner")
    android.home_screen.notifications.verify_notification_banner(expected_title=ObjNoti(trade_obj).order_submitted_banner()[0])

    logger.info("Step 4: Navigate to Asset Screen")
    android.home_screen.navigate_to(Features.ASSETS, wait=True)

    logger.info(f"Verify My Trade list is not changed ({', '.join(symbols)})")
    android.assets_screen.verify_my_trade_list(symbols)


@pytest.fixture
def setup_test(android):
    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")

    logger.info("- Send API request to get current placed Markets orders", setup=True)
    order_details = APIClient().order.get_orders_details(order_type=OrderType.MARKET, exclude_issue_symbols=False)

    if len(order_details) < 5:
        amount = 5 - len(order_details)

        logger.info(f"- No market order available, Place {amount} new orders", setup=True)
        symbols = random.choices(ObjSymbol().get_symbols(get_all=True), k=amount)
        for _symbol in symbols:
            APIClient().trade.post_order(ObjTrade(symbol=_symbol, order_type=OrderType.MARKET), update_price=False)

        order_details = APIClient().order.get_orders_details(order_type=OrderType.MARKET)

    symbols = [item["symbol"] for item in order_details][:5]

    logger.info(f">> Setup Summary: 5 latest placed Market orders: {', ' .join(symbols)}", setup=True)
    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield symbols