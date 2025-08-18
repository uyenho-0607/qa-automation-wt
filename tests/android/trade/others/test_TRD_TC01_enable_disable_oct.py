from src.utils.logging_utils import logger


def test_oct_enable(android, symbol):
    logger.info(f"Step 1: Enable the OCT")
    android.trade_screen.place_order_panel.toggle_oct(submit=True)

    logger.info(f"Verify if the elements are present")
    android.trade_screen.place_order_panel.verify_oct_action(oct_action=True)


def test_oct_disable(android, symbol):
    logger.info(f"Step 1: Disable the OCT")
    android.trade_screen.place_order_panel.toggle_oct(enable=False)

    logger.info(f"Verify if the elements are present")
    android.trade_screen.place_order_panel.verify_oct_action(oct_action=False)
