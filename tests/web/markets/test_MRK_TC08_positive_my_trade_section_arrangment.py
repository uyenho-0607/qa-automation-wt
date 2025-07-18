import random
import time

import pytest

from src.data.consts import SYMBOLS
from src.data.enums import OrderType, Features, WatchListTab, MarketsSection
from src.data.objects.trade_object import ObjectTrade
from src.data.project_info import ProjectConfig
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, disable_OCT):

    symbol_list = random.choices(SYMBOLS[ProjectConfig.client], k=5)

    logger.info("Step 1: Navigate to Trade Page")
    time.sleep(1)
    web.home_page.navigate_to(Features.TRADE, wait=True)

    logger.info("Step 2: Select Tab Crypto")
    web.trade_page.watch_list.select_tab(WatchListTab.CRYPTO)

    for idx, _symbol in enumerate(symbol_list):

        logger.info(f"Step {3 + idx * 2}: Select symbol from watch list - {_symbol!r}")
        web.trade_page.watch_list.select_symbol(_symbol)

        logger.info(f"Step {4 + idx * 2}: Place Market orders")
        web.trade_page.place_order_panel.place_order(ObjectTrade(order_type=OrderType.MARKET, symbol=_symbol), submit=True)
        web.home_page.notifications.close_noti_banner()
        time.sleep(2)

    logger.info("Step 13: Navigate to Market Page and check My Trade Section")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info(f"Verify symbols list displayed in My Trade are: {symbol_list[::-1]}")
    web.markets_page.verify_my_trade_items_list(symbol_list[::-1])

    logger.info(f"Step 14: Place Pending Order for symbol: {symbol_list[-1]}")
    web.markets_page.select_symbol(MarketsSection.MY_TRADE)

    trade_obj = ObjectTrade(symbol=symbol_list[-1], order_type=OrderType.LIMIT)
    web.trade_page.place_order_panel.place_order(trade_obj, submit=True)

    logger.info("Step 15: Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info("Verify displaying symbols are not changed")
    web.markets_page.verify_my_trade_items_list(symbol_list[::-1])
