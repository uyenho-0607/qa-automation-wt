import allure
import pytest

from src.apis.api_client import APIClient
from src.data.enums import Features, MarketsSection, WatchListTab, OrderType
from src.data.objects.trade_obj import ObjTrade
from src.utils import DotDict
from src.utils.logging_utils import logger


@allure.issue("https://aquariux.atlassian.net/browse/WT-8765", "WT-8765")
@pytest.mark.critical
def test(web, setup_test):
    section_symbol = setup_test

    for step, (section, symbol) in enumerate(section_symbol.items(), 1):
        logger.info(f"Step {step}: Select symbol from {section.title()}")
        # Navigate to Markets page (except for first iteration if it's already there)
        web.home_page.navigate_to(Features.MARKETS, wait=True)

        # Select symbol from the section
        web.markets_page.select_symbol(section)

        # Verify based on section type
        if section == MarketsSection.SIGNAL:
            logger.info(f"Verify symbol {symbol!r} is selected in Signal Page")
            web.signal_page.verify_signal_selected(symbol)

        else:
            # Verify correct tab is selected based on section
            expected_tab = {
                MarketsSection.MY_TRADE: WatchListTab.ALL,
                MarketsSection.TOP_PICKS: WatchListTab.TOP_PICKS,
                MarketsSection.TOP_GAINER: WatchListTab.TOP_GAINER
            }.get(section)

            if expected_tab:
                logger.info(f"Verify {expected_tab.value} Tab on Trade Page is selected")
                web.trade_page.watch_list.verify_tab_selected(expected_tab)
                
                logger.info(f"Verify symbol {symbol} is selected")
                web.trade_page.watch_list.verify_symbol_selected(symbol)

    # todo: increase coverage: add more check on symbol details is selected

@pytest.fixture
def setup_test(web):
    section_symbol = DotDict()

    logger.info("- POST some order for my-trade section")
    for _ in range(3):
        APIClient().trade.post_order(trade_object=ObjTrade(order_type=OrderType.MARKET), update_price=False)

    logger.info("- Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS, wait=True)

    logger.info("- Get section symbols")
    web.markets_page.get_last_symbol(store_data=section_symbol)

    remove_keys = []
    for key in section_symbol.keys():
        if not section_symbol[key] and key not in [MarketsSection.MY_TRADE, MarketsSection.SIGNAL]:
            remove_keys.append(key)

    yield {k: v for k, v in section_symbol.items() if k not in remove_keys}
