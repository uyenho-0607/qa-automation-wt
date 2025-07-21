
from src.data.enums import WatchListTab, Features
from src.utils.logging_utils import logger


def test(android):
    
    logger.info(f"Step 1: Navigate to Markets Page")
    android.home_screen.navigate_to(Features.MARKETS)
    
    logger.info("Step 2: Click and mark star for from Trade Page")
    star_symbol = android.markets_screen.watch_list.toggle_star_symbol(mark_star=True)
    
    logger.info(f"Verify symbols {star_symbol!r} is displayed in Favourites tab - Market Page")
    android.markets_screen.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, star_symbol)
    
    logger.info(f"Step 3: Click on Favourites tab to remove symbols:")
    android.home_screen.navigate_to(Features.MARKETS)
    android.markets_screen.watch_list.select_tab(WatchListTab.FAVOURITES)
    unstar_symbol = android.markets_screen.watch_list.toggle_star_symbol(mark_star=False)
    
    logger.info(f"Verify symbols {unstar_symbol!r} no longer displayed in Favourites tab - Market Page")
    android.markets_screen.watch_list.verify_symbols_displayed(WatchListTab.FAVOURITES, unstar_symbol, is_display=False)