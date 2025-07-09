from src.data.enums import Features, MarketsSection, WatchListTab
from src.utils.logging_utils import logger


def test(web, ):
    logger.info(f"Step 1: Select arrow: {MarketsSection.MY_TRADE.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.click_arrow_icon(MarketsSection.MY_TRADE)

    logger.info("Verify Page is redirected to Asset Page")
    web.assets_page.verify_page_url()

    logger.info(f"Step 2: Select arrow: {MarketsSection.TOP_PICKS.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.click_arrow_icon(MarketsSection.TOP_PICKS)

    logger.info("Verify Top Picks Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.TOP_PICKS)

    logger.info(f"Step 3: Select arrow: {MarketsSection.TOP_GAINER.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.click_arrow_icon(MarketsSection.TOP_GAINER)

    logger.info("Verify Top Picks Tab on Trade Page is selected")
    web.trade_page.watch_list.verify_tab_selected(WatchListTab.TOP_GAINER)

    logger.info(f"Step 4: Select arrow: {MarketsSection.SIGNAL.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.click_arrow_icon(MarketsSection.SIGNAL)

    logger.info("Verify Page is redirected to Signal Page")
    web.signal_page.verify_page_url()

    logger.info(f"Step 5: Select arrow: {MarketsSection.NEWS.title()!r}")
    web.home_page.navigate_to(Features.MARKETS)
    web.markets_page.click_arrow_icon(MarketsSection.NEWS)

    logger.info("Verify Page is redirected to Signal Page")
    web.news_page.verify_page_url()
