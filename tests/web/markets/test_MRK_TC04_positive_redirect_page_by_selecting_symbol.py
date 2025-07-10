import pytest

from src.data.enums import Features, MarketsSection, WatchListTab
from src.utils import DotDict
from src.utils.logging_utils import logger


@pytest.mark.critical
def test(web, setup_test):
    section_symbol = setup_test
    my_trade, top_pick, top_gainer, signal = MarketsSection.list_values(except_val=MarketsSection.NEWS)

    logger.info(f"Step 1: Select symbol from {my_trade.title()!r}")
    web.markets_page.select_symbol(my_trade)

    logger.info("Verify All Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.ALL)

    logger.info(f"Verify symbol {section_symbol[my_trade]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(section_symbol[my_trade])

    logger.info(f"Step 2: Select symbol from {top_pick.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.select_symbol(top_pick)

    logger.info("Verify Top Picks Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.TOP_PICKS)

    logger.info(f"Verify symbol {section_symbol[top_pick]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(section_symbol[top_pick])

    logger.info(f"Step 3: Select symbol from {top_gainer.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.select_symbol(top_gainer)

    logger.info("Verify Top Gainer Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.TOP_GAINER)

    logger.info(f"Verify symbol {section_symbol[top_gainer]} is selected")
    web.trade_page.watch_list.verify_symbol_selected(section_symbol[top_gainer])

    logger.info(f"Step 4: Select symbol from {signal.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.select_symbol(signal)

    logger.info(f"Verify symbol {section_symbol[signal]!r} is selected in Signal Page")
    web.signal_page.verify_signal_selected(section_symbol[signal])

    # todo: increase coverage: add more check on symbol details is selected

@pytest.fixture
def setup_test(web):
    section_symbol = DotDict()

    logger.info("- Navigate to Market Page")
    web.home_page.navigate_to(Features.MARKETS)

    logger.info("- Get section symbols")
    web.markets_page.get_last_symbol(store_data=section_symbol)

    yield section_symbol
