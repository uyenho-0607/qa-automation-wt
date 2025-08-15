import pytest

from src.utils.logging_utils import logger


@pytest.mark.critical
def test(ios, teardown):
    logger.info("Step 1: Open My Account modal")
    ios.home_screen.open_my_account()

    logger.info("Step 2: Close Balance section")
    ios.home_screen.my_account_modal.toggle_balance(open=False)

    logger.info("Verify Balance section is closed")
    ios.home_screen.my_account_modal.verify_balance_items_displayed(is_display=False)

    logger.info("Step 3: Open Balance section")
    ios.home_screen.my_account_modal.toggle_balance(open=True)

    logger.info("Verify Balance section is opened")
    ios.home_screen.my_account_modal.verify_balance_items_displayed(is_display=True)

    logger.info("Step 4: Close Notes section")
    ios.home_screen.my_account_modal.toggle_note(open=False)

    logger.info("Verify Notes section is closed")
    ios.home_screen.my_account_modal.verify_note_items_displayed(is_display=False)

    logger.info("Step 5: Open Notes section")
    ios.home_screen.my_account_modal.toggle_note(open=True)

    logger.info("Verify Notes section is closed")
    ios.home_screen.my_account_modal.verify_note_items_displayed(is_display=True)


@pytest.fixture
def teardown(ios):
    yield
    logger.info("- Close My Account modal")
    ios.home_screen.my_account_modal.close()
