import pytest

from src.data.enums import Features, SignalTab
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(android):
    
    logger.info("Step 1: Navigate to Signal Page")
    android.home_screen.navigate_to(Features.SIGNAL)
    
    logger.info("Step 2: Add signal to favourites")
    signal_id = android.signal_screen.add_signal_to_favourites()
    
    logger.info(f"Verify signal {signal_id!r} is displayed in Favourites tab")
    android.signal_screen.select_tab(SignalTab.FAVOURITE)
    android.signal_screen.verify_signal_in_favourites(signal_id)
    
    logger.info("Step 3: Copy favourite signal to order")
    signal_data = android.signal_screen.select_signal_for_copy()
    trade_object = android.signal_screen.copy_signal_to_order(signal_data)
    
    logger.info("Verify trade order panel populated with favourite signal data")
    android.trade_screen.place_order_panel.verify_signal_data_populated(trade_object)
    
    logger.info("Step 4: Submit the copied order")
    android.trade_screen.place_order_panel.submit_order()
    
    logger.info("Verify trade confirmation")
    android.trade_screen.modals.verify_trade_confirmation(trade_object)
    
    logger.info("Step 5: Confirm place order")
    android.trade_screen.modals.confirm_trade()


@pytest.fixture(autouse=True)
def teardown_test(android):
    yield
    logger.info("- Teardown test")
    android.trade_screen.place_order_panel.click_cancel_btn()