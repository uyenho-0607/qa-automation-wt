import pytest

from src.data.enums import Features
from src.data.objects.trade_obj import ObjTrade
from src.utils.logging_utils import logger


def test(android):
    
    logger.info("Step 1: Navigate to Signal Page")
    android.home_screen.navigate_to(Features.SIGNAL)
    
    logger.info("Step 2: Select a signal to copy")
    signal_data = android.signal_screen.select_signal_for_copy()
    
    logger.info("Step 3: Copy signal to order")
    trade_object = android.signal_screen.copy_signal_to_order(signal_data)
    
    logger.info("Verify trade order panel populated with signal data")
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