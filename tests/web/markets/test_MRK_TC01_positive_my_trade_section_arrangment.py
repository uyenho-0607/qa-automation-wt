import random

import pytest

from src.apis.api_client import APIClient
from src.data.enums import OrderType, Features, MarketsSection, AssetTabs
from src.data.objects.notification_obj import ObjNoti
from src.data.objects.symbol_obj import ObjSymbol
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, disable_OCT, setup_test):
    order_amount = setup_test
    step_idx = 1

    if order_amount < 5:
        step_idx += 1
        placed_amount = 5 - order_amount

        symbol_list = random.choices(ObjSymbol().get_symbols(get_all=True), k=5)

        logger.info(f"Step 1: Send API to place {placed_amount} more Market Orders ({', '.join(symbol_list)}) (current orders:{order_amount})")

        for _symbol in symbol_list:
            trade_obj = ObjTrade(symbol=_symbol, order_type=OrderType.MARKET)
            APIClient().trade.post_order(trade_object=trade_obj, update_price=False)

    logger.info(f"Step {step_idx}: Navigate to Asset Page and get 5 latest Open Positions")
    web.home_page.navigate_to(Features.ASSETS, wait=True)
    order_list = web.assets_page.asset_tab.get_symbols()[:5]

    logger.info(f"Step {step_idx + 1}: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Verify My Trade list: {', '.join(order_list)} (result from step {step_idx})")
    web.markets_page.verify_my_trade_list(order_list)

    logger.info(f"Step {step_idx + 2}: Place Pending Order for symbol: {order_list[-1]}")
    trade_obj = ObjTrade(symbol=order_list[-1], order_type=OrderType.LIMIT)

    web.markets_page.select_symbol(MarketsSection.MY_TRADE, order_list[-1], wait=True)
    web.trade_page.place_order_panel.place_order(trade_obj, submit=True)
    web.home_page.notifications.close_noti_banner()
    web.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

    logger.info("Verify placed order details in Pending Orders Tab")
    web.trade_page.asset_tab.verify_item_data(trade_obj, AssetTabs.PENDING_ORDER, wait=True)

    logger.info(f"Step {step_idx + 3}: Navigate to back Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Verify My Trade list is not changed ({', '.join(order_list)})")
    web.markets_page.verify_my_trade_list(order_list)

    logger.info(f"Step {step_idx + 4}: Navigate to Asset Page and close 1 order")
    web.markets_page.navigate_to(Features.ASSETS, wait=True)
    web.assets_page.asset_tab.full_close_position()

    logger.info("Verify close order notification banner")
    web.home_page.notifications.verify_notification_banner(ObjNoti(trade_obj).close_order_success_banner()[0])

    logger.info(f"Step {step_idx + 5}: Get current Open Positions after closing order")
    cur_symbols = web.assets_page.asset_tab.get_symbols()[:5]

    logger.info(f"Step {step_idx + 6}: Navigate to Market Page")
    web.assets_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Verify My Trade list is changed after closing order: {', '.join(cur_symbols)}")
    web.markets_page.verify_my_trade_list(cur_symbols)


@pytest.fixture(autouse=True)
def setup_test(web, ):
    logger.info(f"{'=' * 10} Setup Test - Start {'=' * 10}")

    logger.info("- Send API request to get current placed Markets orders")
    tab_amount = APIClient().order.get_counts(order_type=OrderType.MARKET)

    logger.info(f"{'=' * 10} Setup Test - Done {'=' * 10}")

    yield tab_amount

    logger.info("[Cleanup] Navigate back to markets page")
    web.home_page.navigate_to(Features.MARKETS)
