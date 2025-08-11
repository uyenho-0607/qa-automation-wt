from src.data.enums import Features, SignalTab
from src.utils.logging_utils import logger


def test(android):
    
    logger.info("Step 1: Navigate to Signal Page")
    android.home_screen.navigate_to(Features.SIGNAL)
    
    logger.info("Step 2: Add signal to favourites from Signal List")
    signal_id = android.signal_screen.add_signal_to_favourites()
    
    logger.info(f"Verify signal {signal_id!r} is displayed in Favourites tab")
    android.signal_screen.select_tab(SignalTab.FAVOURITE)
    android.signal_screen.verify_signal_in_favourites(signal_id)
    
    logger.info("Step 3: Remove signal from favourites")
    android.signal_screen.remove_signal_from_favourites(signal_id)
    
    logger.info(f"Verify signal {signal_id!r} no longer displayed in Favourites tab")
    android.signal_screen.verify_signal_not_in_favourites(signal_id)